from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

# Shared SQLAlchemy db instance for the blueprint
db = SQLAlchemy()
ledger_bp = Blueprint('ledger', __name__, template_folder='templates', static_folder='static')

def init_app(app, url_prefix='/ledger'):
    """
    Initialize the ledger blueprint and attach the SQLAlchemy db to the main app.
    
    Usage from your Flask app:
        from ledger import init_app, db
        init_app(app)
        db.init_app(app)
        with app.app_context():
            db.create_all()
    """
    # Configure default upload folder if not set
    if not app.config.get('LEDGER_UPLOAD_FOLDER'):
        app.config['LEDGER_UPLOAD_FOLDER'] = app.config.get('UPLOAD_FOLDER', 'uploads')
    
    # Register blueprint under /ledger by default
    app.register_blueprint(ledger_bp, url_prefix=url_prefix)
    
    # Attach db instance to app
    db.init_app(app)
