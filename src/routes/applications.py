import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from src.models.application import Application, db
from src.models.document import Document
from src.models.job import Job

applications_bp = Blueprint('applications', __name__)

# Configuration pour l'upload de fichiers
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_upload_folder():
    """Créer le dossier d'upload s'il n'existe pas"""
    try:
        # Usar caminho absoluto baseado no diretório do projeto
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        upload_path = os.path.join(project_root, UPLOAD_FOLDER)
        
        print(f"Creating upload folder at: {upload_path}")
        
        if not os.path.exists(upload_path):
            os.makedirs(upload_path, exist_ok=True)
            print(f"Created base upload folder: {upload_path}")
        
        # Criar subpastas por data para organização
        from datetime import datetime
        date_folder = datetime.now().strftime('%Y/%m')
        full_upload_path = os.path.join(upload_path, date_folder)
        
        print(f"Creating date folder at: {full_upload_path}")
        
        if not os.path.exists(full_upload_path):
            os.makedirs(full_upload_path, exist_ok=True)
            print(f"Created date folder: {full_upload_path}")
        
        return full_upload_path
    except Exception as e:
        print(f"Error creating upload folder: {str(e)}")
        # Fallback para pasta uploads simples
        fallback_path = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(fallback_path):
            os.makedirs(fallback_path, exist_ok=True)
        return fallback_path

@applications_bp.route('/applications', methods=['POST'])
def create_application():
    """Créer une nouvelle candidature"""
    try:
        data = request.get_json()
        
        # Validation des données requises
        required_fields = [
            'job_id', 'first_name', 'last_name', 'email', 
            'phone', 'address', 'city', 'postal_code'
        ]
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Le champ {field} est requis'
                }), 400
        
        # Vérifier que le job existe
        job = Job.query.get(data['job_id'])
        if not job or not job.is_active:
            return jsonify({
                'success': False,
                'error': 'Cette offre d\'emploi n\'existe pas ou n\'est plus disponible'
            }), 404
        
        # Créer la candidature
        application = Application(
            job_id=data['job_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            sip=data.get('sip'),
            address=data['address'],
            city=data['city'],
            postal_code=data['postal_code'],
            country=data.get('country', 'France'),
            cover_letter=data.get('cover_letter')
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'application': application.to_dict(),
            'message': 'Candidature créée avec succès'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@applications_bp.route('/applications/<int:application_id>/documents', methods=['POST'])
def upload_document(application_id):
    """Upload d'un document pour une candidature"""
    try:
        
        # Vérifier que la candidature existe
        application = Application.query.get_or_404(application_id)
        
        # Vérifier qu'un fichier a été envoyé
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Aucun fichier fourni'
            }), 400
        
        file = request.files['file']
        document_type = request.form.get('document_type')
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Aucun fichier sélectionné'
            }), 400
        
        if not document_type:
            return jsonify({
                'success': False,
                'error': 'Type de document requis'
            }), 400
        
        if document_type not in Document.get_allowed_types():
            return jsonify({
                'success': False,
                'error': 'Type de document non autorisé'
            }), 400
        
        if file and allowed_file(file.filename):
            # Vérifier la taille du fichier
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > MAX_FILE_SIZE:
                return jsonify({
                    'success': False,
                    'error': 'Fichier trop volumineux (max 5MB)'
                }), 400
            
            # Créer le dossier d'upload
            upload_path = create_upload_folder()
            
            # Générer un nom de fichier unique
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
            file_path = os.path.join(upload_path, unique_filename)
            
            # Sauvegarder le fichier
            print(f"Saving file to: {file_path}")
            file.save(file_path)
            print(f"File saved successfully")
            
            # Créer l'enregistrement en base
            document = Document(
                application_id=application_id,
                document_type=document_type,
                file_name=secure_filename(file.filename),
                file_path=file_path,
                file_size=file_size,
                mime_type=file.content_type
            )
            
            print(f"Creating document record: {document_type} for application {application_id}")
            db.session.add(document)
            db.session.commit()
            print(f"Document saved to database with ID: {document.id}")
            
            return jsonify({
                'success': True,
                'document': document.to_dict(),
                'message': 'Document uploadé avec succès'
            }), 201
        
        else:
            return jsonify({
                'success': False,
                'error': 'Type de fichier non autorisé'
            }), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@applications_bp.route('/applications/<int:application_id>', methods=['GET'])
def get_application(application_id):
    """Récupérer une candidature spécifique"""
    try:
        application = Application.query.get_or_404(application_id)
        
        return jsonify({
            'success': True,
            'application': application.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@applications_bp.route('/documents/<int:document_id>/download', methods=['GET'])
def download_document(document_id):
    """Télécharger un document"""
    try:
        document = Document.query.get_or_404(document_id)
        
        # Vérifier que le fichier existe
        if not os.path.exists(document.file_path):
            return jsonify({
                'success': False,
                'error': 'Fichier non trouvé'
            }), 404
        
        directory = os.path.dirname(document.file_path)
        filename = os.path.basename(document.file_path)
        
        return send_from_directory(
            directory, 
            filename, 
            as_attachment=True, 
            download_name=document.file_name
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@applications_bp.route('/applications/<int:application_id>/documents/<int:document_id>', methods=['DELETE'])
def delete_document(application_id, document_id):
    """Supprimer un document"""
    try:
        document = Document.query.filter_by(
            id=document_id, 
            application_id=application_id
        ).first_or_404()
        
        # Supprimer le fichier physique
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Supprimer l'enregistrement en base
        db.session.delete(document)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Document supprimé avec succès'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

