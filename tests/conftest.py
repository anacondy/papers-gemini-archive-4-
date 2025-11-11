"""
Test configuration and fixtures for Terminal Archives application.
"""
import os
import sys
import pytest
import tempfile
import shutil
from werkzeug.security import generate_password_hash

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app as app_module


@pytest.fixture
def app():
    """Create and configure a test instance of the app."""
    # Create a temporary directory for uploads
    test_upload_folder = tempfile.mkdtemp()
    
    # Set test configuration
    app_module.app.config['TESTING'] = True
    app_module.app.config['UPLOAD_FOLDER'] = test_upload_folder
    app_module.app.config['SECRET_KEY'] = 'test-secret-key'
    app_module.app.config['WTF_CSRF_ENABLED'] = False
    
    # Override admin password hash for testing
    app_module.ADMIN_PASSWORD_HASH = generate_password_hash('test_password')
    
    yield app_module.app
    
    # Cleanup
    shutil.rmtree(test_upload_folder, ignore_errors=True)


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def authenticated_client(client):
    """Create an authenticated test client."""
    with client.session_transaction() as session:
        session['admin_authenticated'] = True
    return client


@pytest.fixture
def sample_pdf():
    """Create a sample PDF file for testing."""
    from PyPDF2 import PdfWriter
    import io
    
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    
    pdf_buffer = io.BytesIO()
    writer.write(pdf_buffer)
    pdf_buffer.seek(0)
    
    return pdf_buffer
