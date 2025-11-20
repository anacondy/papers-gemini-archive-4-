import os
import json
import hashlib
import datetime
from flask import current_app, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from . import ledger_bp, db
from .models import MetadataLedger

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json', 'csv', 'zip'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ledger_bp.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')

@ledger_bp.route('/metadata', methods=['POST'])
def add_metadata():
    resource_id = None
    if request.content_type and request.content_type.startswith('application/json'):
        j = request.get_json(silent=True) or {}
        resource_id = j.get('resource_id')
    else:
        resource_id = request.form.get('resource_id')
    
    if not resource_id:
        return jsonify({'ok': False, 'error': 'resource_id required'}), 400
    
    created_by = (request.form.get('created_by') or (request.get_json(silent=True) or {}).get('created_by'))
    
    base_metadata = {}
    if request.form.get('metadata'):
        try:
            base_metadata = json.loads(request.form.get('metadata'))
        except Exception:
            return jsonify({'ok': False, 'error': 'invalid metadata json'}), 400
    elif request.content_type and request.content_type.startswith('application/json'):
        base_metadata = (request.get_json(silent=True) or {}).get('metadata') or {}
    
    files_meta = []
    upload_folder = current_app.config.get('LEDGER_UPLOAD_FOLDER', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    for key in request.files:
        f = request.files.get(key)
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            unique = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
            save_name = f"{unique}-{fname}"
            save_path = os.path.join(upload_folder, save_name)
            f.save(save_path)
            
            h = hashlib.sha256()
            with open(save_path, 'rb') as fh:
                for chunk in iter(lambda: fh.read(8192), b''):
                    h.update(chunk)
            file_hash = h.hexdigest()
            
            rel_path = os.path.relpath(save_path, start=os.getcwd())
            files_meta.append({'field': key, 'filename': fname, 'stored_as': save_name, 'path': rel_path, 'sha256': file_hash})
    
    if files_meta:
        base_metadata.setdefault('files', []).extend(files_meta)
    
    last = MetadataLedger.query.filter_by(resource_id=resource_id).order_by(MetadataLedger.created_at.desc(), MetadataLedger.id.desc()).first()
    prev_hash = last.entry_hash if last else ''
    
    metadata_text = json.dumps(base_metadata, sort_keys=True, separators=(',', ':'))
    created_at = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
    hash_input = '|'.join([prev_hash, resource_id, metadata_text, created_at, created_by or ''])
    entry_hash = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
    
    signature = None
    signing_key = current_app.config.get('SIGNING_KEY')
    if signing_key:
        signature = hashlib.pbkdf2_hmac('sha256', entry_hash.encode('utf-8'), signing_key.encode('utf-8'), 100000).hex()
    
    entry = MetadataLedger(resource_id=resource_id, metadata=base_metadata, created_by=created_by, created_at=datetime.datetime.utcnow(), prev_hash=prev_hash or None, entry_hash=entry_hash, signature=signature)
    db.session.add(entry)
    db.session.commit()
    
    return jsonify({'ok': True, 'entry': entry.as_dict()})

@ledger_bp.route('/ledger/<resource_id>', methods=['GET'])
def get_ledger(resource_id):
    entries = MetadataLedger.query.filter_by(resource_id=resource_id).order_by(MetadataLedger.created_at.asc(), MetadataLedger.id.asc()).all()
    return jsonify({'ok': True, 'entries': [e.as_dict() for e in entries]})

@ledger_bp.route('/entry/<entry_hash>', methods=['GET'])
def get_entry(entry_hash):
    e = MetadataLedger.query.filter_by(entry_hash=entry_hash).first()
    if not e:
        return jsonify({'ok': False, 'error': 'not_found'}), 404
    return jsonify({'ok': True, 'entry': e.as_dict()})

@ledger_bp.route('/uploads/<path:filename>', methods=['GET'])
def uploaded_file(filename):
    upload_folder = current_app.config.get('LEDGER_UPLOAD_FOLDER', 'uploads')
    return send_from_directory(upload_folder, filename)
