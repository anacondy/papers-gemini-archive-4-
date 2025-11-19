# PythonAnywhere Deployment - Quick Guide

This guide explains exactly what files you need to upload to PythonAnywhere to get your application live.

## 📋 Required Files Checklist

### Essential Files (Must Upload)

| File/Folder | Purpose | Critical? |
|------------|---------|-----------|
| ✅ `app.py` | Main Flask application with all routes | **REQUIRED** |
| ✅ `requirements.txt` | Python package dependencies | **REQUIRED** |
| ✅ `templates/` folder | All HTML templates | **REQUIRED** |
| ├─ `index.html` | Main terminal interface page | **REQUIRED** |
| ├─ `upload.html` | Admin upload form | **REQUIRED** |
| └─ `login.html` | Admin login page | **REQUIRED** |
| ✅ `static/` folder | CSS, JavaScript, and assets | **REQUIRED** |
| ├─ `style.css` | Stylesheet | **REQUIRED** |
| └─ `script.js` | JavaScript functionality | **REQUIRED** |
| ✅ `.env` | Configuration (SECRET_KEY, passwords) | **REQUIRED** |

### Optional Files (Not Needed for Deployment)

| File/Folder | Needed? | Reason |
|------------|---------|--------|
| ❌ `Procfile` | No | Only for Heroku |
| ❌ `runtime.txt` | No | Only for Heroku |
| ❌ `tests/` | No | Testing only |
| ❌ `*.md` files | No | Documentation |
| ❌ `.git/` | No | Version control |
| ❌ `.github/` | No | GitHub Actions |
| ❌ `config.py` | No | Optional configuration |
| 📁 `uploads/` | Auto-created | Created automatically by app |

## 🚀 Quick Deployment Steps

### Step 1: Upload Files to PythonAnywhere

**Option A: Using Git (Recommended)**
```bash
# In PythonAnywhere Bash console:
git clone https://github.com/your-username/papers-gemini-archive-4-.git
cd papers-gemini-archive-4-
```

**Option B: Manual Upload**
1. Go to **Files** tab on PythonAnywhere
2. Create directory: `papers-archive`
3. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `templates/` folder (with all 3 HTML files)
   - `static/` folder (with CSS and JS)
   - Create `.env` file (see below)

### Step 2: Create `.env` File

In your project directory, create `.env` with:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-random-key-here
DEBUG=False

# Admin Password - CHANGE THIS!
ADMIN_PASSWORD=YourStrongPasswordHere123!

# Upload Configuration
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads

# Rate Limiting
RATELIMIT_ENABLED=True
RATELIMIT_STORAGE_URL=memory://
```

**Generate a secure SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Step 3: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 4: Configure Web App

1. Go to **Web** tab → **Add a new web app**
2. Choose **Manual configuration**
3. Select **Python 3.10** (or latest)

### Step 5: Edit WSGI Configuration

Click on **WSGI configuration file** link and replace content with:

```python
import sys
import os

# CHANGE 'yourusername' to your actual PythonAnywhere username!
project_home = '/home/yourusername/papers-gemini-archive-4-'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import Flask app
from app import app as application
```

**⚠️ Important:** Replace `yourusername` with your actual PythonAnywhere username!

### Step 6: Configure Static Files

In the **Web** tab, scroll to **Static files** section and add:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/papers-gemini-archive-4-/static` |
| `/uploads/` | `/home/yourusername/papers-gemini-archive-4-/uploads` |

### Step 7: Set Virtual Environment

In **Virtualenv** section, enter:
```
/home/yourusername/papers-gemini-archive-4-/venv
```

### Step 8: Create Uploads Directory

```bash
cd papers-gemini-archive-4-
mkdir -p uploads
chmod 755 uploads
```

### Step 9: Reload and Go Live! 🎉

1. Click the big green **Reload** button
2. Visit: `yourusername.pythonanywhere.com`
3. Test the terminal interface
4. Login at: `yourusername.pythonanywhere.com/admin/login`

## ✅ Verification Checklist

After deployment, verify:

- [ ] Homepage loads correctly
- [ ] Terminal interface displays
- [ ] Search functionality works (mobile and desktop)
- [ ] Can access `/admin/login`
- [ ] Can login with configured password
- [ ] Upload page loads after login
- [ ] Can upload a PDF file
- [ ] Uploaded files appear in search results

## 🔧 Common Issues & Fixes

### "Something went wrong"
- Check **Error log** in Web tab
- Verify all paths in WSGI file use your actual username
- Ensure `.env` file exists in project root

### Can't login
- Verify `ADMIN_PASSWORD` is set in `.env`
- Check `.env` is in same directory as `app.py`
- Reload the web app after changing `.env`

### Static files not loading
- Verify static files paths in Web tab use absolute paths
- Ensure paths include your username
- Click Reload after configuration changes

### Upload errors
- Run: `chmod 755 uploads` in project directory
- Verify uploads folder exists
- Check file size is under 16MB

## 📊 File Size Summary

Approximate sizes of required files:
- `app.py`: ~12 KB
- `requirements.txt`: ~1 KB
- `templates/`: ~10 KB total
- `static/`: ~15 KB total
- `.env`: ~0.5 KB

**Total**: Less than 40 KB (excluding uploaded PDFs)

PythonAnywhere free tier provides **512 MB** disk space, which is plenty for this application!

## 🔄 Updating Your Deployed App

When you make changes:

```bash
# If using Git:
cd papers-gemini-archive-4-
git pull origin main
source venv/bin/activate
pip install -r requirements.txt  # Only if dependencies changed

# Then always:
# Go to Web tab → Click "Reload"
```

## 💡 Pro Tips

1. **Backup**: Regularly download your `uploads/` folder
2. **Security**: Use a strong admin password
3. **Monitoring**: Check Error logs regularly
4. **Updates**: Keep dependencies updated with `pip list --outdated`

## 📱 Mobile Search Bar Feature

This application includes a **fixed search bar** specifically for smartphones:
- Automatically detects mobile devices
- Shows fixed search bar at bottom of screen
- Desktop users still use Ctrl+K for search modal
- Works on all mobile browsers without keyboard issues

## 🎯 What's Next?

After successful deployment:
- Share your site: `yourusername.pythonanywhere.com`
- Start uploading papers via admin panel
- Students can search and download papers
- Monitor usage in PythonAnywhere dashboard

## 🆘 Need Help?

- **PythonAnywhere Help**: [help.pythonanywhere.com](https://help.pythonanywhere.com)
- **GitHub Issues**: Create an issue in the repository
- **Documentation**: Read full [DEPLOYMENT.md](DEPLOYMENT.md) for advanced options

---

**Ready to deploy?** Start with Step 1 above! 🚀
