# Quick Start Guide

Get up and running with Terminal Archives in 5 minutes!

## Prerequisites
- Python 3.8+ installed
- pip (Python package manager)
- Git (optional, for cloning)

## Installation Steps

### 1. Get the Code
```bash
# Option A: Clone with Git
git clone https://github.com/anacondy/papers-gemini-archive-4-.git
cd papers-gemini-archive-4-

# Option B: Download ZIP
# Download from GitHub and extract
# cd into the extracted folder
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and set your admin password
# On Linux/Mac:
nano .env
# Or use any text editor

# Set these values:
SECRET_KEY=your-very-long-random-secret-key-change-this
ADMIN_PASSWORD=your-strong-password-here
DEBUG=False
```

**Generate a secure SECRET_KEY**:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access the Application
Open your browser and navigate to:
- **Main Page**: http://localhost:5000
- **Admin Login**: http://localhost:5000/admin/login

## First Time Setup

### Upload Your First Paper

1. Go to http://localhost:5000/admin/login
2. Enter the admin password you set in `.env`
3. Fill in the paper details:
   - Your name
   - Class (e.g., BSc)
   - Subject (e.g., Physics)
   - Semester
   - Year
   - Exam type
   - Medium
4. Upload a PDF file (max 16MB)
5. Click "Upload Paper"

### Search for Papers

**Desktop**:
- Press `Ctrl+K` to open search
- Type your query (e.g., "Physics 2024")
- Press Enter

**Mobile**:
- Use the search bar at the bottom
- Type and press Enter

## Common Issues & Solutions

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Permission denied" when uploading
```bash
# Linux/Mac
chmod 755 uploads/

# Windows: Run as administrator
```

### Port 5000 already in use
Change the port in `app.py`:
```python
app.run(debug=debug_mode, host='127.0.0.1', port=5001)
```

### Can't access from other devices
Change the host:
```python
app.run(debug=debug_mode, host='0.0.0.0', port=5000)
```
Then access via: `http://YOUR_IP:5000`

## Production Deployment

### Quick Production Setup
```bash
# Install Gunicorn
pip install gunicorn

# Set environment variables
export SECRET_KEY="your-secret-key"
export ADMIN_PASSWORD="your-password"
export DEBUG=False
export FLASK_ENV=production

# Run with Gunicorn (4 workers)
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Using systemd (Linux)
Create `/etc/systemd/system/papers-archive.service`:
```ini
[Unit]
Description=Terminal Archives
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/papers-gemini-archive-4-
Environment="PATH=/path/to/venv/bin"
EnvironmentFile=/path/to/papers-gemini-archive-4-/.env
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable papers-archive
sudo systemctl start papers-archive
```

## Tips & Tricks

### Keyboard Shortcuts
- `Ctrl+K`: Open search (desktop)
- Type `upload` in search: Quick admin access

### Backup Your Data
```bash
# Backup uploaded files
tar -czf backup-$(date +%Y%m%d).tar.gz uploads/

# Or use rsync
rsync -av uploads/ /path/to/backup/
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Check for Security Issues
```bash
pip install safety
safety check
```

## Next Steps

- 📖 Read the full [README.md](README.md)
- 🔒 Review [SECURITY.md](SECURITY.md)
- 📊 Check [SECURITY_AUDIT_REPORT.md](SECURITY_AUDIT_REPORT.md)
- 🎨 Customize the theme in `static/style.css`
- 📝 Add more subjects in `templates/upload.html`

## Need Help?

- Check the [README](README.md) for detailed documentation
- Open an issue on GitHub
- Review the [SECURITY_AUDIT_REPORT.md](SECURITY_AUDIT_REPORT.md)

---

Made with ❤️ by Anuj Meena
