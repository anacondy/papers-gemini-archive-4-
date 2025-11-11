"""
Integration tests for routes and endpoints in the Terminal Archives application.
"""
import pytest
import io
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestRoutes:
    """Test suite for application routes."""
    
    def test_homepage_loads(self, client):
        """Test that homepage loads successfully."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Terminal' in response.data or b'terminal' in response.data
    
    def test_admin_page_redirects_when_not_authenticated(self, client):
        """Test that admin page redirects to login when not authenticated."""
        response = client.get('/admin', follow_redirects=False)
        assert response.status_code == 302
        assert '/admin/login' in response.location
    
    def test_admin_page_loads_when_authenticated(self, authenticated_client):
        """Test that admin page loads when authenticated."""
        response = authenticated_client.get('/admin')
        assert response.status_code == 200
        assert b'upload' in response.data.lower() or b'Upload' in response.data
    
    def test_admin_login_page_loads(self, client):
        """Test that login page loads successfully."""
        response = client.get('/admin/login')
        assert response.status_code == 200
        assert b'password' in response.data.lower()
    
    def test_admin_login_with_correct_password(self, client):
        """Test login with correct credentials."""
        response = client.post('/admin/login', data={
            'password': 'test_password'
        }, follow_redirects=False)
        assert response.status_code == 302
        assert '/admin' in response.location
    
    def test_admin_login_with_wrong_password(self, client):
        """Test login with incorrect credentials."""
        response = client.post('/admin/login', data={
            'password': 'wrong_password'
        })
        assert response.status_code == 200
        assert b'Invalid' in response.data or b'invalid' in response.data
    
    def test_admin_logout(self, authenticated_client):
        """Test logout functionality."""
        response = authenticated_client.get('/admin/logout', follow_redirects=False)
        assert response.status_code == 302
        
        # Verify we can't access admin page after logout
        response = authenticated_client.get('/admin', follow_redirects=False)
        assert response.status_code == 302
    
    def test_api_papers_endpoint(self, client):
        """Test the papers API endpoint."""
        response = client.get('/api/papers')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        # Should return a JSON array (even if empty)
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_404_error_handler(self, client):
        """Test custom 404 error page."""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404
        assert b'404' in response.data or b'Not Found' in response.data


class TestSecurityHeaders:
    """Test suite for security headers."""
    
    def test_security_headers_present(self, client):
        """Test that security headers are set correctly."""
        response = client.get('/')
        
        # Check for required security headers
        assert 'X-Content-Type-Options' in response.headers
        assert response.headers['X-Content-Type-Options'] == 'nosniff'
        
        assert 'X-Frame-Options' in response.headers
        assert response.headers['X-Frame-Options'] == 'DENY'
        
        assert 'X-XSS-Protection' in response.headers
        assert response.headers['X-XSS-Protection'] == '1; mode=block'
        
        assert 'Strict-Transport-Security' in response.headers
        assert 'max-age' in response.headers['Strict-Transport-Security']
        
        assert 'Content-Security-Policy' in response.headers


class TestFileUpload:
    """Test suite for file upload functionality."""
    
    def test_upload_without_authentication(self, client, sample_pdf):
        """Test that upload requires authentication."""
        data = {
            'file': (sample_pdf, 'test.pdf'),
            'admin_name': 'Test Admin',
            'class': 'BSc',
            'subject': 'Physics',
            'semester': '3',
            'exam_year': '2024',
            'exam_type': 'Main Semester',
            'medium': 'English Medium'
        }
        response = client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 401
    
    def test_upload_with_valid_data(self, authenticated_client, sample_pdf):
        """Test successful file upload with all required fields."""
        data = {
            'file': (sample_pdf, 'test.pdf'),
            'admin_name': 'Test Admin',
            'class': 'BSc',
            'subject': 'Physics',
            'semester': '3',
            'exam_year': '2024',
            'exam_type': 'Main Semester',
            'medium': 'English Medium',
            'time': '3 hr',
            'max_marks': '100'
        }
        response = authenticated_client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        assert b'success' in response.data.lower() or b'uploaded' in response.data.lower()
    
    def test_upload_missing_required_field(self, authenticated_client, sample_pdf):
        """Test upload fails when required field is missing."""
        data = {
            'file': (sample_pdf, 'test.pdf'),
            'admin_name': 'Test Admin',
            'class': 'BSc',
            # Missing subject
            'semester': '3',
            'exam_year': '2024',
            'exam_type': 'Main Semester',
            'medium': 'English Medium'
        }
        response = authenticated_client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        assert b'Missing' in response.data or b'missing' in response.data or b'required' in response.data
    
    def test_upload_with_non_pdf_file(self, authenticated_client):
        """Test that non-PDF files are rejected."""
        # Create a fake text file
        fake_file = io.BytesIO(b'This is not a PDF file')
        data = {
            'file': (fake_file, 'test.txt'),
            'admin_name': 'Test Admin',
            'class': 'BSc',
            'subject': 'Physics',
            'semester': '3',
            'exam_year': '2024',
            'exam_type': 'Main Semester',
            'medium': 'English Medium'
        }
        response = authenticated_client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        assert b'Invalid' in response.data or b'invalid' in response.data or b'PDF' in response.data
    
    def test_upload_without_file(self, authenticated_client):
        """Test upload fails when no file is provided."""
        data = {
            'admin_name': 'Test Admin',
            'class': 'BSc',
            'subject': 'Physics',
            'semester': '3',
            'exam_year': '2024',
            'exam_type': 'Main Semester',
            'medium': 'English Medium'
        }
        response = authenticated_client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        assert b'Missing' in response.data or b'missing' in response.data


class TestInputSanitization:
    """Test suite for input sanitization and security."""
    
    def test_sanitize_prevents_path_traversal_in_upload(self, authenticated_client, sample_pdf):
        """Test that path traversal attempts are sanitized."""
        data = {
            'file': (sample_pdf, 'test.pdf'),
            'admin_name': '../../etc/passwd',
            'class': 'BSc',
            'subject': '../../../test',
            'semester': '3',
            'exam_year': '2024',
            'exam_type': 'Main Semester',
            'medium': 'English Medium'
        }
        response = authenticated_client.post('/upload', data=data, content_type='multipart/form-data')
        # Should succeed but with sanitized filenames
        assert response.status_code == 200
        # Check that dangerous characters were removed
        assert b'../' not in response.data
    
    def test_sanitize_prevents_xss_in_upload(self, authenticated_client, sample_pdf):
        """Test that XSS attempts are sanitized."""
        data = {
            'file': (sample_pdf, 'test.pdf'),
            'admin_name': '<script>alert("xss")</script>',
            'class': 'BSc',
            'subject': 'Physics<script>',
            'semester': '3',
            'exam_year': '2024',
            'exam_type': 'Main Semester',
            'medium': 'English Medium'
        }
        response = authenticated_client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        # Script tags should not appear in response
        assert b'<script>' not in response.data
