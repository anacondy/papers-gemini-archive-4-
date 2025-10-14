# Security Policy

## Supported Versions

Currently supported versions of this project:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Security Features

This application implements several security measures:

### Authentication & Authorization
- Password-protected admin access using Werkzeug password hashing
- Session management with secure cookies (HTTPOnly, Secure, SameSite)
- Login rate limiting (5 attempts per minute)

### Input Validation & Sanitization
- All user inputs are sanitized to prevent injection attacks
- File type validation (PDF only)
- File size limits (16MB maximum)
- Filename sanitization using Werkzeug's `secure_filename()`
- Path traversal prevention

### Rate Limiting
- General requests: 200/day, 50/hour
- Upload endpoint: 10/hour
- Login endpoint: 5/minute
- API endpoint: 100/minute

### Security Headers
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- Content Security Policy (CSP)

### File Upload Security
- PDF-only validation
- File size enforcement
- Duplicate file detection
- Metadata sanitization
- Error handling with cleanup

### Environment Security
- Debug mode disabled by default
- Secret key from environment variables
- Sensitive configuration in `.env` (not committed)
- `.gitignore` prevents sensitive file commits

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please follow these steps:

1. **DO NOT** create a public GitHub issue
2. Email the maintainer directly at: [your-email@example.com]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

### What to Expect

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 1-3 days
  - High: 1-2 weeks
  - Medium: 2-4 weeks
  - Low: Next release

### Security Update Process

1. Vulnerability confirmed
2. Fix developed and tested
3. Security advisory published
4. Update released
5. Users notified

## Security Best Practices for Deployment

### Production Deployment Checklist

- [ ] Use HTTPS/SSL certificates
- [ ] Set strong `SECRET_KEY` in environment variables
- [ ] Set strong `ADMIN_PASSWORD` in environment variables
- [ ] Set `DEBUG=False` in production
- [ ] Use a production WSGI server (not Flask development server)
- [ ] Configure firewall rules
- [ ] Enable HTTPS-only cookies
- [ ] Regular security updates for dependencies
- [ ] Monitor logs for suspicious activity
- [ ] Regular backups of uploads directory
- [ ] Consider using a reverse proxy (nginx/Apache)
- [ ] Implement IP whitelisting for admin endpoints (optional)

### Recommended Production Setup

```bash
# Install production dependencies
pip install gunicorn

# Set environment variables
export SECRET_KEY="your-very-long-random-secret-key"
export ADMIN_PASSWORD="your-strong-password"
export DEBUG=False
export FLASK_ENV=production

# Run with Gunicorn
gunicorn -w 4 -b 127.0.0.1:8000 app:app
```

### Using a Reverse Proxy (nginx example)

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Known Limitations

### Current Security Considerations

1. **Single Admin Account**: Only one admin password supported
2. **No 2FA**: Two-factor authentication not implemented
3. **No Audit Logging**: Security events not logged to files
4. **File System Storage**: Uses local file system instead of secure cloud storage
5. **Client-side Search**: Search performed in browser (all data exposed)
6. **No Session Timeout**: Sessions don't automatically expire
7. **Basic Rate Limiting**: Uses in-memory storage (resets on restart)

### Recommendations for Enhanced Security

For production deployments with sensitive data:

1. Implement proper user management system
2. Add two-factor authentication (TOTP)
3. Use database instead of file system
4. Implement comprehensive audit logging
5. Add session timeout and idle detection
6. Use Redis/Memcached for persistent rate limiting
7. Implement CAPTCHA on login
8. Add brute force protection
9. Regular security audits
10. Penetration testing

## Security Dependencies

This project uses the following security-focused dependencies:

- **Flask**: Web framework with built-in security features
- **Werkzeug**: Security utilities (password hashing, secure filename)
- **Flask-Limiter**: Rate limiting protection
- **python-dotenv**: Environment variable management

### Keeping Dependencies Updated

```bash
# Check for outdated packages
pip list --outdated

# Update all packages
pip install --upgrade -r requirements.txt

# Check for security vulnerabilities
pip install safety
safety check
```

## Security Disclosure Policy

We take security seriously and appreciate responsible disclosure of vulnerabilities. We commit to:

1. Acknowledging receipt of vulnerability reports
2. Providing regular updates on fix progress
3. Crediting reporters (unless anonymity requested)
4. Maintaining confidentiality until fix is released

## Contact

For security concerns, contact:
- GitHub: [@anacondy](https://github.com/anacondy)
- Create a private security advisory on GitHub

---

**Last Updated**: 2025-10-14
