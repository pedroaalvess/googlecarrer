from src.models.user import db
from datetime import datetime

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    location = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    employment_type = db.Column(db.String(50), nullable=False)
    benefits = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relation avec les candidatures
    applications = db.relationship('Application', backref='job', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Job {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'requirements': self.requirements,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'location': self.location,
            'department': self.department,
            'employment_type': self.employment_type,
            'benefits': self.benefits,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active,
            'applications_count': len(self.applications) if self.applications else 0
        }

