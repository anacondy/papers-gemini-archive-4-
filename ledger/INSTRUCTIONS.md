# Metadata Ledger — Repo & PythonAnywhere Deployment Steps

This document explains exactly which files belong in the repository vs what must be done on the server (PythonAnywhere). It provides step-by-step commands and checklists so you can:

- Add the metadata ledger feature to the repo (branch / PR).
- Deploy and run it on PythonAnywhere (virtualenv, uploads, env vars).
- Test and secure the feature.

Use this as a copy-paste-ready checklist and reference for collaborators or automation agents.

---

## Short summary / goal
Add a Flask blueprint `ledger/` that implements an append-only metadata ledger with:
- SHA-256 chained entry hashes (prev_hash → entry_hash).
- Optional signature (SIGNING_KEY).
- Drag & drop file upload UI that stores files in an `uploads/` folder and records file metadata (filename, stored path, sha256) in ledger entries.

We separate steps into:
- Repo changes — what to commit to version control.
- PythonAnywhere server setup — what to configure on the live host (virtualenv, uploads folder, env vars, WSGI).

---

## Files to add to the repository (commit these)
Place the following files into your project repository exactly as shown.

ledger/ (blueprint)
- ledger/__init__.py
- ledger/models.py
- ledger/routes.py
- ledger/README.md
- ledger/templates/upload.html
- ledger/static/ledger.js
- ledger/static/ledger.css

requirements/
- requirements/ledger-requirements.txt

Notes:
- Do NOT commit `uploads/` (server-side storage) — add it to `.gitignore`.

Why in repo:
- These files are source code + static assets and are required for other developers and CI. They define the blueprint and UI and must be versioned.

---

## Files & resources to create/configure on PythonAnywhere (server-side)
These are NOT committed to the repo; they are runtime resources and environment configuration:

- uploads/ directory (physical folder where uploaded files are saved)
  - Path example: `/home/<yourusername>/uploads`
  - Create this on the server and make it writable by the web process.
