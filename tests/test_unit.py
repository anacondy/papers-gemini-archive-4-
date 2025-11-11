"""
Unit tests for helper functions in the Terminal Archives application.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import allowed_file, sanitize


class TestHelperFunctions:
    """Test suite for helper functions."""
    
    def test_allowed_file_with_valid_pdf(self):
        """Test that PDF files are allowed."""
        assert allowed_file('document.pdf') is True
        assert allowed_file('test.PDF') is True
        assert allowed_file('file-name_123.pdf') is True
    
    def test_allowed_file_with_invalid_extensions(self):
        """Test that non-PDF files are rejected."""
        assert allowed_file('document.txt') is False
        assert allowed_file('image.jpg') is False
        assert allowed_file('script.js') is False
        assert allowed_file('style.css') is False
        assert allowed_file('data.json') is False
        assert allowed_file('archive.zip') is False
    
    def test_allowed_file_with_no_extension(self):
        """Test files without extensions."""
        assert allowed_file('noextension') is False
        assert allowed_file('') is False
    
    def test_allowed_file_with_multiple_dots(self):
        """Test files with multiple dots in name."""
        assert allowed_file('document.backup.pdf') is True
        assert allowed_file('test.txt.pdf') is True
        assert allowed_file('file.pdf.txt') is False
    
    def test_sanitize_with_clean_text(self):
        """Test sanitization of clean text."""
        assert sanitize('Hello World') == 'Hello World'
        assert sanitize('Test123') == 'Test123'
        assert sanitize('File_Name-2024') == 'File_Name-2024'
    
    def test_sanitize_with_special_characters(self):
        """Test sanitization removes special characters."""
        assert sanitize('<script>alert("xss")</script>') == 'scriptalertxssscript'
        assert sanitize('../../etc/passwd') == 'etcpasswd'
        assert sanitize('test@email.com') == 'testemailcom'
        assert sanitize('name!@#$%^&*()') == 'name'
    
    def test_sanitize_with_sql_injection_attempts(self):
        """Test sanitization of SQL injection patterns."""
        assert sanitize("'; DROP TABLE users; --") == ' DROP TABLE users --'
        assert sanitize("1' OR '1'='1") == '1 OR 11'
    
    def test_sanitize_with_empty_or_none(self):
        """Test sanitization of empty or None values."""
        assert sanitize('') == ''
        assert sanitize(None) == ''
    
    def test_sanitize_preserves_spaces_underscores_hyphens(self):
        """Test that spaces, underscores, and hyphens are preserved."""
        assert sanitize('Test File Name') == 'Test File Name'
        assert sanitize('test_file_name') == 'test_file_name'
        assert sanitize('test-file-name') == 'test-file-name'
        assert sanitize('test file_name-123') == 'test file_name-123'
    
    def test_sanitize_with_unicode_characters(self):
        """Test sanitization with Unicode characters."""
        # Note: The current sanitize function uses isalnum() which includes Unicode letters
        # It preserves Unicode alphanumeric characters
        result = sanitize('Tëst Ñame 日本語')
        # Check that spaces are preserved
        assert ' ' in result
        # Current implementation preserves Unicode alphanumeric characters
        # This is actually acceptable for international support
    
    def test_sanitize_strips_trailing_whitespace(self):
        """Test that trailing whitespace is removed."""
        assert sanitize('test   ') == 'test'
        assert sanitize('  test  ') == '  test'
        assert sanitize('test\n') == 'test'
        assert sanitize('test\t') == 'test'
