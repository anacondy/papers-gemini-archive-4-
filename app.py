import os
import re
import secrets
from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory, session, abort
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from PyPDF2 import PdfReader, PdfWriter
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables
load_dotenv()

# Configuration Constants
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Rate Limiting Configuration
RATE_LIMIT_DEFAULT = ["200 per day", "50 per hour"]
RATE_LIMIT_UPLOAD = "10 per hour"
RATE_LIMIT_LOGIN = "5 per minute"
RATE_LIMIT_API = "100 per minute"

# Security Headers
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'"
}

# HTML Response Templates
HTML_ERROR_TEMPLATE = """
<style> 
    body {{ font-family: sans-serif; background-color: #1a1a1a; color: #e0e0e0; padding: 40px; }} 
    h1 {{ color: #4CAF50; }} 
    p {{ color: #bbb; }} 
    a {{ display: inline-block; margin-top: 20px; padding: 10px 15px; background-color: #4CAF50; 
         color: white; text-decoration: none; border-radius: 4px; }} 
    a:hover {{ background-color: #45a049; }} 
</style>
<h1>{title}</h1>
<p>{message}</p>
{links}
"""

HTML_SUCCESS_TEMPLATE = """
<style> 
    body {{ font-family: sans-serif; background-color: #1a1a1a; color: #e0e0e0; padding: 40px; }} 
    h1 {{ color: #4CAF50; }} 
    p {{ color: #bbb; }} 
    a {{ display: inline-block; margin-top: 20px; padding: 10px 15px; background-color: #4CAF50; 
         color: white; text-decoration: none; border-radius: 4px; }} 
    a:hover {{ background-color: #45a049; }} 
</style>
<h1>File Uploaded Successfully!</h1> 
<p>Metadata has been written directly into the PDF properties.</p> 
<p><strong>Saved as:</strong> {filename}</p> 
<a href="/">Go to Home Page</a> 
<a href="/admin">Upload Another</a>
"""

# Flask App Initialization
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookie over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=RATE_LIMIT_DEFAULT,
    storage_uri=os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
)

# Simple admin password (hashed)
ADMIN_PASSWORD_HASH = generate_password_hash(os.environ.get('ADMIN_PASSWORD', 'changeme'))


# Helper Functions
def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def sanitize(text):
    """Sanitize text to prevent injection attacks."""
    if not text:
        return ""
    return "".join(c for c in text if c.isalnum() or c in (' ', '_', '-')).rstrip()


def check_admin_auth():
    """Check if admin is authenticated."""
    return session.get('admin_authenticated', False)


def create_html_response(template, **kwargs):
    """Create an HTML response using a template."""
    return template.format(**kwargs)


def create_error_response(title, message, links=''):
    """Create a standardized error response."""
    return create_html_response(HTML_ERROR_TEMPLATE, title=title, message=message, links=links)


def create_success_response(filename):
    """Create a standardized success response."""
    return create_html_response(HTML_SUCCESS_TEMPLATE, filename=filename)


@app.after_request
def set_security_headers(response):
    """Add security headers to all responses."""
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    return response


@app.route('/')
def terminal_ui():
    return render_template('index.html')


@app.route('/admin')
def upload_form():
    if not check_admin_auth():
        return redirect(url_for('admin_login'))
    return render_template('upload.html')


@app.route('/admin/login', methods=['GET', 'POST'])
@limiter.limit(RATE_LIMIT_LOGIN)
def admin_login():
    """Handle admin login."""
    if request.method == 'POST':
        password = request.form.get('password', '')
        if check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['admin_authenticated'] = True
            session.permanent = True
            return redirect(url_for('upload_form'))
        else:
            return render_template('login.html', error='Invalid password')
    return render_template('login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_authenticated', None)
    return redirect(url_for('terminal_ui'))


