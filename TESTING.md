# Testing Guide

This document describes how to test the Papers Archive application.

## Manual Testing Checklist

### 1. Installation Testing

- [ ] Clone/download repository successfully
- [ ] Virtual environment creates without errors
- [ ] Dependencies install without conflicts
- [ ] Application starts without errors
- [ ] No errors in console on startup

### 2. UI Testing

#### Homepage (/)
- [ ] Page loads successfully
- [ ] Terminal animation displays correctly
- [ ] Device info appears (CPU cores, memory, storage)
- [ ] "Welcome to Terminal Archives" message shows
- [ ] System reports "ready"

#### Desktop Search (Ctrl+K)
- [ ] Ctrl+K opens search modal
- [ ] Modal has proper styling
- [ ] Input field is focused automatically
- [ ] ESC key closes modal
- [ ] Enter submits search

#### Mobile Search
- [ ] On mobile, search bar appears at bottom
- [ ] Search bar is fixed position
- [ ] Keyboard doesn't cover search results
- [ ] Touch interactions work smoothly

#### Upload Page (/admin)
- [ ] Page loads successfully
- [ ] All form fields display correctly
- [ ] Dropdowns have correct options
- [ ] File upload button works
- [ ] Form styling is consistent

### 3. Functional Testing

#### Search Functionality
Test searches with:
- [ ] Single subject: "Physics"
- [ ] Year only: "2024"
- [ ] Combined: "BSc Physics 2024"
- [ ] Semester: "Sem 1"
- [ ] Exam type: "CIA"
- [ ] Medium: "English"
- [ ] Non-existent term: "XYZ123" (should show "no results")

#### Upload Functionality

**Valid Uploads:**
- [ ] Upload with all required fields filled
- [ ] Upload with optional fields empty
- [ ] Upload with special characters in subject
- [ ] Upload with long filename
- [ ] Upload small PDF (< 1MB)
- [ ] Upload large PDF (5-9MB)

**Invalid Uploads (Should Fail):**
- [ ] Empty file name
- [ ] Missing required fields
- [ ] File > 10MB (should reject)
- [ ] Non-PDF file (.txt, .doc, .jpg)
- [ ] PDF with .txt extension
- [ ] Empty form submission

#### File Download
- [ ] Click search result opens PDF
- [ ] PDF displays in browser
- [ ] PDF can be downloaded
- [ ] PDF metadata is correct (check properties)

### 4. Security Testing

#### Input Validation
- [ ] Try path traversal: "../../etc/passwd"
- [ ] Try special chars in admin name: "<script>alert('xss')</script>"
- [ ] Try SQL injection patterns (if database added)
- [ ] Try empty strings in required fields
- [ ] Try very long strings (>1000 chars)

#### File Upload Security
- [ ] Try uploading .exe renamed to .pdf
- [ ] Try uploading file with null bytes in name
- [ ] Try uploading to different path: "../../test.pdf"
- [ ] Verify files go to uploads/ folder only

#### HTTP Headers
- [ ] Check X-Frame-Options header exists
- [ ] Check Content-Security-Policy header exists
- [ ] Check X-Content-Type-Options header exists

### 5. Error Handling

- [ ] Try accessing non-existent file
- [ ] Try accessing /uploads/../../etc/passwd
- [ ] Submit form with JavaScript disabled
- [ ] Try uploading while offline
- [ ] Rapid-fire multiple uploads

### 6. Performance Testing

- [ ] Upload 10 PDFs in sequence
- [ ] Search with 50+ results
- [ ] Load page with slow connection
- [ ] Test on mobile 3G
- [ ] Multiple concurrent users (if possible)

### 7. Browser Compatibility

