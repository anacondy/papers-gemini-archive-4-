# Ledger blueprint

This blueprint provides a minimal metadata ledger for Flask applications with drag & drop file uploads.

## Quick setup

1. Install dependencies in your virtualenv:
 ```
 pip install Flask SQLAlchemy python-dotenv
 ```

2. Copy the `ledger/` folder into your project.

3. In your main Flask app (e.g., app.py), initialize the blueprint:
 ```python
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

4. Create uploads folder and ensure permissions (on PythonAnywhere create $HOME/uploads and set LEDGER_UPLOAD_FOLDER accordingly).

5. Visit /ledger/upload to try the drag & drop UI.

## Notes for PythonAnywhere

- Use a virtualenv and the web tab to point the web app to the virtualenv and WSGI file.
- Set environment variables in the PythonAnywhere Web -> Environment variables section:
  - DATABASE_URL if using an external DB
  - LEDGER_UPLOAD_FOLDER (recommended: /home/yourusername/uploads)
  - SIGNING_KEY (optional HMAC-like signing key)
- Ensure the upload directory is writeable by the web process.

**Security note**: Protect the /ledger/metadata POST endpoint with your app's authentication. Currently this blueprint accepts writes from any client that can reach the endpoint.

## Production notes:

- For higher assurance use an asymmetric signature stored in a KMS (AWS KMS / Azure Key Vault / GCP KMS) and sign entry_hash values.
- To make entries notarized, periodically compute a Merkle root for a batch of new entries and anchor the root on a public ledger; store anchor tx id in anchor_tx column.
