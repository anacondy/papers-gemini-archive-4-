# Deployment Guide

## Why This Cannot Run on GitHub Pages

GitHub Pages is designed for **static websites only**. It can serve:
- HTML files
- CSS files
- JavaScript files
- Images and other assets

**This application requires:**
- Python runtime environment
- Flask web server
- File system access for uploads
- Server-side processing for file uploads
- Backend API endpoints

Therefore, **GitHub Pages is not suitable** for this application.

## Recommended Deployment Options

### Option 1: Heroku (Free Tier Available)

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
3. Add gunicorn to requirements.txt:
   ```
   gunicorn==21.2.0
   ```
4. Deploy:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

### Option 2: Railway.app (Free Tier Available)

1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway auto-detects Flask apps
4. Set environment variables in dashboard
5. Deploy automatically

### Option 3: PythonAnywhere (Free Tier Available) - Detailed Guide

PythonAnywhere is an excellent choice for beginners and offers a free tier perfect for this application.

#### Step-by-Step PythonAnywhere Deployment

##### 1. Sign Up and Initial Setup

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com) and create a free account
2. Once logged in, go to the **Dashboard**

##### 2. Upload Your Files

You have two options:

**Option A: Using Git (Recommended)**

1. Open a **Bash console** from the dashboard
2. Clone your repository:
   ```bash
   git clone https://github.com/your-username/papers-gemini-archive-4-.git
   cd papers-gemini-archive-4-
   ```

**Option B: Manual Upload**

1. Go to the **Files** tab
2. Create a new directory (e.g., `papers-archive`)
3. Upload these essential files:
   - `app.py` - Main Flask application
   - `requirements.txt` - Python dependencies
   - `templates/` folder - All HTML templates (index.html, upload.html, login.html)
   - `static/` folder - CSS and JavaScript files (style.css, script.js)
   - `.env` - Environment configuration (create from .env.example)

##### 3. File Structure Explanation

Here's what each file does:

| File/Folder | Purpose | Required? |
|------------|---------|-----------|
| `app.py` | Main Flask application with all routes and logic | ✅ Required |
| `requirements.txt` | Lists all Python packages needed | ✅ Required |
| `templates/` | HTML templates for web pages | ✅ Required |
| `static/` | CSS, JavaScript, and other static assets | ✅ Required |
| `.env` | Configuration (SECRET_KEY, ADMIN_PASSWORD, etc.) | ✅ Required |
| `uploads/` | Folder where PDF files are stored | Auto-created |
| `config.py` | Configuration classes (optional) | ⚠️ Optional |
| `Procfile` | For Heroku deployment | ❌ Not needed for PythonAnywhere |
| `runtime.txt` | Python version specification | ❌ Not needed for PythonAnywhere |
| `tests/` | Test files | ❌ Not needed for deployment |
| `*.md` files | Documentation | ❌ Not needed for deployment |

##### 4. Create Virtual Environment

In the Bash console:

```bash
cd papers-gemini-archive-4-  # or your directory name
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

##### 5. Configure Environment Variables

**Create `.env` file** in your project directory:

```bash
nano .env
```

Add your configuration:

```env
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-secret-random-key-here-change-this-to-something-random
DEBUG=False

# Admin Authentication - SET YOUR DESIRED PASSWORD HERE
ADMIN_PASSWORD=YourStrongPasswordHere123!

# Upload Configuration
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads

# Rate Limiting
RATELIMIT_ENABLED=True
RATELIMIT_STORAGE_URL=memory://
```

**🔑 Important**: Replace `YourStrongPasswordHere123!` with your desired admin password!

**How to generate a strong SECRET_KEY**:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Save the file (Ctrl+X, then Y, then Enter in nano).

##### 6. Create WSGI Configuration File

1. Go to the **Web** tab in PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration** (not the "Flask" option)
4. Select **Python 3.10** (or latest available)
5. Click through to create the app

##### 7. Configure WSGI File

1. In the **Web** tab, click on the **WSGI configuration file** link
2. Replace the entire content with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/papers-gemini-archive-4-'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set up environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import Flask app
from app import app as application
```

**Replace `yourusername`** with your actual PythonAnywhere username!

##### 8. Configure Static Files

