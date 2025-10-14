# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     User's Browser                      │
│  ┌───────────────────────────────────────────────────┐  │
│  │         Frontend (HTML/CSS/JavaScript)           │  │
│  │  • Terminal UI Animation                         │  │
│  │  • Search Interface (Ctrl+K / Mobile Bar)        │  │
│  │  • Device Info Display                           │  │
│  │  • Upload Form                                   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                           ▼ HTTP Requests
┌─────────────────────────────────────────────────────────┐
│               Flask Application Server                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Security Middleware                 │  │
│  │  • HTTP Security Headers (CSP, HSTS, etc.)      │  │
│  │  • Content-Type Protection                      │  │
│  │  • XSS Protection                               │  │
│  └───────────────────────────────────────────────────┘  │
│                           ▼                             │
│  ┌───────────────────────────────────────────────────┐  │
│  │                Routes/Endpoints                  │  │
│  │  • GET  /          → Terminal UI                │  │
│  │  • GET  /admin     → Upload Form                │  │
│  │  • POST /upload    → File Upload Handler        │  │
│  │  • GET  /api/papers → Papers List API           │  │
│  │  • GET  /uploads/<file> → File Download         │  │
│  └───────────────────────────────────────────────────┘  │
│                           ▼                             │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Business Logic                      │  │
│  │  • Input Validation & Sanitization              │  │
│  │  • File Type Checking (PDF only)                │  │
│  │  • Size Limit Enforcement (10MB)                │  │
│  │  • Path Traversal Prevention                    │  │
│  │  • Filename Generation                          │  │
│  └───────────────────────────────────────────────────┘  │
│                           ▼                             │
│  ┌───────────────────────────────────────────────────┐  │
│  │              PDF Processing                      │  │
│  │  • PyPDF2 Integration                           │  │
│  │  • Metadata Embedding                           │  │
│  │  • File Integrity                               │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  File System Storage                    │
│  uploads/                                               │
│  ├── [BSc]_[Physics]_[Sem-3]_[2024]_[...].pdf         │
│  ├── [BCA]_[Maths]_[Sem-1]_[2023]_[...].pdf           │
│  └── [...]                                              │
└─────────────────────────────────────────────────────────┘
```

## Component Breakdown

### Frontend Layer
**Files**: `templates/*.html`, `static/*.css`, `static/*.js`

**Responsibilities**:
- Display terminal-style UI
- Handle user interactions
- Search functionality
- Upload form interface
- Mobile responsiveness

**Technology**: Vanilla JavaScript, CSS3, HTML5

### Application Layer
**File**: `app.py`

**Responsibilities**:
- Route handling
- Request processing
- Security enforcement
- Business logic
- Error handling

**Technology**: Flask 3.0, Python 3.8+

### Storage Layer
**Directory**: `uploads/`

**Responsibilities**:
- PDF file storage
- Metadata in filenames
- File serving

**Technology**: File system (no database)

## Data Flow

### Upload Flow
```
1. User fills form → /admin
2. User clicks "Upload Paper"
3. POST /upload with multipart/form-data
   ├── Validate required fields
   ├── Check file type (PDF only)
   ├── Check file size (<10MB)
   ├── Sanitize inputs
   ├── Generate secure filename
   ├── Save to uploads/
   ├── Embed metadata in PDF
   └── Return success page
```

### Search Flow
```
1. User types query (Ctrl+K or mobile bar)
2. JavaScript triggers search
3. Fetch GET /api/papers
4. Backend lists uploads/ directory
   ├── Match filename pattern with regex
   ├── Extract metadata from filename
   ├── Build JSON response
5. JavaScript filters results
6. Display clickable links
```

### Download Flow
```
1. User clicks paper link
2. GET /uploads/<filename>
3. Backend validates filename
   ├── Check path traversal
   ├── Verify file exists
   ├── Validate extension
4. Send file to browser
5. Browser displays/downloads PDF
```

## Security Layers

### Layer 1: Input Validation
```python
def sanitize(text):
    # Remove harmful characters
    return "".join(c for c in text if c.isalnum() or c in (' ', '_', '-'))

def validate_filename(filename):
    # Prevent path traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
```

### Layer 2: File Upload Protection
```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

### Layer 3: HTTP Security Headers
```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "..."
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # ... more headers
```

### Layer 4: Path Validation
```python
# Ensure file stays in uploads directory
if not os.path.abspath(filepath).startswith(
    os.path.abspath(app.config['UPLOAD_FOLDER'])):
    abort(400)
```

## Filename Convention

Papers are stored with metadata-rich filenames:

```
Format:
[Class]_[Subject]_[Sem-X]_[Year]_[ExamType]_[Medium]_[Uploader]_[OriginalName].pdf

Example:
[BSc]_[Physics]_[Sem-3]_[2024]_[MainSemester]_[EnglishMedium]_[Alvido]_[sample.pdf
```

This allows:
- Easy parsing with regex
- No database needed for basic metadata
- Searchable via filesystem
- Clear organization

## Search Algorithm

```javascript
const results = livePapersDB.filter(paper => {
    const fullText = `${paper.class} ${paper.subject} ${paper.year} 
                      ${paper.original_name} ${paper.exam_type} ${paper.medium}`;
    return fullText.toLowerCase().includes(query.toLowerCase());
});
```

**Properties**:
- Client-side filtering (fast)
- Case-insensitive
- Partial matching
- Multiple field search
- Real-time results

## Configuration Management

### Development
```python
# app.py
debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
app.run(debug=debug_mode, host='127.0.0.1', port=5000)
```

### Production
```python
# Use config.py
from config import config
app.config.from_object(config['production'])

# Deploy with Gunicorn
# gunicorn app:app
```

## Deployment Architecture

### Local Development
```
Developer's Machine
├── Python 3.8+
├── pip install -r requirements.txt
└── python app.py
```

### Production (Heroku)
```
Heroku Platform
├── Dyno (container)
│   ├── Python runtime
│   ├── gunicorn (WSGI server)
│   └── Flask app
├── Environment variables
│   ├── SECRET_KEY
│   └── FLASK_DEBUG=False
└── Ephemeral filesystem
    └── uploads/ (cleared on restart!)
```

**Note**: Heroku filesystem is ephemeral. For production, use:
- AWS S3 for file storage
- PostgreSQL for metadata
- Redis for caching

## Scalability Considerations

### Current Limitations
1. **File System Storage**: Limited by disk space
2. **No Database**: Hard to scale search
3. **No Caching**: Repeated requests recalculate
4. **Single Server**: No horizontal scaling

### Recommended Improvements
```
┌─────────────────────────────────────────┐
│         Load Balancer (Nginx)          │
└─────────────────────────────────────────┘
              ▼         ▼         ▼
    ┌─────────┐   ┌─────────┐   ┌─────────┐
    │ Flask 1 │   │ Flask 2 │   │ Flask 3 │
    └─────────┘   └─────────┘   └─────────┘
         ▼              ▼              ▼
    ┌─────────────────────────────────────┐
    │        PostgreSQL Database          │
    │  • User accounts                    │
    │  • Paper metadata                   │
    │  • Search indexes                   │
    └─────────────────────────────────────┘
                      ▼
    ┌─────────────────────────────────────┐
    │       Cloud Storage (AWS S3)        │
    │  • PDF files                        │
    │  • Scalable storage                 │
    │  • CDN distribution                 │
    └─────────────────────────────────────┘
```

## API Documentation

### GET /
Returns terminal UI page

**Response**: HTML page

### GET /admin
Returns upload form

**Response**: HTML page

### POST /upload
Handles file upload

**Parameters** (multipart/form-data):
- `file`: PDF file (required)
- `admin_name`: Uploader name (required)
- `class`: Class name (required)
- `subject`: Subject name (required)
- `semester`: Semester number (required)
- `exam_year`: Year (required)
- `exam_type`: Type of exam (required)
- `medium`: Language (required)
- `time`: Duration (optional)
- `max_marks`: Maximum marks (optional)

**Response**: HTML success/error page

### GET /api/papers
Lists all papers

**Response** (JSON):
```json
[
    {
        "class": "BSc",
        "subject": "Physics",
        "semester": "3",
        "year": "2024",
        "exam_type": "Main Semester",
        "medium": "English Medium",
        "uploader": "Alvido",
        "original_name": "sample.pdf",
        "url": "/uploads/[BSc]_[Physics]_..."
    }
]
```

### GET /uploads/<filename>
Downloads specific paper

**Response**: PDF file

## Error Handling

```python
try:
    # Upload logic
except Exception as e:
    print(f"Error: {e}")  # Log to console
    return "Safe error message", 500  # No stack trace to user
```

**Error Types**:
- 400: Bad Request (invalid input)
- 404: Not Found (file doesn't exist)
- 500: Server Error (processing failed)

All errors return user-friendly messages without exposing system details.

## Future Architecture

For production scale:

```
Users → CDN → Load Balancer → Flask Servers → PostgreSQL
                                     ↓
                                  Redis Cache
                                     ↓
                               AWS S3 Storage
```

**Benefits**:
- Horizontal scaling
- Fast search with database indexes
- Caching for performance
- Distributed file storage
- High availability

---

**Current Architecture**: Simple, effective, easy to understand
**Recommended for**: Small-medium scale, learning, portfolios
**Production Ready**: With authentication and rate limiting added