Test on:
- [ ] Chrome/Chromium (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Chrome
- [ ] Mobile Safari

### 8. Responsive Design

Test at resolutions:
- [ ] Desktop: 1920x1080
- [ ] Laptop: 1366x768
- [ ] Tablet: 768x1024
- [ ] Mobile: 375x667
- [ ] Mobile landscape: 667x375

## Automated Testing (Future)

### Unit Tests (Not yet implemented)

Suggested test cases:

```python
def test_allowed_file():
    assert allowed_file('test.pdf') == True
    assert allowed_file('test.txt') == False
    
def test_sanitize():
    assert sanitize('<script>alert("xss")</script>') == 'scriptalertxssscript'
    
def test_validate_filename():
    assert validate_filename('test.pdf') == True
    assert validate_filename('../test.pdf') == False
```

### Integration Tests (Not yet implemented)

```python
def test_upload_endpoint():
    # Test file upload with all fields
    pass
    
def test_search_api():
    # Test /api/papers endpoint
    pass
    
def test_security_headers():
    # Test all security headers present
    pass
```

## Security Testing Tools

### Manual Tools

**Browser DevTools:**
1. Open DevTools (F12)
2. Network tab: Check headers
3. Console: Check for errors
4. Application: Check cookies/storage

**cURL Testing:**
```bash
# Test security headers
curl -I http://127.0.0.1:5000/

# Test file upload
curl -X POST -F "file=@test.pdf" \
  -F "admin_name=Test" \
  -F "class=BSc" \
  http://127.0.0.1:5000/upload

# Test API endpoint
curl http://127.0.0.1:5000/api/papers
```

### Automated Tools

**OWASP ZAP (Recommended):**
1. Download from owasp.org
2. Point to http://127.0.0.1:5000
3. Run active scan
4. Review findings

**Security Headers Check:**
```bash
# Online tool
https://securityheaders.com

# Or use curl
curl -I http://127.0.0.1:5000/ | grep -i "^x-\|^content-security"
```

## Performance Testing

### Load Testing with Apache Bench

```bash
# Test homepage
ab -n 1000 -c 10 http://127.0.0.1:5000/

# Test API
ab -n 1000 -c 10 http://127.0.0.1:5000/api/papers
```

### Expected Results
- Response time < 200ms for homepage
- Response time < 500ms for API
- No errors under normal load

## Test Data

### Sample Valid Upload
```
Admin Name: Test User
Class: BSc
Subject: Physics
Semester: 3
Year: 2024
Exam Type: Main Semester
Medium: English Medium
Time: 3 hr
Max Marks: 100
File: sample.pdf (valid PDF file)
```

### Sample Test PDFs

Create test PDFs:
- Small: 500 KB
- Medium: 5 MB
- Large: 9 MB
- Too large: 11 MB (should fail)

## Bug Reporting Template

When you find a bug:

```markdown
**Bug Title:** Brief description

**Severity:** Critical/High/Medium/Low

**Steps to Reproduce:**
1. Go to...
2. Click on...
3. Enter...
4. See error

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Screenshots:**
If applicable

**Environment:**
- OS: Windows 10
- Browser: Chrome 120
- Python: 3.11
- Flask: 3.0.0

**Console Errors:**
Any errors from browser console or terminal
```

## Testing Checklist Summary

**Before Release:**
- [ ] All manual tests pass
- [ ] No console errors
- [ ] Security headers present
- [ ] File upload works
- [ ] Search works
- [ ] Mobile responsive
- [ ] Cross-browser compatible
- [ ] No XSS vulnerabilities
- [ ] No path traversal possible
- [ ] Files upload to correct directory
- [ ] Documentation is accurate

**Before Production Deployment:**
- [ ] Add authentication
- [ ] Add rate limiting
- [ ] Add automated tests
- [ ] Security audit complete
- [ ] Load testing complete
- [ ] Backup system in place
- [ ] Monitoring configured
- [ ] Error logging set up

## Continuous Testing

### After Each Code Change:
1. Run manual smoke test (homepage, upload, search)
2. Check console for errors
3. Test on mobile view
4. Verify security headers still present

### Weekly:
1. Full manual test suite
2. Security scan with OWASP ZAP
3. Performance test with Apache Bench
4. Dependency updates check

### Before Deployment:
1. Complete test checklist
2. Browser compatibility check
3. Mobile device testing
4. Security review
5. Code review

---

**Remember:** Testing is ongoing! Always test after making changes.
