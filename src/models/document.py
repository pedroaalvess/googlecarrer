from src.models.user import db
from datetime import datetime

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    
    # Informations du fichier
    document_type = db.Column(db.String(50), nullable=False)  # id_front, id_back, address_proof, cv, cover_letter
    file_name = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    mime_type = db.Column(db.String(100))
    
    # Métadonnées
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)
    verification_notes = db.Column(db.Text)

    def __repr__(self):
        return f'<Document {self.file_name} for Application {self.application_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'application_id': self.application_id,
            'document_type': self.document_type,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'is_verified': self.is_verified,
            'verification_notes': self.verification_notes
        }

    @staticmethod
    def get_allowed_types():
        """Types de documents autorisés"""
        return {
            'id_front': 'Pièce d\'identité (recto)',
            'id_back': 'Pièce d\'identité (verso)',
            'address_proof': 'Justificatif de domicile',
            'cv': 'Curriculum Vitae',
            'cover_letter': 'Lettre de motivation'
        }

    @staticmethod
    def get_allowed_extensions():
        """Extensions de fichiers autorisées"""
        return {'jpg', 'jpeg', 'png', 'pdf'}

    @staticmethod
    def get_max_file_size():
        """Taille maximale en bytes (5MB)"""
        return 5 * 1024 * 1024

