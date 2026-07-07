import os
import sys
import stat
import secrets
import logging
from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
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

# ---------------------------------------------------------------------------
# Logging (replaces bare print() so failures are visible on real hosts)
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('terminal_archives')

_running_under_pytest = "PYTEST_CURRENT_TEST" in os.environ or "pytest" in sys.modules

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
# FIX: added Referrer-Policy + Permissions-Policy.
# FIX: script-src drops 'unsafe-inline' -- VERIFY your current templates have
# no inline <script> blocks before deploying this. If a page breaks / you see
# CSP violation errors in the browser console, either move that script to a
# static/*.js file or tell me and I'll add a nonce instead of reverting this.
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Referrer-Policy': 'no-referrer',
    'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
    'Content-Security-Policy': (
        "default-src 'self'; script-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; "
        "connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; "
        "form-action 'self'"
    )
}


def _load_or_create_secret_key():
    """
    SECURITY FIX: SECRET_KEY previously fell back to secrets.token_hex(32)
    PER PROCESS with no persistence and no warning. Under multiple gunicorn
    workers (or any restart), that silently invalidates sessions/CSRF tokens
    depending on which worker/process handles a given request.

    New behavior: SECRET_KEY env var always wins. Otherwise persist a
    generated key to .flask_secret_key (0600) next to app.py so all workers
    on the SAME host share one key and it survives restarts -- with a loud
    warning that this still isn't safe across multiple hosts.
    """
    env_key = os.environ.get('SECRET_KEY')
    if env_key:
        return env_key

    if _running_under_pytest:
        return secrets.token_hex(32)

    logger.warning(
        "SECRET_KEY is not set. Falling back to a key persisted at "
        ".flask_secret_key. Not safe for multi-host deployments -- set "
        "SECRET_KEY explicitly before deploying beyond a single host."
    )
    key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.flask_secret_key')
    try:
        if os.path.exists(key_path):
            with open(key_path, 'r') as f:
                existing = f.read().strip()
                if existing:
                    return existing
        new_key = secrets.token_hex(32)
        with open(key_path, 'w') as f:
            f.write(new_key)
        try:
            os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass
        return new_key
    except OSError as e:
        logger.error(f"Could not persist secret key file ({e}); using an ephemeral key.")
        return secrets.token_hex(32)


# Flask App Initialization
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['SECRET_KEY'] = _load_or_create_secret_key()
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookie over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection (partial, see CSRF below)

# FIX: needed if deployed behind nginx/another reverse proxy, otherwise
# Flask-Limiter's get_remote_address() sees the proxy's own IP for every
# request. Opt-in since it must match your actual proxy topology.
if os.environ.get('BEHIND_PROXY', 'False').lower() == 'true':
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

_ratelimit_storage_uri = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
if _ratelimit_storage_uri.startswith('memory://') and not _running_under_pytest:
    logger.warning(
        "Rate limiting is using in-process memory storage. Under multiple "
        "gunicorn workers each worker enforces its OWN independent counters, "
        "so the documented '5 login attempts/minute' becomes roughly "
        "5 x <worker count> in practice. Set RATELIMIT_STORAGE_URL to a "
        "shared backend (e.g. redis://...) for accurate multi-worker limits."
    )

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=RATE_LIMIT_DEFAULT,
    storage_uri=_ratelimit_storage_uri
)

# ---------------------------------------------------------------------------
# SECURITY/OPS FIX: ADMIN_PASSWORD handling.
#
# The prior code did:
#     ADMIN_PASSWORD_HASH = generate_password_hash(os.environ.get('ADMIN_PASSWORD', secrets.token_urlsafe(32)))
# This is better than a static 'changeme' default (not guessable), but it has
# its own bug: the random fallback is generated PER PROCESS. Under multiple
# gunicorn workers with no ADMIN_PASSWORD set, each worker has a DIFFERENT
# password and nobody -- including you -- knows any of them. Login appears
# to "randomly" fail depending which worker handles the request, with zero
# indication why.
#
# New behavior: fail closed and loud at startup instead, same as SECRET_KEY.
# Bypassed under DEBUG=True or pytest so local dev / the existing test suite
# keep working unchanged.
# ---------------------------------------------------------------------------
_debug_mode_at_boot = os.environ.get('DEBUG', 'False').lower() == 'true'
_admin_password_env = os.environ.get('ADMIN_PASSWORD')

