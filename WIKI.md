# 📚 Terminal Archives Wiki

Complete documentation for the Terminal Archives project - A secure, terminal-themed web application for archiving and searching previous year exam papers.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation & Setup](#installation--setup)
4. [Usage Guide](#usage-guide)
5. [Configuration](#configuration)
6. [Architecture](#architecture)
7. [API Documentation](#api-documentation)
8. [Security](#security)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)
11. [FAQ](#faq)
12. [Contributing](#contributing)
13. [Roadmap](#roadmap)

---

## Overview

### What is Terminal Archives?

Terminal Archives is a Flask-based web application designed to help students and educational institutions manage and search through a database of previous year exam papers. The application features a unique terminal-style interface that provides a nostalgic computing experience while delivering modern functionality.

### Key Highlights

- **🔒 Security First**: Built with security best practices including password hashing, rate limiting, and input sanitization
- **🎨 Unique UI**: Retro terminal aesthetic with modern responsiveness
- **⚡ Fast Search**: Client-side search for instant results
- **📱 Mobile Ready**: Fully responsive design for all devices
- **🔧 Easy Setup**: Simple installation with minimal dependencies
- **📦 No Database**: File-based storage for simplicity

### Who Should Use This?

- **Educational Institutions**: Schools, colleges, and universities wanting to archive exam papers
- **Student Organizations**: Student bodies managing resource libraries
- **Study Groups**: Collaborative learning communities
- **Individual Educators**: Teachers sharing resources with students

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | Flask | 3.0.0 |
| **Language** | Python | 3.8+ |
| **PDF Processing** | pypdf | 3.17.4 |
| **Rate Limiting** | Flask-Limiter | 3.5.0 |
| **Security** | Werkzeug | 3.0.1 |
| **Environment** | python-dotenv | 1.0.0 |
| **Frontend** | Vanilla JavaScript | ES6+ |
| **Styling** | Pure CSS | CSS3 |

---

## Features

### 1. Security Features (Rating: 8/10)

#### Authentication & Authorization
- **Password-Protected Admin Access**: Admin area secured with Werkzeug password hashing (PBKDF2-SHA256)
- **Session Management**: Secure cookies with HTTPOnly, Secure, and SameSite attributes
- **Login Rate Limiting**: Maximum 5 login attempts per minute to prevent brute force attacks

#### Input Validation & Sanitization
- **File Type Validation**: Strict PDF-only upload enforcement
- **File Size Limits**: Maximum 16MB per file to prevent resource exhaustion
- **Filename Sanitization**: Using Werkzeug's `secure_filename()` to prevent path traversal
- **Input Sanitization**: All user inputs are sanitized to prevent injection attacks
- **Path Traversal Prevention**: Secure path handling throughout the application

#### Rate Limiting
- **General Requests**: 200 per day, 50 per hour
- **Upload Endpoint**: 10 per hour (admin only)
- **Login Endpoint**: 5 per minute
- **API Endpoint**: 100 per minute
- **Customizable**: Can be configured via environment variables

#### Security Headers
- `X-Content-Type-Options: nosniff` - Prevents MIME type sniffing
- `X-Frame-Options: DENY` - Prevents clickjacking
- `X-XSS-Protection: 1; mode=block` - XSS protection
- `Strict-Transport-Security` - Forces HTTPS
- **Content Security Policy (CSP)** - Restricts resource loading

#### File Upload Security
- PDF-only validation at multiple levels
- Duplicate file detection
- Metadata sanitization
- Error handling with automatic cleanup
- Virus scanning ready (can be integrated)

### 2. User Experience Features (Rating: 9/10)

#### Terminal Interface
- **Retro Aesthetic**: Classic green-on-black terminal theme
- **Animated Loading**: Progress bars for operations
- **Command-Line Feel**: Search uses command-line style syntax
- **System Messages**: Informative boot sequence and system messages

#### Mobile Responsiveness & Device Detection
- **Robust Device Detection**: Advanced detection system identifies:
  - **Mobile OS**: Android, iOS (iPhone/iPad), Windows Phone
  - **Desktop OS**: Windows, macOS, Linux, Chrome OS
  - **Browser**: Chrome, Firefox, Safari, Edge, Internet Explorer
  - **Device Type**: Mobile, Tablet, Desktop
  - **Touch Support**: Detects touch-enabled devices
  - **Screen Size**: Adapts based on viewport width
- **Adaptive Search UI**:
  - **Mobile Devices**: Fixed search bar at bottom of screen
  - **Desktop**: Ctrl+K modal search overlay
  - **Automatic Switching**: Seamlessly adapts based on device
- **Mobile Search Bar**: Bottom-anchored search for mobile devices (Android, iOS, etc.)
- **Touch Optimized**: Touch-friendly interface elements
- **Desktop Search Modal**: Ctrl+K shortcut for desktop users (Windows, Mac, Linux)
- **Responsive Breakpoints**:
  - Mobile: ≤ 767px (search bar at bottom)
  - Tablet: 768px - 1023px (treated as mobile for search)
  - Desktop: ≥ 1024px (Ctrl+K modal)
  - Ultrawide: ≥ 1920px (optimized layout)

#### Search Functionality
- **Real-Time Search**: Client-side search for instant results
- **Multi-Field Search**: Searches across class, subject, year, exam type, and medium
- **Smart Filtering**: Case-insensitive matching
- **Quick Results Display**: Results appear as clickable links

#### Keyboard Shortcuts
- **Ctrl+K**: Open search modal (desktop only)
- **Escape**: Close search modal
- **Enter**: Execute search
- **Type "upload"**: Quick access to admin area

#### Design Elements
- **Dark Theme**: Easy on the eyes
- **Green Accents**: High contrast for readability
- **Fira Code Font**: Monospace font for authentic terminal feel
- **Clean Layout**: Minimal distractions, focus on content

### 3. Technical Features (Rating: 8/10)

#### PDF Processing
- **Metadata Embedding**: Automatically adds metadata to PDFs
- **Metadata Fields**:
  - Author (uploader name)
  - Title (class, subject, semester)
  - Subject
  - Keywords (class, year, semester, exam type, medium, time, marks)
- **PDF Validation**: Ensures files are valid PDFs before processing

#### File Management
- **Organized Storage**: Files stored with descriptive names
- **Naming Convention**: `{class}_{subject}_Sem{semester}_{year}_{exam_type}_{medium}.pdf`
- **Automatic Cleanup**: Failed uploads are automatically cleaned up
- **No Duplicates**: Existing files are detected

#### API Endpoints
- **RESTful API**: JSON API for paper listing
- **CORS Ready**: Can be configured for cross-origin requests
- **Rate Limited**: Protected against abuse

---

## Installation & Setup

### Prerequisites

Before installing Terminal Archives, ensure you have:

- **Python 3.8 or higher** installed
- **pip** (Python package manager)
- **Git** (optional, for cloning)
- **Virtual environment** (recommended)

Check your Python version:
```bash
python --version
# or
python3 --version
```

### Step 1: Get the Code

#### Option A: Clone with Git
```bash
git clone https://github.com/anacondy/papers-gemini-archive-4-.git
cd papers-gemini-archive-4-
```

#### Option B: Download ZIP
1. Go to https://github.com/anacondy/papers-gemini-archive-4-
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Open terminal/command prompt in the extracted folder

### Step 2: Create Virtual Environment (Recommended)

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0
- Werkzeug 3.0.1
- PyPDF2 3.0.1
- python-dotenv 1.0.0
- Flask-Limiter 3.5.0

### Step 4: Configure Environment

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file:**
   ```bash
   nano .env
   # or use any text editor
   ```

3. **Set these values:**
   ```env
   # Secret key for session management
   SECRET_KEY=your-very-long-random-secret-key-here
   
   # Admin password (will be hashed automatically)
   ADMIN_PASSWORD=your-strong-password-here
   
   # Debug mode (NEVER use True in production)
   DEBUG=False
   
   # Rate limit storage (optional)
   RATELIMIT_STORAGE_URL=memory://
   ```

4. **Generate a secure SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

### Step 5: Run the Application

```bash
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

### Step 6: Access the Application

Open your browser and navigate to:
- **Main Interface**: http://localhost:5000
- **Admin Login**: http://localhost:5000/admin/login

### Step 7: Upload Your First Paper

1. Go to http://localhost:5000/admin/login
2. Enter your admin password (from `.env` file)
3. Fill in the paper details
4. Upload a PDF file (max 16MB)
5. Click "Upload Paper"

---

## Usage Guide

### For Students: Searching Papers

#### Desktop Users

1. **Open Search**:
   - Press `Ctrl+K` anywhere on the page
   - OR click the search prompt that appears

2. **Enter Search Query**:
   - Type any keyword: class name, subject, year, etc.
   - Examples:
     - "Physics" - finds all Physics papers
     - "2024" - finds all papers from 2024
     - "BSc" - finds all BSc papers
     - "Physics 2024" - finds Physics papers from 2024

3. **View Results**:
   - Results appear instantly as you type
   - Click any result to download the PDF
   - Press `Escape` to close search

4. **Quick Admin Access**:
   - Type "upload" in search to access admin area

#### Mobile Users

1. **Use Search Bar**:
   - Search bar is at the bottom of the screen
   - Tap to focus and type your query
   - Press Enter to search

2. **View Results**:
   - Scroll through results
   - Tap any result to open/download PDF

### For Admins: Uploading Papers

#### Login Process

1. **Navigate to Admin Login**:
   - Go to http://localhost:5000/admin/login
   - OR type "upload" in search (you'll be asked for your name)

2. **Enter Password**:
   - Use the password from your `.env` file
   - If incorrect, you'll see an error message
   - Maximum 5 attempts per minute (rate limited)

3. **Access Upload Form**:
   - After successful login, you'll see the upload form

#### Upload Form Fields

| Field | Description | Required | Example |
|-------|-------------|----------|---------|
| **Your Name** | Name of uploader (embedded in PDF) | Yes | "Dr. John Smith" |
| **Class** | Class/Program name | Yes | "BSc", "BA", "MA" |
| **Subject** | Subject name | Yes | "Physics", "Mathematics" |
| **Semester** | Semester number | Yes | "I", "II", "III" |
| **Exam Year** | Year of examination | Yes | "2024", "2023" |
| **Exam Type** | Type of exam | Yes | "Regular", "Backpaper" |
| **Medium** | Language of paper | Yes | "English", "Hindi", "Hinglish" |
| **Time** | Duration of exam | No | "3 Hours", "180 Minutes" |
| **Max Marks** | Total marks | No | "100", "75" |
| **PDF File** | The exam paper PDF | Yes | Max 16MB |

#### Upload Process

1. **Fill all required fields** (marked with *)
2. **Select PDF file** (max 16MB)
3. **Click "Upload Paper"**
4. **Wait for confirmation**:
   - Success: You'll see a success message with filename
   - Error: You'll see an error message (e.g., "Invalid file type")

#### File Naming Convention

Files are automatically named using this format:
```
{Class}_{Subject}_Sem{Semester}_{Year}_{ExamType}_{Medium}.pdf
```

Example:
```
BSc_Physics_SemIII_2024_Regular_English.pdf
```

#### After Upload

- PDF is saved to `uploads/` directory
- Metadata is embedded in the PDF
- File appears in search results immediately
- You can upload another paper or return to home

### Logout

To logout from admin area:
- Go to http://localhost:5000/admin/logout
- OR close the browser/clear session

---

## Configuration

### Environment Variables

All configuration is done through `.env` file:

```env
# Required Variables
SECRET_KEY=your-secret-key-here
ADMIN_PASSWORD=your-password-here

# Optional Variables
DEBUG=False                           # Enable debug mode (development only)
RATELIMIT_STORAGE_URL=memory://      # Rate limit storage
```

### Customizing Rate Limits

Edit `app.py` to modify rate limits:

```python
# Default limits for all routes
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],  # Modify these
)

# Login endpoint
@app.route('/admin/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Modify this
def admin_login():
    # ...

# Upload endpoint
@app.route('/upload', methods=['POST'])
@limiter.limit("10 per hour")  # Modify this
def upload_file():
    # ...

# API endpoint
@app.route('/api/papers')
@limiter.limit("100 per minute")  # Modify this
def get_papers():
    # ...
```

### Customizing File Size Limit

Edit `app.py`:

```python
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB, modify as needed
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
```

### Customizing Upload Folder

Edit `app.py`:

```python
UPLOAD_FOLDER = 'uploads'  # Change to your preferred folder
```

### Customizing Theme

Edit `static/style.css`:

```css
:root {
    --primary-color: #4CAF50;    /* Main accent color (green) */
    --bg-color: #1a1a1a;         /* Background (dark) */
    --text-color: #e0e0e0;       /* Text color (light gray) */
    --secondary-color: #888;     /* Secondary text */
    --border-color: #333;        /* Borders */
}
```

### Adding More Subjects

Edit `templates/upload.html`:

```html
<select name="subject" required>
    <option value="">Select Subject</option>
    <option value="Physics">Physics</option>
    <option value="Chemistry">Chemistry</option>
    <option value="Mathematics">Mathematics</option>
    <!-- Add more subjects here -->
    <option value="Your Subject">Your Subject</option>
</select>
```

### Adding More Classes

Edit `templates/upload.html`:

```html
<select name="class" required>
    <option value="">Select Class</option>
    <option value="BA">BA</option>
    <option value="BSc">BSc</option>
    <!-- Add more classes here -->
    <option value="Your Class">Your Class</option>
</select>
```

---

## Architecture

### Application Structure

```
papers-gemini-archive-4-/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── README.md                  # Quick start guide
├── WIKI.md                    # This file
├── QUICKSTART.md              # Quick setup guide
├── SECURITY.md                # Security documentation
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                    # MIT License
├── static/                    # Static assets
│   ├── script.js             # Frontend JavaScript
│   └── style.css             # Stylesheets
├── templates/                 # Jinja2 templates
│   ├── index.html            # Main terminal interface
│   ├── upload.html           # Admin upload form
│   └── login.html            # Admin login page
├── uploads/                   # PDF storage (not in git)
└── docs/                      # GitHub Pages
    └── index.html            # Project landing page
```

### Application Flow

```
User Request
    ↓
Flask Application (app.py)
    ↓
Rate Limiter Check
    ↓
Route Handler
    ↓
Authentication Check (if admin route)
    ↓
Input Validation & Sanitization
    ↓
Business Logic
    ↓
Template Rendering / JSON Response
    ↓
Security Headers Added
    ↓
Response to User
```

### Data Flow for Upload

```
Admin Login
    ↓
Upload Form (templates/upload.html)
    ↓
POST /upload
    ↓
Validate Session
    ↓
Validate File Type & Size
    ↓
Sanitize Inputs
    ↓
Generate Filename
    ↓
Save PDF File
    ↓
Embed Metadata (PyPDF2)
    ↓
Success/Error Response
```

### Data Flow for Search

```
User Opens Page
    ↓
Load Terminal UI (templates/index.html)
    ↓
Fetch Papers (GET /api/papers)
    ↓
Store in JavaScript Variable
    ↓
User Types Search Query
    ↓
Client-Side Filter (static/script.js)
    ↓
Display Results
    ↓
User Clicks Result
    ↓
Download PDF (GET /uploads/<filename>)
```

### Security Layers

```
1. Rate Limiting (Flask-Limiter)
2. Authentication (Session-based)
3. Input Validation (Python functions)
4. File Validation (Type & Size checks)
5. Sanitization (secure_filename, custom sanitize)
6. Security Headers (CSP, HSTS, etc.)
7. Error Handling (Custom error pages)
```

---

## API Documentation

### GET /

**Description**: Main terminal interface

**Authentication**: None required

**Response**: HTML page

---

### GET /admin/login

**Description**: Admin login page

**Authentication**: None required

**Response**: HTML login form

---

### POST /admin/login

**Description**: Admin login authentication

**Authentication**: None required (password in form)

**Rate Limit**: 5 per minute

**Request Body**:
```
password=admin_password
```

**Response**:
- Success: Redirect to `/admin`
- Failure: Login page with error message

---

### GET /admin

**Description**: Admin upload form

**Authentication**: Required (session)

**Response**:
- If authenticated: HTML upload form
- If not authenticated: Redirect to `/admin/login`

---

### GET /admin/logout

**Description**: Admin logout

**Authentication**: None required

**Response**: Redirect to `/`

---

### POST /upload

**Description**: Upload a paper

**Authentication**: Required (session)

**Rate Limit**: 10 per hour

**Request Body** (multipart/form-data):
```
admin_name: string (required)
class: string (required)
subject: string (required)
semester: string (required)
exam_year: string (required)
exam_type: string (required)
medium: string (required)
time: string (optional)
max_marks: string (optional)
file: PDF file (required, max 16MB)
```

**Response**:
- Success: HTML success message with filename
- Error: HTML error message

**Error Conditions**:
- 400: No file uploaded
- 400: Invalid file type (not PDF)
- 400: File already exists
- 500: Error processing PDF

---

### GET /api/papers

**Description**: Get list of all papers

**Authentication**: None required

**Rate Limit**: 100 per minute

**Response**: JSON array

```json
[
  {
    "filename": "BSc_Physics_SemIII_2024_Regular_English.pdf",
    "url": "/uploads/BSc_Physics_SemIII_2024_Regular_English.pdf",
    "class": "BSc",
    "subject": "Physics",
    "semester": "III",
    "year": "2024",
    "exam_type": "Regular",
    "medium": "English",
    "original_name": "BSc Physics SemIII 2024 Regular English"
  }
]
```

---

### GET /uploads/<filename>

**Description**: Download a paper

**Authentication**: None required

**Response**: PDF file

**Error Conditions**:
- 404: File not found

---

### Error Handlers

#### 404 - Not Found
Returns custom HTML page

#### 413 - File Too Large
Returns HTML error page

#### 429 - Rate Limit Exceeded
Returns HTML error page with retry information

---

## Security

### Security Best Practices

For detailed security information, see [SECURITY.md](SECURITY.md).

#### Production Deployment

1. **Use HTTPS**: Always deploy with SSL/TLS
2. **Strong Passwords**: Use long, random passwords
3. **Environment Variables**: Never commit `.env` to git
4. **Regular Updates**: Keep dependencies updated
5. **Monitoring**: Monitor logs for suspicious activity
6. **Backups**: Regular backups of `uploads/` directory
7. **Firewall**: Use a firewall to restrict access
8. **Reverse Proxy**: Use nginx or Apache as reverse proxy

#### Security Checklist

- [ ] HTTPS enabled
- [ ] Strong admin password set
- [ ] `.env` file not in git
- [ ] Dependencies updated
- [ ] Rate limits configured
- [ ] Backups scheduled
- [ ] Logs monitored
- [ ] Firewall configured

### Known Security Limitations

1. **Single Admin Account**: Only one admin supported
2. **No 2FA**: Two-factor authentication not implemented
3. **No Audit Logging**: Security events not logged to files
4. **File System Storage**: Uses local files instead of database
5. **Client-Side Search**: All paper data visible to clients
6. **No Session Timeout**: Sessions persist until logout
7. **In-Memory Rate Limiting**: Resets on application restart

### Recommendations for Production

1. Implement multi-user authentication
2. Add two-factor authentication (TOTP)
3. Use database for persistence
4. Implement comprehensive audit logging
5. Add session timeout
6. Use Redis for persistent rate limiting
7. Implement CAPTCHA on login
8. Add intrusion detection
9. Regular security audits
10. Penetration testing

---

## Troubleshooting

### Installation Issues

#### "Module not found" error

**Problem**: Missing dependencies

**Solution**:
```bash
pip install -r requirements.txt
```

#### "Permission denied" error

**Problem**: No write permissions for uploads directory

**Solution**:
```bash
# Linux/Mac
chmod 755 uploads/

# Windows: Run terminal as administrator
```

#### "Python command not found"

**Problem**: Python not in PATH

**Solution**:
- **Windows**: Reinstall Python with "Add to PATH" option
- **Linux/Mac**: Use `python3` instead of `python`

### Runtime Issues

#### Port 5000 already in use

**Problem**: Another application using port 5000

**Solution 1**: Kill the process using port 5000
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Solution 2**: Change port in `app.py`
```python
app.run(debug=debug_mode, host='127.0.0.1', port=5001)
```

#### Can't access from other devices

**Problem**: App listening on localhost only

**Solution**: Change host to 0.0.0.0
```python
app.run(debug=debug_mode, host='0.0.0.0', port=5000)
```

Then access via: `http://YOUR_IP:5000`

#### Rate limit errors

**Problem**: Too many requests

**Solutions**:
1. Wait for cooldown period
2. Adjust rate limits in `app.py`
3. Use Redis for persistent storage

#### Session expires immediately

**Problem**: SESSION_COOKIE_SECURE requires HTTPS

**Solution**: For local development, comment out in `app.py`:
```python
# app.config['SESSION_COOKIE_SECURE'] = True  # Comment this for HTTP
```

### Upload Issues

#### "Invalid file type" error

**Problem**: File is not a PDF

**Solution**: Ensure file has `.pdf` extension and is a valid PDF

#### "File too large" error

**Problem**: File exceeds 16MB limit

**Solutions**:
1. Compress PDF
2. Increase limit in `app.py`

#### Upload succeeds but file not found

**Problem**: File permission issues

**Solution**:
```bash
ls -la uploads/
chmod 755 uploads/*
```

#### Metadata not embedded

**Problem**: PDF is corrupted or PyPDF2 error

**Solution**: Try a different PDF or check PDF validity

### Search Issues

#### No results found

**Problem**: Papers not loading or search query incorrect

**Solutions**:
1. Check browser console for errors (F12)
2. Verify `/api/papers` returns data
3. Check search query syntax

#### Search modal won't open

**Problem**: JavaScript error or browser compatibility

**Solutions**:
1. Check browser console (F12)
2. Try different browser
3. Clear browser cache

### Performance Issues

#### Slow page load

**Problem**: Too many papers or slow network

**Solutions**:
1. Enable gzip compression
2. Use CDN for static assets
3. Implement pagination

#### High memory usage

**Problem**: Many large PDFs

**Solutions**:
1. Compress PDFs
2. Increase server memory
3. Implement lazy loading

---

## Best Practices

### For Administrators

1. **Backup Regularly**
   ```bash
   tar -czf backup-$(date +%Y%m%d).tar.gz uploads/
   ```

2. **Monitor Logs**
   ```bash
   tail -f /var/log/syslog  # Linux
   ```

3. **Update Dependencies**
   ```bash
   pip list --outdated
   pip install --upgrade -r requirements.txt
   ```

4. **Check Security**
   ```bash
   pip install safety
   safety check
   ```

5. **Use Strong Passwords**
   - Minimum 16 characters
   - Mix of letters, numbers, symbols
   - Use password manager

6. **Enable HTTPS**
   - Use Let's Encrypt for free SSL
   - Configure reverse proxy

7. **Set Up Monitoring**
   - Use tools like Uptime Robot
   - Monitor disk space
   - Monitor application logs

### For Developers

1. **Use Virtual Environments**
   - Isolate dependencies
   - Avoid conflicts

2. **Follow PEP 8**
   - Use consistent code style
   - Add docstrings

3. **Test Changes**
   - Test locally before deploying
   - Test on multiple browsers

4. **Document Changes**
   - Update README and WIKI
   - Add code comments

5. **Version Control**
   - Commit often
   - Write clear commit messages

6. **Security First**
   - Never commit secrets
   - Validate all inputs
   - Use parameterized queries

### For Users

1. **Use Specific Searches**
   - "Physics 2024" instead of just "Physics"
   - Include semester and exam type

2. **Report Issues**
   - Open GitHub issues for bugs
   - Include error messages

3. **Provide Feedback**
   - Suggest improvements
   - Report usability issues

---

## FAQ

### General Questions

**Q: Is this project free to use?**
A: Yes, it's open source under MIT License.

**Q: Can I use this for commercial purposes?**
A: Yes, the MIT License allows commercial use.

**Q: Does it work on Windows/Mac/Linux?**
A: Yes, it works on all platforms with Python 3.8+.

**Q: Do I need a database?**
A: No, it uses file-based storage.

### Technical Questions

**Q: Can I change the admin password?**
A: Yes, edit the `ADMIN_PASSWORD` in `.env` file.

**Q: Can I have multiple admin users?**
A: Not currently. This is a planned feature.

**Q: Can I integrate this with my existing system?**
A: Yes, use the `/api/papers` endpoint for integration.

**Q: Is there a mobile app?**
A: No, but the web interface is mobile-responsive.

**Q: Can I customize the look?**
A: Yes, edit `static/style.css` for styling.

**Q: Does it support other file types?**
A: No, only PDFs are supported for security reasons.

### Security Questions

**Q: Is it secure for production?**
A: It has good security basics, but consider additional measures for sensitive data.

**Q: Is two-factor authentication supported?**
A: Not currently. This is a planned feature.

**Q: Are passwords encrypted?**
A: Yes, using Werkzeug's password hashing (PBKDF2-SHA256).

**Q: Is HTTPS required?**
A: Strongly recommended for production, especially if accessible over internet.

### Deployment Questions

**Q: Can I deploy on shared hosting?**
A: If they support Python and Flask, yes.

**Q: Can I use this on Heroku/AWS/Azure?**
A: Yes, it can be deployed on any platform supporting Flask.

**Q: How do I deploy to production?**
A: See the comprehensive [DEPLOYMENT.md](DEPLOYMENT.md) guide, which includes:
- Detailed PythonAnywhere deployment (free tier available)
- Heroku deployment
- Railway.app deployment
- DigitalOcean and AWS options
- File structure explanation
- Environment configuration
- Password setup instructions

**Q: How do I deploy to PythonAnywhere specifically?**
A: The [DEPLOYMENT.md](DEPLOYMENT.md) file now includes a complete step-by-step PythonAnywhere guide covering:
- Which files to upload
- What each file does
- How to set your admin password
- Virtual environment setup
- WSGI configuration
- Static files configuration
- Troubleshooting common issues

**Q: Can I use a CDN?**
A: Yes, you can serve static files from a CDN.

### Usage Questions

**Q: How many papers can I store?**
A: Limited only by disk space.

**Q: Can students upload papers?**
A: No, only admins can upload (by design).

**Q: Can I restrict downloads?**
A: Not currently, but you can add authentication for downloads.

**Q: How do I delete papers?**
A: Manually delete files from the `uploads/` directory.

---

## Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute

1. **Report Bugs**: Open issues on GitHub
2. **Suggest Features**: Share your ideas
3. **Improve Documentation**: Fix typos, add examples
4. **Submit Code**: Create pull requests
5. **Test**: Help test new features
6. **Spread the Word**: Share with others

### Contribution Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

### Coding Guidelines

- Follow PEP 8 for Python code
- Use 4 spaces for indentation
- Add docstrings to functions
- Write clear comments
- Test your changes

For detailed guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

### Priority Areas

**High Priority:**
- [ ] Unit tests
- [ ] Session timeout
- [ ] Audit logging
- [ ] Two-factor authentication
- [ ] Bulk upload

**Medium Priority:**
- [ ] PDF preview
- [ ] Advanced search filters
- [ ] Download statistics
- [ ] Admin dashboard
- [ ] Email notifications

**Low Priority:**
- [ ] Theme customization
- [ ] Multi-language support
- [ ] Export functionality
- [ ] Mobile app
- [ ] Browser extensions

---

## Roadmap

### Version 1.1 (Q1 2026)
- [ ] Multi-user admin support
- [ ] Role-based access control
- [ ] Session timeout
- [ ] Audit logging
- [ ] Unit tests

### Version 1.2 (Q2 2026)
- [ ] Two-factor authentication
- [ ] PDF preview in browser
- [ ] Advanced search filters
- [ ] Download analytics
- [ ] Bulk upload

### Version 1.3 (Q3 2026)
- [ ] Database integration (PostgreSQL/SQLite)
- [ ] Email notifications
- [ ] Tags and categories
- [ ] Paper versioning
- [ ] API documentation

### Version 2.0 (Q4 2026)
- [ ] Complete UI redesign
- [ ] Mobile apps (iOS/Android)
- [ ] Cloud storage integration
- [ ] Machine learning features
- [ ] GraphQL API

### Long-term Goals
- Multi-tenant support
- Internationalization
- Advanced analytics
- Integration with LMS systems
- AI-powered search and recommendations

---

## Additional Resources

### Documentation
- [README.md](README.md) - Quick start guide
- [QUICKSTART.md](QUICKSTART.md) - Fast setup instructions
- [SECURITY.md](SECURITY.md) - Security documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

### External Links
- [GitHub Repository](https://github.com/anacondy/papers-gemini-archive-4-)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)

### Support
- GitHub Issues: Report bugs and request features
- GitHub Discussions: Ask questions and share ideas
- Email: Contact maintainer via GitHub profile

### Community
- Share your deployment stories
- Showcase customizations
- Help other users
- Contribute to documentation

---

## Changelog

### Version 1.0.0 (Current)
- Initial release
- Terminal-style UI
- PDF upload and management
- Client-side search
- Admin authentication
- Rate limiting
- Security features
- Mobile responsive design

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

### MIT License Summary

**You can:**
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Use privately

**You must:**
- 📄 Include license and copyright notice

**You cannot:**
- ❌ Hold author liable

---

## Credits

### Author
**Anuj Meena** ([@anacondy](https://github.com/anacondy))

### Technologies Used
- Flask - Web framework
- PyPDF2 - PDF processing
- Werkzeug - Security utilities
- Flask-Limiter - Rate limiting
- Google Fonts (Fira Code) - Typography

### Inspiration
- Classic Unix terminals
- Retro computing aesthetic
- Modern web security practices

### Contributors
Thank you to all contributors who help improve this project!

---

## Acknowledgments

- Thanks to the Flask community for excellent documentation
- Thanks to all users providing feedback
- Thanks to contributors improving the codebase
- Thanks to students everywhere who inspired this project

---

**Made with ❤️ for students everywhere**

*Last Updated: October 14, 2025*
