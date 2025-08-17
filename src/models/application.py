from src.models.user import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    
    # Informations personnelles
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    sip = db.Column(db.String(50))
    
    # Adresse
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(100), nullable=False, default='France')
    
    # Autres informations
    cover_letter = db.Column(db.Text)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')  # pending, reviewed, accepted, rejected
    admin_notes = db.Column(db.Text)
    
    # Relation avec les documents
    documents = db.relationship('Document', backref='application', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Application {self.first_name} {self.last_name} for Job {self.job_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'sip': self.sip,
            'address': self.address,
            'city': self.city,
            'postal_code': self.postal_code,
            'country': self.country,
            'cover_letter': self.cover_letter,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status,
            'admin_notes': self.admin_notes,
            'documents': [doc.to_dict() for doc in self.documents] if self.documents else []
        }

    def to_dict_summary(self):
        """Version simplifiée pour les listes"""
        return {
            'id': self.id,
            'job_id': self.job_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'city': self.city,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status,
            'documents_count': len(self.documents) if self.documents else 0
        }

