# 📚 Terminal Archives - Previous Year Papers Repository

A secure, terminal-themed web application for archiving and searching previous year exam papers. Built with Flask and designed with a retro terminal aesthetic.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Flask](https://img.shields.io/badge/flask-3.0.0-lightgrey)

## 🎯 Project Purpose

This application provides a centralized platform for students to:
- **Search** through a database of previous year exam papers
- **Access** papers by class, subject, semester, year, exam type, and medium
- **Upload** new papers (admin only, with authentication)
- **Browse** papers with a unique terminal-style interface

## ✨ Features

### Security Features (Rating: 8/10)
- ✅ **Authentication**: Password-protected admin access
- ✅ **Rate Limiting**: Protects against brute force and DDoS attacks
- ✅ **File Validation**: Strict PDF-only upload with size limits (16MB)
- ✅ **Path Sanitization**: Prevents directory traversal attacks
- ✅ **Security Headers**: CSP, X-Frame-Options, X-XSS-Protection, HSTS
- ✅ **Session Security**: HTTPOnly, Secure, SameSite cookies
- ✅ **Input Sanitization**: All user inputs are sanitized
- ✅ **Error Handling**: Custom error pages prevent information leakage

### User Experience (Rating: 9/10)
- 🖥️ **Terminal UI**: Unique retro terminal interface
- 📱 **Mobile Responsive**: Adapts to mobile and desktop devices
- 🔍 **Fast Search**: Real-time client-side search
- ⌨️ **Keyboard Shortcuts**: Ctrl+K for quick search on desktop
- 🎨 **Clean Design**: Dark theme with green accents

### Technical Stack (Rating: 8/10)
- **Backend**: Flask 3.0.0 (Python)
- **Frontend**: Vanilla JavaScript (no frameworks)
- **PDF Processing**: PyPDF2
- **Security**: Flask-Limiter, Werkzeug security utilities
- **Styling**: Pure CSS with Google Fonts (Fira Code)

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/anacondy/papers-gemini-archive-4-.git
   cd papers-gemini-archive-4-
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   - `SECRET_KEY`: A strong random secret key
   - `ADMIN_PASSWORD`: Your admin password
   - `DEBUG`: Set to `False` for production

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Main interface: `http://localhost:5000`
   - Admin login: `http://localhost:5000/admin/login`

## 📖 Usage Guide

### For Students (Searching Papers)

1. **Desktop**: Press `Ctrl+K` to open search modal
2. **Mobile**: Use the search bar at the bottom
3. Type your query (e.g., "Physics 2024", "BSc Semester I")
4. Click on results to download papers

### For Admins (Uploading Papers)

1. Navigate to `/admin/login`
2. Enter your admin password
3. Fill in the paper details:
   - Your name
   - Class (BA, BSc, etc.)
   - Subject
   - Semester
   - Exam year
   - Exam type
   - Medium (English/Hindi/Hinglish)
   - Time and marks (optional)
4. Upload PDF file (max 16MB)
5. Paper metadata is automatically embedded in the PDF

### Admin Shortcut
Type `upload` in the search box to quickly access admin login (you'll be prompted for your name).

## 🔒 Security Best Practices

### For Deployment

1. **Use HTTPS**: Always deploy with SSL/TLS certificates
2. **Strong Passwords**: Use a strong, random admin password
3. **Environment Variables**: Never commit `.env` file to git
4. **Regular Updates**: Keep dependencies updated
5. **Backup**: Regularly backup the `uploads/` directory
6. **Monitoring**: Monitor logs for suspicious activity

### Default Security Settings

- File size limit: 16MB
- Rate limits: 
  - General: 200 requests/day, 50/hour
  - Upload: 10 requests/hour
  - Login: 5 attempts/minute
  - API: 100 requests/minute

## 📁 Project Structure

```
papers-gemini-archive-4-/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
├── README.md             # This file
├── static/               # Static assets
│   ├── script.js        # Frontend JavaScript
│   └── style.css        # Styles
├── templates/           # HTML templates
│   ├── index.html      # Main terminal interface
│   ├── upload.html     # Admin upload form
│   └── login.html      # Admin login page
└── uploads/            # PDF storage (not in git)
```

## 🎨 Customization

### Changing the Theme
Edit `style.css` variables:
```css
:root {
    --primary-color: #4CAF50;  /* Main accent color */
    --bg-color: #1a1a1a;       /* Background */
    --text-color: #e0e0e0;     /* Text color */
}
```

### Adding More Subjects/Classes
Edit the dropdown options in `templates/upload.html`.

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "Permission denied" on uploads
```bash
chmod 755 uploads/
```

### Rate limit errors
Adjust limits in `app.py` or wait for the cooldown period.

## 📊 Project Ratings

| Category | Rating | Notes |
|----------|--------|-------|
| **Security** | 8/10 | Strong security measures, could add 2FA |
| **Setup Ease** | 9/10 | Simple pip install and run |
| **Code Quality** | 8/10 | Clean, well-structured, documented |
| **UI/UX** | 9/10 | Unique terminal theme, responsive |
| **Innovation** | 7/10 | Creative UI approach, standard backend |
| **Documentation** | 9/10 | Comprehensive README and comments |
| **Maintainability** | 8/10 | Modular code, easy to extend |

**Overall Score**: 8.3/10

## 🚧 Known Limitations

- Single admin account (no multi-user support)
- No database (uses file system)
- No paper preview functionality
- No bulk upload feature
- Client-side search only (no advanced queries)

## 🔮 Future Enhancements

- [ ] Multi-user admin support with roles
- [ ] PostgreSQL/SQLite database integration
- [ ] PDF preview in browser
- [ ] Bulk upload functionality
- [ ] Advanced search filters
- [ ] Paper analytics and download tracking
- [ ] Email notifications for new uploads
- [ ] Tags and categories
- [ ] Two-factor authentication

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Anuj Meena**
- GitHub: [@anacondy](https://github.com/anacondy)

## 🙏 Acknowledgments

- Terminal UI inspired by classic Unix terminals
- Built with Flask and modern web technologies
- Community feedback and contributions

---

**⚠️ Important Security Note**: This application includes basic security features suitable for small-scale deployments. For production use with sensitive data, consider additional security measures like:
- Regular security audits
- Professional penetration testing
- Advanced authentication systems (OAuth, SAML)
- Database encryption
- Comprehensive logging and monitoring
- Web Application Firewall (WAF)

---

Made with ❤️ for students everywhere
