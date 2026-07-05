# Deployment Readiness Report (Reznik)

**Date:** 2026-07-05  
**Repository:** papers-gemini-archive-4-  
**Branch Checked:** main

## Executive Verdict

**Status: Conditionally ready, with 1 deployment blocker.**

The application is functionally stable in current tests and core runtime smoke checks, but production deployment using `Procfile` will fail unless `gunicorn` is added to installable dependencies.

## Validation Performed

1. Installed dependencies from `requirements.txt`.
2. Ran full automated tests (`pytest -q`).
3. Ran runtime smoke checks via Flask test client for:
   - Core routes (`/`, `/api/papers`, `/admin/login`)
   - Security headers
   - Upload path traversal protection
   - Session cookie hardening (`Secure`, `HttpOnly`, `SameSite=Lax`)
4. Compared README/deployment claims with actual source code and dependency files.

## Results Summary

- **Automated Tests:** `28 passed, 1 warning` (warning is from pypdf cryptography deprecation, non-blocking).
- **Core Route Health:** PASS (`/` 200, `/api/papers` 200 and returns JSON list).
- **Security Controls:** PASS for implemented headers and traversal defense check.
- **Authentication Flow:** PASS (`/admin/login` valid password redirects; session cookies hardened).

## Feature Matrix (README Claims vs Actual)

| Area | Claimed | Actual Status | Evidence |
|---|---|---|---|
| Admin authentication | Password-protected admin access | ✅ Working | Login route and tests pass |
| Rate limiting | Login/upload/API/general rate limits | ✅ Implemented | Flask-Limiter configured and route limits present |
| PDF-only upload | Strict PDF validation | ✅ Working | `allowed_file()` + upload tests |
| File size limit | 16MB | ✅ In main app | `MAX_FILE_SIZE = 16 * 1024 * 1024` in app |
| Metadata embedding | Write metadata into uploaded PDF | ✅ Implemented | pypdf writer metadata block in upload flow |
| Search API | Real-time searchable paper list | ✅ Working backend | `/api/papers` returns JSON list |
| Security headers | CSP, HSTS, frame/content/XSS headers | ✅ Working | headers verified in tests/smoke |
| Path sanitization | Traversal prevention for uploads | ✅ Working | path traversal smoke check returns 404 |
| Mobile/desktop UX | Ctrl+K desktop + mobile search bar | ⚠️ Implemented but not browser-E2E validated in this run | JavaScript logic present |

## What Is Working

1. Application starts and serves main and API routes.
2. Admin login/logout and upload access control work.
3. Upload endpoint validation and sanitization are active.
4. Security headers are applied globally.
5. File serving route includes traversal defenses.
6. Test suite currently passes fully.

## What Is Not Ready / Gaps

### 1. Deployment Blocker: `gunicorn` missing from dependencies

- `Procfile` expects: `web: gunicorn app:app`
- `requirements.txt` currently does **not** include `gunicorn`
- Validation check: `gunicorn_installed False`

**Impact:** Platforms that rely on the Procfile command (e.g., Heroku-style deploy) can fail at startup.

### 2. Documentation/Config Drift (non-blocking but important)

- `app.py` enforces **16MB** upload size.
- `config.py`, `TESTING.md`, and some architecture docs still reference **10MB**.

**Impact:** Operational confusion and incorrect expectations during QA/deployment.

### 3. `config.py` appears informational, not wired into app init

- Current app config is directly defined in `app.py`.

**Impact:** Team may edit `config.py` expecting behavior changes that do not apply.

## Deployment Recommendation

Proceed to deployment **after** resolving the blocker below:

1. Add `gunicorn` to `requirements.txt` (or remove Procfile dependence if target platform does not use it).

Then strongly recommended:

2. Normalize size-limit and deployment docs to 16MB (or change code to 10MB consistently).
3. Clarify whether `config.py` is active configuration or archive/template.
4. Run one browser-based manual smoke pass for UI-only claims (Ctrl+K behavior, mobile search bar UX).

## Final Readiness Call

- **For local/dev and core backend behavior:** Ready.
- **For production deployment using current Procfile path:** Not ready until `gunicorn` dependency gap is fixed.