- Environment variables (configured in the PythonAnywhere Web UI)
  - LEDGER_UPLOAD_FOLDER=/home/<yourusername>/uploads
  - SIGNING_KEY=<strong-random-string> (optional, for HMAC-like tamper evidence)
  - DATABASE_URL (optional if using an external DB; by default the blueprint uses sqlite:///ledger.db)
- Virtualenv with dependencies installed (Flask, SQLAlchemy, python-dotenv, etc.)
- WSGI entrypoint changes: import the blueprint init and call `init_app(app, url_prefix='/ledger')` and run `db.create_all()` in app context (update the project's WSGI/app file).

Why server-only:
- `uploads/` contains user data and must not be tracked in Git. Environment settings are secrets/host-specific and should be set in the host environment, not in the repo.

---

## Step-by-step: Add files to the repo (local developer flow)

1. Create a branch:
   git checkout -b feature/metadata-ledger

2. Create file structure and paste files (or copy them in your editor):
   mkdir -p ledger/templates ledger/static requirements

   # create each file under ledger/ and paste the provided contents

3. Add uploads/ to `.gitignore`:
   echo "uploads/" >> .gitignore

4. Stage & commit:
   git add ledger/ requirements/ledger-requirements.txt .gitignore
   git commit -m "Add metadata ledger blueprint with drag-and-drop uploads"

5. Push the branch:
   git push origin feature/metadata-ledger

6. Create a Pull Request:
   - Using GitHub CLI:
     gh pr create --base main --head feature/metadata-ledger --title "Add metadata ledger blueprint with drag-and-drop uploads" --body "Adds ledger/ blueprint and README for PythonAnywhere deployment."
   - Or use the GitHub web UI to open a PR.

---

## Step-by-step: Integrate blueprint into your Flask app (repo change)

Edit your Flask app entrypoint (e.g., `app.py`, or `wsgi.py`) and add:

```python
# Integration snippet (copy into your app creation code)
import os
from flask import Flask
from ledger import init_app, db

app = Flask(__name__)
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///ledger.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    LEDGER_UPLOAD_FOLDER = os.environ.get('LEDGER_UPLOAD_FOLDER', 'uploads'),
    SIGNING_KEY = os.environ.get('SIGNING_KEY', None),
)

init_app(app, url_prefix='/ledger')

with app.app_context():
    db.create_all()
```

Notes:
- Use server-side `current_user` or your auth system to set `created_by`. Do not trust client-supplied `created_by` for accountability.
- Commit the integration changes on the same feature branch before opening the PR (or push a new commit to the PR).

---

## Step-by-step: Deploy to PythonAnywhere

1. Prepare virtualenv (PythonAnywhere web tab or console)
   - In Bash console:
     mkvirtualenv --python=python3.10 <yourenv>   # or create virtualenv manually
     pip install -r requirements/ledger-requirements.txt
     # Also install your project requirements (if separate), or add dependencies to central requirements.

2. Create uploads folder on server (do NOT commit)
   mkdir -p /home/<yourusername>/uploads
   chmod 755 /home/<yourusername>/uploads
   # Ensure the web app process can write to it

3. Set environment variables in PythonAnywhere Web -> Environment variables:
   - LEDGER_UPLOAD_FOLDER=/home/<yourusername>/uploads
   - SIGNING_KEY=<a strong random string>
   - DATABASE_URL if using external DB (optional)

4. Modify WSGI or app entrypoint used by PythonAnywhere to include the integration snippet above (if you committed it to repo, then ensure WSGI imports the Flask app module normally).

5. Restart the web app from PythonAnywhere Web tab.

6. Visit the upload UI:
   https://<your-username>.pythonanywhere.com/ledger/upload
   or https://your-custom-domain/ledger/upload if configured.

---

## Quick tests (after deployment or local dev)

- Upload via UI: visit `/ledger/upload`, drag a file, set `resource_id`, click Submit. Response should include `entry.entry_hash`.

- Upload via curl (multipart):
  curl -v \
    -F "resource_id=test1" \
    -F "created_by=testuser" \
    -F "file0=@/path/to/file.png" \
    https://<your-host>/ledger/metadata

- List ledger for a resource:
  curl https://<your-host>/ledger/ledger/test1

- Get single entry:
  curl https://<your-host>/ledger/entry/<entry_hash>

- Validate chaining:
  - On successive uploads for same resource, ensure entry2.prev_hash == entry1.entry_hash.

---

## Security checklist (must do before public rollout)

- Require authentication on `POST /ledger/metadata`. Example:
  - Add your app's login decorator around `add_metadata()` or check `current_user` and return 401 if not authenticated.
  - Server should set `created_by = current_user.username` (do not trust client-sent created_by).
- Limit file types and max upload size:
  - Update `ALLOWED_EXTENSIONS` and enforce `MAX_CONTENT_LENGTH` in Flask config.
- Protect your SIGNING_KEY: set as environment variable (PythonAnywhere Web UI), never store in repo.
- Consider replacing PBKDF2 pseudo-signatures with an asymmetric signature using KMS for true non-repudiation.
- Consider storing big files in S3 or other object storage; store only reference (S3 URL or content-addressed CID) in the ledger.

---

## CI, tests & acceptance criteria (recommended)

Add tests that assert:
- POST /ledger/metadata returns 200 and `entry.entry_hash`.
- GET /ledger/<resource_id> returns entries in chronological order.
- prev_hash chaining is correct.
- Files are saved to LEDGER_UPLOAD_FOLDER and sha256 recorded.

Acceptance criteria for merging:
- Upload page loads at `/ledger/upload`.
- POST /ledger/metadata requires authentication and returns ledger entries.
- Files saved to the configured upload directory and metadata recorded.

---

## What belongs in the repo vs what must be done on PythonAnywhere (concise)

In repo (commit):
- ledger/ (all files listed above)
- integration code in your Flask app source (snippet to register blueprint)
- tests and CI config
- requirements/ledger-requirements.txt
- .gitignore updated to include `uploads/`

On server (do not commit):
- uploads/ directory (create and ensure permissions)
- environment variables (LEDGER_UPLOAD_FOLDER, SIGNING_KEY, DATABASE_URL)
- virtualenv with packages installed (pip install)
- production database (if external)
- web app configuration / WSGI file and restart

Why this split:
- Repo contains code and assets so they can be version-controlled, reviewed, and tested.
- Server contains runtime data (uploads) and secrets (env vars), which must not be committed for security and portability.

---

## Ready-to-paste agent prompt (if you want someone to finish and open a PR)

Use this to instruct a developer/agent to complete integration and open the PR:

"Task: integrate the `ledger/` blueprint into the Flask app, secure the write endpoint, add tests, and open a PR.

Repository: anacondy/papers-gemini-archive-4-
Base: main
Feature branch: feature/metadata-ledger-integration

Steps:
1. Ensure `ledger/` exists; if not, add the provided ledger files and `requirements/ledger-requirements.txt`.
2. Add the integration snippet into the Flask app entrypoint (import `init_app, db` and call `init_app(app, url_prefix='/ledger')` and `db.create_all()` within app context).
3. Protect `POST /ledger/metadata` with the app's authentication and set `created_by` from the server-side `current_user`.
4. Add `uploads/` to `.gitignore`.
5. Merge requirements and install dependencies in CI/virtualenv.
6. Add tests covering upload and chaining behavior.
7. Create branch `feature/metadata-ledger-integration`, commit changes, push branch, and open a PR to `main` with title: 'Integrate metadata ledger blueprint and add drag-and-drop upload UI'.
8. Assign reviewer `anacondy` and include testing & PythonAnywhere deployment steps in the PR description.

Acceptance: PR builds (tests pass), upload page reachable at `/ledger/upload`, `POST /ledger/metadata` requires auth and returns `entry_hash`, files stored in uploads directory."

---

## Useful commands recap

Local Git:
- git checkout -b feature/metadata-ledger
- git add ledger/ requirements/ledger-requirements.txt .gitignore
- git commit -m "Add metadata ledger blueprint with drag-and-drop uploads"
- git push origin feature/metadata-ledger
- gh pr create --base main --head feature/metadata-ledger --title "Add metadata ledger blueprint with drag-and-drop uploads" --body "..."

PythonAnywhere (console):
- mkdir -p /home/<yourusername>/uploads
- chmod 755 /home/<yourusername>/uploads
- workon <virtualenv> or source <venv>/bin/activate
- pip install -r requirements/ledger-requirements.txt

curl test:
- curl -F "resource_id=doc1" -F "file0=@/path/to/file.png" https://<host>/ledger/metadata

---

If you want, I will add this file to the repo for you on a new commit/branch and prepare a PR body ready to submit. Which do you prefer: (A) I commit this INSTRUCTIONS.md to the `ledger/` folder on a new branch and prepare PR content, or (B) you will add it yourself and I help verify the PR/tests?
