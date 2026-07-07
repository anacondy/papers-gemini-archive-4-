import os
import re
from app import app, db, Paper
from services.paper_index import PAPER_FILENAME_PATTERN

def migrate():
    print("Starting migration from file-system to SQLite...")
    upload_folder = 'uploads'
    if not os.path.exists(upload_folder):
        print("Upload folder not found.")
        return

    count = 0
    for filename in os.listdir(upload_folder):
        match = PAPER_FILENAME_PATTERN.match(filename)
        if match:
            groups = match.groups()
            # Check if already in DB
            if Paper.query.filter_by(filename=filename).first():
                continue
            
            new_paper = Paper(
                filename=filename,
                admin_name=groups[6],
                class_name=groups[0],
                subject=groups[1],
                semester=groups[2].replace("Sem-", ""),
                exam_year=groups[3],
                exam_type=groups[4],
                medium=groups[5],
                original_name=groups[7]
            )
            db.session.add(new_paper)
            count += 1
    
    db.session.commit()
    print(f"Successfully migrated {count} papers to the database!")

if __name__ == '__main__':
    with app.app_context():
        migrate()
