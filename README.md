# 📚 Papers Archive - Previous Year Exam Papers Repository

A secure Flask-based web application for archiving and searching previous year exam papers with a terminal-style user interface.

## 🎯 Project Overview

This application provides a searchable archive of exam papers (PDFs) with metadata management. It features:
- **Terminal-style UI** for a unique user experience
- **Advanced search** by class, subject, year, semester, exam type, and medium
- **PDF metadata management** - automatically adds metadata to uploaded papers
- **Mobile responsive** design with touch-friendly search
- **Secure file upload** system with comprehensive validation

## 🔒 Security Features

This application implements multiple security layers:

### ✅ Implemented Security Measures
- **File Upload Security**
  - File size limit (10MB max)
  - File type validation (PDF only)
  - Filename sanitization and path traversal prevention
  - Secure filename generation
  
- **Security Headers**
  - Content Security Policy (CSP)
  - X-Frame-Options (clickjacking protection)
  - X-Content-Type-Options (MIME sniffing protection)
  - X-XSS-Protection
  - Strict-Transport-Security (HSTS)

- **Input Validation**
  - All user inputs are sanitized
  - Required field validation
  - Empty value checks

- **Application Security**
  - Secret key for session management
  - Debug mode disabled by default
  - Error handling with safe error messages

### ⚠️ Important Security Notes

**This application is NOT suitable for GitHub Pages deployment** because:
1. GitHub Pages only serves static files (HTML, CSS, JS)
2. This is a Flask application requiring a Python backend server
3. File upload functionality requires server-side processing
4. Database operations need a running application server

**Authentication/Authorization**: This application currently does NOT have:
- User authentication for the upload endpoint
- Admin access control
- User management system

**For production use, you MUST add:**
- Proper authentication system (Flask-Login, OAuth, etc.)
- Role-based access control
- Rate limiting for API endpoints
- HTTPS/SSL certificate
- Database for paper metadata (currently uses filesystem)
- Regular security audits and updates

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/anacondy/papers-gemini-archive-4-.git
cd papers-gemini-archive-4-
```

### 2. Create Virtual Environment (Recommended)

```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables (Optional)

```bash
# On Linux/Mac
export SECRET_KEY="your-secret-key-here"
export FLASK_DEBUG=False

# On Windows
set SECRET_KEY=your-secret-key-here
set FLASK_DEBUG=False
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

## 📖 Usage

### For Students/Users

1. Open the application in your browser
2. Use the search interface:
   - **Desktop**: Press `Ctrl + K` to open search modal
   - **Mobile**: Use the search bar at the bottom of the screen
3. Search by any combination of:
   - Class (BA, BSc, BCA, etc.)
   - Subject (Physics, Chemistry, Maths, etc.)
   - Year (2024, 2023, etc.)
   - Semester (1-6)
   - Exam Type (Main Semester, CIA, etc.)
   - Medium (English, Hindi, Hinglish)
4. Click on search results to download/view papers

### For Administrators

1. Navigate to `/admin` endpoint
2. Fill in the upload form with paper details:
   - Your name (uploader)
   - Class, Subject, Semester
   - Exam year and type
   - Medium of instruction
   - Time and max marks (optional)
3. Select PDF file
4. Click "Upload Paper"

### Special Commands

- Type `upload` in the search box for quick access to admin panel

## 🏗️ Project Structure

```
papers-gemini-archive-4-/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
├── LICENSE            # MIT License
├── README.md          # This file
├── templates/         # HTML templates
│   ├── index.html     # Main terminal UI
│   └── upload.html    # Upload form
├── static/            # Static assets
│   ├── style.css      # Stylesheet
│   └── script.js      # Frontend JavaScript
└── uploads/           # Uploaded PDF storage
    └── .gitkeep       # Keep directory in git
```

## 🔧 Configuration

### File Upload Limits

Edit in `app.py`:
```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

### Allowed File Types

Edit in `app.py`:
```python
ALLOWED_EXTENSIONS = {'pdf'}  # Add more if needed
```

## 🐛 Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed: `python --version`
- Check all dependencies are installed: `pip list`
- Verify you're in the correct directory
- Check if port 5000 is already in use

### Upload not working
- Verify file is a PDF
- Check file size is under 10MB
- Ensure all required fields are filled
- Check uploads directory exists and is writable

### Search returns no results
- Ensure papers are uploaded with correct metadata
- Check uploads folder has PDF files
- Verify filename format matches pattern

## 🛡️ Security Checklist for Production

- [ ] Set strong SECRET_KEY environment variable
- [ ] Disable debug mode (FLASK_DEBUG=False)
- [ ] Add authentication for /admin and /upload routes
- [ ] Implement rate limiting
- [ ] Set up HTTPS with valid SSL certificate
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Implement logging and monitoring
- [ ] Regular security updates for dependencies
- [ ] Add CAPTCHA for upload form
- [ ] Implement file scanning for malware
- [ ] Set up database for metadata (PostgreSQL/MySQL)
- [ ] Add backup system for uploaded files

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Anuj Meena**

## 🙏 Acknowledgments

- Terminal UI inspired by classic terminal interfaces
- Flask framework for Python web applications
- PyPDF2 for PDF manipulation

## 📊 Repository Stats

**Security Rating**: 7/10
- ✅ Input validation
- ✅ File upload security
- ✅ Security headers
- ✅ Error handling
- ⚠️ No authentication system
- ⚠️ No rate limiting
- ⚠️ Debug mode configurable

**Setup Difficulty**: 3/10 (Easy)
- Simple requirements
- Clear documentation
- No complex dependencies

**Code Quality**: 8/10
- Well-structured Flask app
- Proper error handling
- Secure coding practices
- Good separation of concerns

**UI/UX**: 8/10
- Unique terminal aesthetic
- Mobile responsive
- Intuitive search
- Clean design

**Technology Stack**: 7/10
- Modern Flask
- Client-side rendering
- PDF processing
- No database (limitation)

---

**⚠️ IMPORTANT**: This application requires a server to run. It **CANNOT** be deployed on GitHub Pages, Netlify, or other static hosting services. Use platforms like Heroku, Railway, DigitalOcean, or AWS that support Python applications.
