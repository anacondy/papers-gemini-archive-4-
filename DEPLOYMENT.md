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

### Option 3: PythonAnywhere (Free Tier Available)

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your code or pull from GitHub
3. Create a virtual environment
4. Configure WSGI file
5. Set your app to run

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
