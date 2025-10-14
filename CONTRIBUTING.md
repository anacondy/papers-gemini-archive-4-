# Contributing to Terminal Archives

Thank you for your interest in contributing to Terminal Archives! This document provides guidelines for contributions.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other contributors

## How to Contribute

### Reporting Bugs

Before creating a bug report:
1. Check existing issues to avoid duplicates
2. Verify the bug with the latest version
3. Collect relevant information

Include in your bug report:
- Description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, browser)
- Screenshots if applicable
- Error messages/logs

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:
- Clear description of the feature
- Use case and benefits
- Possible implementation approach
- Any relevant examples

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/anacondy/papers-gemini-archive-4-.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments where necessary
   - Update documentation if needed

4. **Test your changes**
   ```bash
   python app.py
   # Test manually in browser
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Explain what you changed and why

## Development Guidelines

### Code Style

**Python (PEP 8)**:
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings to functions

**JavaScript**:
- Use 4 spaces for indentation
- Use camelCase for variables
- Use semicolons
- Add comments for complex logic

**HTML/CSS**:
- Use 4 spaces for indentation
- Use semantic HTML
- Keep CSS organized by component

### Project Structure
```
papers-gemini-archive-4-/
├── app.py              # Main application
├── .env.example        # Environment template
├── requirements.txt    # Dependencies
├── static/            # CSS, JS, images
├── templates/         # HTML templates
├── uploads/           # Uploaded files (not in git)
└── docs/             # GitHub Pages content
```

### Testing

Currently, the project doesn't have automated tests. We welcome contributions to add:
- Unit tests for backend functions
- Integration tests for routes
- End-to-end tests for user flows

### Documentation

Update documentation when:
- Adding new features
- Changing existing functionality
- Fixing bugs that affect usage
- Updating dependencies

Files to update:
- `README.md` - Main documentation
- `QUICKSTART.md` - Setup instructions
- `SECURITY.md` - Security policies
- Code comments

## Areas for Contribution

### High Priority
- [ ] Add unit tests
- [ ] Implement session timeout
- [ ] Add audit logging
- [ ] Implement 2FA
- [ ] Add bulk upload feature

### Medium Priority
- [ ] Add PDF preview
- [ ] Implement search filters
- [ ] Add download statistics
- [ ] Create admin dashboard
- [ ] Add email notifications

### Low Priority
- [ ] Theme customization
- [ ] Multi-language support
- [ ] Export functionality
- [ ] Mobile app
- [ ] Browser extensions

## Security Contributions

Security is paramount. If contributing security features:
- Follow OWASP guidelines
- Document security considerations
- Add tests for security features
- Update SECURITY.md

**Never commit**:
- Passwords or secrets
- API keys
- Personal data
- Production credentials

## Review Process

1. **Automated checks** run on all PRs
2. **Maintainer review** within 7 days
3. **Feedback** provided if changes needed
4. **Merge** when approved

## Recognition

Contributors will be:
- Listed in release notes
- Credited in commits
- Thanked in documentation

## Questions?

- Open an issue for questions
- Tag maintainers in discussions
- Check existing documentation first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Terminal Archives! 🎉
