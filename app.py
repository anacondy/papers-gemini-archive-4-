import os
import re
from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory, abort
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit

app = Flask(__name__)

# Security configurations
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE  # Limit file upload size
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Security headers middleware
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    # Content Security Policy - adjust as needed for your assets
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self'"
    return response


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def sanitize(text):
    """Sanitize text to prevent injection attacks"""
    if not text:
        return ""
    # Remove any potentially harmful characters
    return "".join(c for c in text if c.isalnum() or c in (' ', '_', '-')).rstrip()


def validate_filename(filename):
    """Validate filename to prevent path traversal attacks"""
    if not filename:
        return False
    # Check for path traversal attempts
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    return True


@app.route('/')
def terminal_ui():
    return render_template('index.html')


@app.route('/admin')
def upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload with comprehensive security checks"""
    # MODIFIED: time and max_marks are no longer required
    required_fields = ['admin_name', 'class', 'subject', 'semester', 'exam_year', 'exam_type', 'medium']
    
    # Check if file is present
    if 'file' not in request.files:
        return "<h1>No file provided. <a href='/admin'>Please try again.</a></h1>", 400
    
    # Check all required fields are present
    if not all(field in request.form for field in required_fields):
        return "<h1>Missing form data. <a href='/admin'>Please try again.</a></h1>", 400

    file = request.files['file']

    # Safely get all fields
    admin_name = request.form.get('admin_name', '').strip()
    class_name = request.form.get('class', '').strip()
    subject = request.form.get('subject', '').strip()
    semester = request.form.get('semester', '').strip()
    exam_year = request.form.get('exam_year', '').strip()
    exam_type = request.form.get('exam_type', '').strip()
    medium = request.form.get('medium', '').strip()
    time = request.form.get('time', 'N/A').strip()  # Default to 'N/A' if empty
    max_marks = request.form.get('max_marks', 'N/A').strip()  # Default to 'N/A' if empty

    # Validate all required fields are not empty
    if file.filename == '' or not all([admin_name, class_name, subject, semester, exam_year, exam_type, medium]):
        return "<h1>A required field is empty. <a href='/admin'>Please try again.</a></h1>", 400

    # Validate filename for security
    if not validate_filename(file.filename):
        return "<h1>Invalid filename. <a href='/admin'>Please try again.</a></h1>", 400

    # Check file extension
    if not allowed_file(file.filename):
        return "<h1>Invalid file type. Only PDFs are allowed. <a href='/admin'>Please try again</a></h1>", 400

    # Process and save file
    try:
        tags = [sanitize(class_name), sanitize(subject), f"Sem-{sanitize(semester)}", sanitize(exam_year),
                sanitize(exam_type), sanitize(medium), sanitize(admin_name)]
        filename_prefix = "_".join(f"[{tag}]" for tag in tags)
        original_secure_name = secure_filename(file.filename)
        original_base, original_ext = os.path.splitext(original_secure_name)
        new_filename = f"{filename_prefix}_{original_base}{original_ext}"
        
        # Additional security: ensure filename is not too long
        if len(new_filename) > 255:
            return "<h1>Generated filename is too long. Please use shorter values. <a href='/admin'>Try again.</a></h1>", 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        
        # Ensure the file will be saved in the uploads directory (prevent path traversal)
        if not os.path.abspath(filepath).startswith(os.path.abspath(app.config['UPLOAD_FOLDER'])):
            return "<h1>Invalid file path. <a href='/admin'>Please try again.</a></h1>", 400
        
        file.save(filepath)

        # Add metadata to PDF
        try:
            reader = PdfReader(filepath)
            writer = PdfWriter()
            for page in reader.pages: 
                writer.add_page(page)
            keywords = f"{class_name}, {exam_year}, Sem {semester}, {exam_type}, {medium}, Time: {time}, Marks: {max_marks}"
            writer.add_metadata(
                {"/Author": admin_name, "/Title": f"{class_name} - {subject} (Sem {semester})", "/Subject": subject,
                 "/Keywords": keywords})
            with open(filepath, "wb") as f:
                writer.write(f)
        except Exception as e:
            print(f"Could not write metadata. Error: {e}")
            # Continue even if metadata writing fails

        return f"""
            <style> body {{ font-family: sans-serif; background-color: #1a1a1a; color: #e0e0e0; padding: 40px; }} h1 {{ color: #4CAF50; }} p {{ color: #bbb; }} a {{ display: inline-block; margin-top: 20px; padding: 10px 15px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 4px; }} a:hover {{ background-color: #45a049; }} </style>
            <h1>File Uploaded Successfully!</h1> <p>Metadata has been written directly into the PDF properties.</p> <p><strong>Saved as:</strong> {new_filename}</p> <a href="/">Go to Home Page</a>
        """
    except Exception as e:
        print(f"Upload error: {e}")
        return "<h1>An error occurred during upload. <a href='/admin'>Please try again.</a></h1>", 500


@app.route('/api/papers')
def get_papers():
    """API endpoint to get list of papers"""
    papers = []
    pattern = re.compile(r"\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_\[(.*?)\]_(.*\.pdf)",
                         re.IGNORECASE)
    
    try:
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            # Skip hidden files and non-files
            if filename.startswith('.'):
                continue
            
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
    except Exception as e:
        print(f"Error reading upload folder: {e}")
        return jsonify([]), 500
    
    return jsonify(papers)


@app.route('/uploads/<path:filename>')
def get_uploaded_file(filename):
    """Serve uploaded files with security checks"""
    # Validate filename to prevent path traversal
    if not validate_filename(filename):
        abort(404)
    
    # Additional security: ensure file exists and is a PDF
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath) or not allowed_file(filename):
        abort(404)
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    # Security: Never run with debug=True in production
    # Use environment variable to control debug mode
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)