Still in the **Web** tab, scroll to **Static files** section:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/papers-gemini-archive-4-/static` |
| `/uploads/` | `/home/yourusername/papers-gemini-archive-4-/uploads` |

Replace `yourusername` with your actual username.

##### 9. Create Uploads Directory

In the Bash console:

```bash
cd papers-gemini-archive-4-
mkdir -p uploads
chmod 755 uploads
```

##### 10. Set Virtualenv

In the **Web** tab, find **Virtualenv** section:

1. Click the link to enter virtualenv path
2. Enter: `/home/yourusername/papers-gemini-archive-4-/venv`
3. Replace `yourusername` with your actual username

##### 11. Reload and Test

1. Click the big green **Reload** button at the top of the Web tab
2. Visit your site: `yourusername.pythonanywhere.com`
3. Test the terminal interface
4. Navigate to `/admin/login` and use your configured password

##### 12. Setting/Changing Admin Password Later

To change your admin password after deployment:

1. Open Bash console
2. Edit the `.env` file:
   ```bash
   cd papers-gemini-archive-4-
   nano .env
   ```
3. Change the `ADMIN_PASSWORD` line:
   ```env
   ADMIN_PASSWORD=YourNewPasswordHere
   ```
4. Save and exit (Ctrl+X, Y, Enter)
5. Go to **Web** tab and click **Reload**

**Note**: The password is hashed when the application starts, so you set it as plain text in `.env` and Flask will hash it automatically.

##### 13. Troubleshooting PythonAnywhere

**Problem: Site shows "Something went wrong"**
- Check the **Error log** in the Web tab
- Common issues:
  - Wrong virtualenv path
  - Missing dependencies: `pip install -r requirements.txt`
  - Wrong project path in WSGI file

**Problem: Can't login as admin**
- Verify `.env` file has `ADMIN_PASSWORD` set
- Check that `.env` is in the same directory as `app.py`
- Make sure `python-dotenv` is installed: `pip install python-dotenv`

**Problem: Upload folder not writable**
- Run: `chmod 755 uploads` in your project directory
- Verify the uploads folder exists

**Problem: Static files not loading**
- Check static files configuration in Web tab
- Ensure paths are absolute: `/home/yourusername/...`
- Click Reload after changing configuration

##### 14. Updating Your Deployment

When you make changes to your code:

**If using Git:**
```bash
cd papers-gemini-archive-4-
git pull origin main
source venv/bin/activate
pip install -r requirements.txt  # If dependencies changed
```

**If manual upload:**
- Upload changed files through Files tab

**Always reload:**
- Go to Web tab → Click **Reload**

##### 15. Free Tier Limitations

PythonAnywhere free tier includes:
- ✅ 512MB disk space (plenty for this app)
- ✅ One web app (yourusername.pythonanywhere.com)
- ✅ Python 3.x support
- ⚠️ Limited to HTTP (not HTTPS) on free domain
- ⚠️ CPU time limits (100 seconds/day for scripts)
- ⚠️ Whitelisted sites only for external API calls

##### 16. Upgrading for Production

For serious production use, consider:
- 💰 **Paid PythonAnywhere account** ($5-$50/month) for:
  - Custom domain support
  - HTTPS/SSL certificates
  - More CPU and storage
  - SSH access
  - Always-on tasks
- Or migrate to AWS, DigitalOcean, etc. for more control

### Option 4: DigitalOcean App Platform

1. Create account on DigitalOcean
2. Connect GitHub repository
3. Configure build settings
4. Set environment variables
5. Deploy

### Option 5: AWS EC2 (More Control, Paid)

1. Launch EC2 instance
2. Install Python and dependencies
3. Set up Nginx + Gunicorn
4. Configure security groups
5. Set up SSL certificate

## Production Deployment Checklist

Before deploying to production:

- [ ] Set strong SECRET_KEY
- [ ] Disable debug mode
- [ ] Add authentication system
- [ ] Set up database (PostgreSQL recommended)
- [ ] Configure HTTPS/SSL
- [ ] Set up logging
- [ ] Implement backup system
- [ ] Add monitoring (Sentry, New Relic, etc.)
- [ ] Configure rate limiting
- [ ] Set up CDN for static files
- [ ] Test all security measures
- [ ] Update dependencies
- [ ] Document API endpoints

## Static Alternative

If you **must** use GitHub Pages, you would need to:

1. Remove all server-side functionality
2. Convert to pure JavaScript application
3. Use a third-party backend service (Firebase, Supabase, etc.)
4. Store files in cloud storage (AWS S3, Cloudinary, etc.)
5. Completely rewrite the upload and search functionality

This would essentially be building a different application.

## For Development/Testing Only

To quickly test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

**Never deploy with `debug=True` or without authentication in production!**
