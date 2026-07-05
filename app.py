import os
import secrets
from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from services.http_responses import create_error_response, create_success_response
from services.paper_index import list_papers
from services.upload_utils import (
    allowed_file as is_allowed_file,
    sanitize as sanitize_input,
    extract_sanitized_fields,
    build_storage_filename,
    file_size_exceeds_limit,
    write_pdf_metadata,
    validate_safe_serving_path,
)

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

# Admin password hash for runtime auth checks.
# If ADMIN_PASSWORD is unset, a random one-time value is used so no static default exists.
ADMIN_PASSWORD_HASH = generate_password_hash(os.environ.get('ADMIN_PASSWORD', secrets.token_urlsafe(32)))


def check_admin_auth():
    """Check if admin is authenticated."""
    return session.get('admin_authenticated', False)


def allowed_file(filename):
    """Backwards-compatible helper used by tests and route logic."""
    return is_allowed_file(filename, ALLOWED_EXTENSIONS)


def sanitize(text):
    """Backwards-compatible helper used by tests and route logic."""
    return sanitize_input(text)


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
    return render_template(
        'upload.html',
        default_admin_name=os.environ.get('ADMIN_NAME', 'Alvido')
    )


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
    """Handle upload request, validation, storage, and metadata write flow."""
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
    fields = extract_sanitized_fields(request.form)

    # Check if all required fields are filled
    if file.filename == '' or not all([
        fields['admin_name'],
        fields['class_name'],
        fields['subject'],
        fields['semester'],
        fields['exam_year'],
        fields['exam_type'],
        fields['medium'],
    ]):
        return create_error_response(
            'Empty Required Field',
            'One or more required fields are empty.',
            '<a href="/admin">Go Back</a>'
        )

    if not file or not allowed_file(file.filename):
        return create_error_response(
            'Invalid File Type',
            'Only PDF files are allowed.',
            '<a href="/admin">Go Back</a>'
        )

    if file_size_exceeds_limit(file, MAX_FILE_SIZE):
        return create_error_response(
            'File Too Large',
            f'Maximum file size is {MAX_FILE_SIZE / 1024 / 1024}MB.',
            '<a href="/admin">Go Back</a>'
        )

    new_filename = build_storage_filename(fields, file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

    if os.path.exists(filepath):
        return create_error_response(
            'File Already Exists',
            'A file with similar details already exists.',
            '<a href="/admin">Go Back</a>'
        )

    file.save(filepath)

    try:
        write_pdf_metadata(filepath, fields)
    except Exception as e:
        print(f"Could not write metadata. Error: {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return create_error_response(
            'Error Processing PDF',
            'Failed to process the PDF file. Please try again.',
            '<a href="/admin">Go Back</a>'
        )

    return create_success_response(new_filename)


@app.route('/api/papers')
@limiter.limit(RATE_LIMIT_API)
def get_papers():
    """Return list of all uploaded papers in JSON format."""
    papers = list_papers(
        app.config['UPLOAD_FOLDER'],
        lambda filename: url_for('get_uploaded_file', filename=filename)
    )
    return jsonify(papers)


@app.route('/uploads/<path:filename>')
def get_uploaded_file(filename):
    """
    Serve uploaded PDF files securely.
    
    Security measures implemented:
    1. Filename sanitization with os.path.basename()
    2. Path separator check
    3. Absolute path verification (must be within upload folder)
    4. File existence and type verification
    5. Using Flask's secure send_from_directory function
    
    Note: CodeQL may flag this as a potential path injection, but this is
    a false positive due to the multiple layers of protection implemented.
    """
    safe_filename = validate_safe_serving_path(app.config['UPLOAD_FOLDER'], filename)
    if not safe_filename:
        abort(404)
    
    # Optional forced download mode. Default behavior keeps PDFs viewable in-browser.
    download_param = request.args.get('download', '').lower()
    force_download = download_param in {'1', 'true', 'yes'}

    # Flask's send_from_directory provides additional security
    response = send_from_directory(
        app.config['UPLOAD_FOLDER'],
        safe_filename,
        as_attachment=force_download,
        download_name=safe_filename if force_download else None
    )

    # Ensure inline rendering by default when browsers support it.
    if not force_download:
        response.headers['Content-Disposition'] = f'inline; filename="{safe_filename}"'

    return response


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