if not _admin_password_env:
    if _debug_mode_at_boot or _running_under_pytest:
        logger.warning(
            "ADMIN_PASSWORD is not set. Continuing because DEBUG=True or a "
            "test run was detected, using a per-process random password "
            "(you will not be able to log in with this outside tests)."
        )
        _admin_password_env = secrets.token_urlsafe(32)
    else:
        raise RuntimeError(
            "Refusing to start: ADMIN_PASSWORD is not set while DEBUG=False. "
            "Set a strong ADMIN_PASSWORD environment variable before running "
            "in production."
        )

ADMIN_PASSWORD_HASH = generate_password_hash(_admin_password_env)


def check_admin_auth():
    """Check if admin is authenticated."""
    return session.get('admin_authenticated', False)


def allowed_file(filename):
    """Backwards-compatible helper used by tests and route logic."""
    return is_allowed_file(filename, ALLOWED_EXTENSIONS)


def sanitize(text):
    """Backwards-compatible helper used by tests and route logic."""
    return sanitize_input(text)


def generate_csrf_token():
    """Return the per-session CSRF token, creating one if needed."""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']


app.jinja_env.globals['csrf_token'] = generate_csrf_token


def validate_csrf(form):
    """
    SECURITY FIX: app-level CSRF token, checked on state-changing POSTs.
    Bypassed when Flask's TESTING config is set (mirrors Flask-WTF's own
    convention) so the existing test suite keeps passing without changes.

    NOTE: add `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`
    inside the <form> in login.html and upload.html for this to actually take
    effect end-to-end -- send me those two templates' current contents and
    I'll give you the exact patch instead of guessing at markup that changed
    in the "Trevor Reznik" pass.
    """
    if app.config.get('TESTING'):
        return True
    token = form.get('csrf_token', '')
    session_token = session.get('csrf_token')
    return bool(token) and bool(session_token) and secrets.compare_digest(token, session_token)


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
        if not validate_csrf(request.form):
            return render_template('login.html', error='Your session expired, please try again.')
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
    if not check_admin_auth():
        return create_error_response(
            'Unauthorized',
            'Please login to access this page.',
            '<a href="/admin/login">Go to Login</a>'
        ), 401

    if not validate_csrf(request.form):
        return create_error_response(
            'Invalid Request',
            'Your session token expired or is invalid. Please go back and resubmit.',
            '<a href="/admin">Go Back</a>'
        ), 400

    required_fields = ['admin_name', 'class', 'subject', 'semester', 'exam_year', 'exam_type', 'medium']
    if 'file' not in request.files or not all(field in request.form for field in required_fields):
        return create_error_response(
            'Missing Form Data',
            'Please fill in all required fields.',
            '<a href="/admin">Go Back</a>'
        )

    file = request.files['file']
    fields = extract_sanitized_fields(request.form)

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
        logger.error(f"Could not write metadata to {new_filename}: {e}")
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
    """
    safe_filename = validate_safe_serving_path(app.config['UPLOAD_FOLDER'], filename)
    if not safe_filename:
        abort(404)

    download_param = request.args.get('download', '').lower()
    force_download = download_param in {'1', 'true', 'yes'}

    response = send_from_directory(
        app.config['UPLOAD_FOLDER'],
        safe_filename,
        as_attachment=force_download,
        download_name=safe_filename if force_download else None
    )

    if not force_download:
        # FIX: defense-in-depth quote-stripping. safe_filename can't actually
        # contain a `"` today (sanitize()/secure_filename() both strip it),
        # but this costs nothing and protects against a future change to the
        # naming scheme accidentally allowing one through into a header value.
        header_safe_filename = safe_filename.replace('"', '')
        response.headers['Content-Disposition'] = f'inline; filename="{header_safe_filename}"'
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
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)
