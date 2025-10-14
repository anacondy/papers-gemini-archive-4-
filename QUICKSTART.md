# Quick Start Guide

Get the Papers Archive app running in under 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

## Installation Steps

### 1. Get the Code

**Option A: Clone from GitHub**
```bash
git clone https://github.com/anacondy/papers-gemini-archive-4-.git
cd papers-gemini-archive-4-
```

**Option B: Download ZIP**
- Download from GitHub
- Extract to a folder
- Open terminal in that folder

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask 3.0.0 (web framework)
- Werkzeug 3.0.1 (WSGI utilities)
- PyPDF2 3.0.1 (PDF processing)

### 3. Run the Application

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### 4. Open in Browser

Navigate to: `http://127.0.0.1:5000`

## Using the Application

### Search for Papers (Students)

**Desktop:**
1. Press `Ctrl + K` to open search
2. Type your query (e.g., "Physics 2024")
3. Press Enter
4. Click results to view/download

**Mobile:**
1. Use the search bar at the bottom
2. Type your query
3. Tap results to open

**Search Tips:**
- Search by subject: "Physics", "Chemistry"
- Search by year: "2024", "2023"
- Search by class: "BSc", "BCA"
- Combine terms: "BSc Physics 2024"

### Upload Papers (Admin)

1. Go to `http://127.0.0.1:5000/admin`
2. Fill in all required fields:
   - Your name
   - Class (BSc, BCA, etc.)
   - Subject
   - Semester (1-6)
   - Year (2024, 2023, etc.)
   - Exam Type
   - Medium (English/Hindi/Hinglish)
3. Optional: Add time and max marks
4. Select PDF file
5. Click "Upload Paper"

**Quick Access:** Type "upload" in the search box

## Configuration (Optional)

### Change Secret Key

```bash
export SECRET_KEY="your-secret-random-key-here"
```

### Enable Debug Mode (Development Only)

```bash
export FLASK_DEBUG=True
```

**⚠️ NEVER enable debug in production!**

### Change Port

Edit `app.py`, line 174:
```python
app.run(debug=debug_mode, host='127.0.0.1', port=YOUR_PORT)
```

## Troubleshooting

### "Command not found: python"

Try `python3` instead:
```bash
python3 app.py
```

### "No module named 'flask'"

Dependencies not installed. Run:
```bash
pip install -r requirements.txt
```

If using Python 3:
```bash
pip3 install -r requirements.txt
```

### "Address already in use"

Port 5000 is busy. Either:
- Stop the other application using port 5000
- Change the port in `app.py`

### "Permission denied" on uploads

Check folder permissions:
```bash
chmod 755 uploads/
```

### No papers showing up

1. Upload at least one paper via `/admin`
2. Check uploads folder has files
3. Check browser console for errors (F12)

## Testing the Application

### Test Search Functionality

1. Upload a test PDF via admin
2. Search for it using any metadata
3. Verify it appears in results
4. Click to download/view

### Test Upload Validation

Try uploading:
- ❌ Non-PDF file (should reject)
- ❌ File > 10MB (should reject)
- ❌ Empty form (should reject)
- ✅ Valid PDF with all fields (should accept)

## Stopping the Application

Press `Ctrl + C` in the terminal

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [SECURITY.md](SECURITY.md) for security info
- See [DEPLOYMENT.md](DEPLOYMENT.md) for hosting options
- Review [ANALYSIS.md](ANALYSIS.md) for detailed assessment

## Need Help?

1. Check the documentation files
2. Look for error messages in terminal
3. Open browser console (F12) for frontend errors
4. Check `uploads/` folder exists and is writable

## Development Mode

For development with auto-reload:

```bash
export FLASK_DEBUG=True
flask run
```

Changes to Python files will auto-restart the server.

## Production Deployment

**DO NOT** use `python app.py` in production!

Use a production server:
```bash
pip install gunicorn
gunicorn app:app
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for full production setup.

---

**Enjoy using Papers Archive! 📚**
