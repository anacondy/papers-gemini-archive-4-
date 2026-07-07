from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paper(db.Model):
    __tablename__ = 'papers'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    admin_name = db.Column(db.String(100))
    class_name = db.Column(db.String(50), index=True)
    subject = db.Column(db.String(100), index=True)
    semester = db.Column(db.String(20), index=True)
    exam_year = db.Column(db.String(10), index=True)
    exam_type = db.Column(db.String(50))
    medium = db.Column(db.String(50))
    time = db.Column(db.String(20))
    max_marks = db.Column(db.String(20))
    original_name = db.Column(db.String(255))

    def to_dict(self, url_builder):
        return {
            "class": self.class_name,
            "subject": self.subject,
            "semester": self.semester,
            "year": self.exam_year,
            "exam_type": self.exam_type,
            "medium": self.medium,
            "uploader": self.admin_name,
            "original_name": self.original_name,
            "url": url_builder(self.filename)
        }