@app.route('/upload', methods=['POST'])
@limiter.limit(RATE_LIMIT_UPLOAD)
def upload_file():
    """Handle file upload with validation and metadata embedding."""
    # Check admin authentication
    if not check_admin_auth():
        return create_error_response(
            'Unauthorized',
            'Please login to access this page.',
            '<a href="/admin/login">Go to Login</a>'
        ), 401
    
    # Validate form data
    required_fields = ['admin_name', 'class', 'subject', 'semester', 'exam_year', 'exam_type', 'medium']
    if 'file' not in request.files or not all(field in request.form for field in required_fields):
        return create_error_response(
            'Missing Form Data',
            'Please fill in all required fields.',
            '<a href="/admin">Go Back</a>'
        )

    file = request.files['file']

    # Safely get all fields and sanitize them
    admin_name = sanitize(request.form.get('admin_name', ''))
    class_name = sanitize(request.form.get('class', ''))
    subject = sanitize(request.form.get('subject', ''))
    semester = sanitize(request.form.get('semester', ''))
    exam_year = sanitize(request.form.get('exam_year', ''))
    exam_type = sanitize(request.form.get('exam_type', ''))
    medium = sanitize(request.form.get('medium', ''))
    time = sanitize(request.form.get('time', 'N/A'))  # Default to 'N/A' if empty
    max_marks = sanitize(request.form.get('max_marks', 'N/A'))  # Default to 'N/A' if empty

    # Check if all required fields are filled
    if file.filename == '' or not all([admin_name, class_name, subject, semester, exam_year, exam_type, medium]):
        return create_error_response(
            'Empty Required Field',
            'One or more required fields are empty.',
            '<a href="/admin">Go Back</a>'
        )

    if file and allowed_file(file.filename):
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return create_error_response(
                'File Too Large',
                f'Maximum file size is {MAX_FILE_SIZE / 1024 / 1024}MB.',
                '<a href="/admin">Go Back</a>'
            )
        
        # Create filename with tags
        tags = [class_name, subject, f"Sem-{semester}", exam_year, exam_type, medium, admin_name]
        filename_prefix = "_".join(f"[{tag}]" for tag in tags)
        original_secure_name = secure_filename(file.filename)
        original_base, original_ext = os.path.splitext(original_secure_name)
        new_filename = f"{filename_prefix}_{original_base}{original_ext}"
        
        # Ensure filename is safe and doesn't contain path traversal
        new_filename = os.path.basename(new_filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        
        # Check if file already exists
        if os.path.exists(filepath):
            return create_error_response(
                'File Already Exists',
                'A file with similar details already exists.',
                '<a href="/admin">Go Back</a>'
            )
        
        # Save file
        file.save(filepath)

        # Add metadata to PDF
        try:
            reader = PdfReader(filepath)
            writer = PdfWriter()
            for page in reader.pages: 
                writer.add_page(page)
            keywords = f"{class_name}, {exam_year}, Sem {semester}, {exam_type}, {medium}, Time: {time}, Marks: {max_marks}"
            writer.add_metadata({
                "/Author": admin_name, 
                "/Title": f"{class_name} - {subject} (Sem {semester})", 
                "/Subject": subject,
                "/Keywords": keywords
            })
            with open(filepath, "wb") as f:
                writer.write(f)
        except Exception as e:
            print(f"Could not write metadata. Error: {e}")
            # Clean up file if metadata writing fails
            if os.path.exists(filepath):
                os.remove(filepath)
            return create_error_response(
                'Error Processing PDF',
                'Failed to process the PDF file. Please try again.',
                '<a href="/admin">Go Back</a>'
            )

        return create_success_response(new_filename)
    else:
        return create_error_response(
            'Invalid File Type',
            'Only PDF files are allowed.',
            '<a href="/admin">Go Back</a>'
        )


@app.route('/api/papers')
@limiter.limit(RATE_LIMIT_API)
def get_papers():
    """Return list of all uploaded papers in JSON format."""
    papers = []
    pattern = re.compile(r"\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_(.*\.pdf)",
                         re.IGNORECASE)
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        return jsonify(papers)
    
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        match = pattern.match(filename)
        if match:
            try:
                groups = match.groups()
                paper_details = {
                    'class': groups[0], 
                    'subject': groups[1], 
                    'semester': groups[2].replace('Sem-', ''),
                    'year': groups[3], 
                    'exam_type': groups[4], 
                    'medium': groups[5], 
                    'uploader': groups[6],
                    'original_name': groups[7], 
                    'url': url_for('get_uploaded_file', filename=filename)
                }
                papers.append(paper_details)
            except Exception as e:
                print(f"Error processing matched file {filename}: {e}")
    return jsonify(papers)


@app.route('/uploads/<path:filename>')
def get_uploaded_file(filename):
    """Serve uploaded PDF files securely."""
    # Sanitize filename to prevent directory traversal
    filename = os.path.basename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Ensure the file exists and is within the upload folder
    upload_folder_abs = os.path.abspath(app.config['UPLOAD_FOLDER'])
    filepath_abs = os.path.abspath(filepath)
    
    if not os.path.exists(filepath) or not filepath_abs.startswith(upload_folder_abs):
        abort(404)
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return create_error_response(
        '404 - Page Not Found',
        'The page you are looking for does not exist.',
        '<a href="/">Go to Home</a>'
    ), 404


@app.errorhandler(413)
def file_too_large(e):
    """Handle file too large errors."""
    return create_error_response(
        'File Too Large',
        f'Maximum file size is {MAX_FILE_SIZE / 1024 / 1024}MB.',
        '<a href="/admin">Try Again</a>'
    ), 413


@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit errors."""
    return create_error_response(
        'Rate Limit Exceeded',
        'Too many requests. Please try again later.',
        '<a href="/">Go to Home</a>'
    ), 429


if __name__ == '__main__':
    # Never run with debug=True in production
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)
