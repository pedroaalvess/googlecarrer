from flask import Blueprint, request, jsonify, send_from_directory
from src.models.job import Job, db
from src.models.application import Application
from src.models.document import Document
from datetime import datetime, timedelta
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/documents/<int:document_id>/view', methods=['GET'])
def view_document(document_id):
    """Visualizar um documento"""
    try:
        document = Document.query.get_or_404(document_id)
        
        # Verificar se o arquivo existe
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
            as_attachment=False,
            mimetype=document.mime_type
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/documents/<int:document_id>/download', methods=['GET'])
def download_document(document_id):
    """Télécharger un document"""
    try:
        document = Document.query.get_or_404(document_id)
        
        # Verificar se o arquivo existe
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

@admin_bp.route('/dashboard', methods=['GET'])
def get_dashboard_stats():
    """Récupérer les statistiques du tableau de bord"""
    try:
        # Statistiques générales
        total_jobs = Job.query.filter(Job.is_active == True).count()
        total_applications = Application.query.count()
        pending_applications = Application.query.filter(Application.status == 'pending').count()
        
        # Statistiques des 30 derniers jours
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_applications = Application.query.filter(
            Application.created_at >= thirty_days_ago
        ).count()
        
        # Applications par statut
        status_stats = db.session.query(
            Application.status,
            db.func.count(Application.id).label('count')
        ).group_by(Application.status).all()
        
        # Applications par mois (6 derniers mois)
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        monthly_stats = db.session.query(
            db.func.strftime('%Y-%m', Application.created_at).label('month'),
            db.func.count(Application.id).label('count')
        ).filter(
            Application.created_at >= six_months_ago
        ).group_by('month').order_by('month').all()
        
        # Top 5 des postes les plus demandés
        popular_jobs = db.session.query(
            Job.title,
            db.func.count(Application.id).label('applications_count')
        ).join(Application).group_by(Job.id, Job.title).order_by(
            db.func.count(Application.id).desc()
        ).limit(5).all()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_jobs': total_jobs,
                'total_applications': total_applications,
                'pending_applications': pending_applications,
                'recent_applications': recent_applications,
                'status_distribution': [
                    {'status': status, 'count': count} 
                    for status, count in status_stats
                ],
                'monthly_applications': [
                    {'month': month, 'count': count} 
                    for month, count in monthly_stats
                ],
                'popular_jobs': [
                    {'title': title, 'applications': count} 
                    for title, count in popular_jobs
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/applications', methods=['GET'])
def get_all_applications():
    """Récupérer toutes les candidatures avec filtres"""
    try:
        # Paramètres de filtrage
        status = request.args.get('status')
        job_id = request.args.get('job_id', type=int)
        search = request.args.get('search')
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Construire la requête
        query = Application.query.join(Job)
        
        # Appliquer les filtres
        if status:
            query = query.filter(Application.status == status)
        
        if job_id:
            query = query.filter(Application.job_id == job_id)
        
        if search:
            search_filter = f'%{search}%'
            query = query.filter(
                db.or_(
                    Application.first_name.ilike(search_filter),
                    Application.last_name.ilike(search_filter),
                    Application.email.ilike(search_filter),
                    Job.title.ilike(search_filter)
                )
            )
        
        # Ordonner par date de création (plus récent en premier)
        query = query.order_by(Application.created_at.desc())
        
        # Paginer
        applications_paginated = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Enrichir avec les informations du job
        applications_data = []
        for app in applications_paginated.items:
            app_data = app.to_dict_summary()
            app_data['job_title'] = app.job.title if app.job else 'N/A'
            applications_data.append(app_data)
        
        return jsonify({
            'success': True,
            'applications': applications_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': applications_paginated.total,
                'pages': applications_paginated.pages,
                'has_next': applications_paginated.has_next,
                'has_prev': applications_paginated.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/applications/<int:application_id>', methods=['GET'])
def get_application_details(application_id):
    """Récupérer les détails complets d'une candidature"""
    try:
        # Usar eager loading para garantir que os documentos sejam carregados
        application = Application.query.options(
            db.joinedload(Application.documents)
        ).get_or_404(application_id)
        
        # Enrichir avec les informations du job
        app_data = application.to_dict()
        app_data['job'] = application.job.to_dict() if application.job else None
        
        # Debug: log para verificar se documentos estão sendo carregados
        print(f"Application {application_id} has {len(application.documents)} documents")
        for doc in application.documents:
            print(f"Document: {doc.id}, type: {doc.document_type}, file: {doc.file_name}")
        
        return jsonify({
            'success': True,
            'application': app_data
        })
        
    except Exception as e:
        print(f"Error getting application details: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/applications/<int:application_id>/status', methods=['PUT'])
def update_application_status(application_id):
    """Mettre à jour le statut d'une candidature"""
    try:
        application = Application.query.get_or_404(application_id)
        data = request.get_json()
        
        new_status = data.get('status')
        admin_notes = data.get('admin_notes')
        
        if not new_status:
            return jsonify({
                'success': False,
                'error': 'Statut requis'
            }), 400
        
        # Valider le statut
        valid_statuses = ['pending', 'reviewed', 'accepted', 'rejected']
        if new_status not in valid_statuses:
            return jsonify({
                'success': False,
                'error': 'Statut invalide'
            }), 400
        
        # Mettre à jour
        application.status = new_status
        if admin_notes:
            application.admin_notes = admin_notes
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'application': application.to_dict(),
            'message': 'Statut mis à jour avec succès'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/jobs', methods=['POST'])
def create_job():
    """Créer une nouvelle offre d'emploi"""
    try:
        data = request.get_json()
        
        # Validation des données requises
        required_fields = [
            'title', 'description', 'requirements', 
            'location', 'department', 'employment_type'
        ]
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Le champ {field} est requis'
                }), 400
        
        # Créer le job
        job = Job(
            title=data['title'],
            description=data['description'],
            requirements=data['requirements'],
            salary_min=data.get('salary_min'),
            salary_max=data.get('salary_max'),
            location=data['location'],
            department=data['department'],
            employment_type=data['employment_type'],
            benefits=data.get('benefits')
        )
        
        db.session.add(job)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'job': job.to_dict(),
            'message': 'Offre d\'emploi créée avec succès'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """Mettre à jour une offre d'emploi"""
    try:
        job = Job.query.get_or_404(job_id)
        data = request.get_json()
        
        # Mettre à jour les champs fournis
        updatable_fields = [
            'title', 'description', 'requirements', 'salary_min', 
            'salary_max', 'location', 'department', 'employment_type', 
            'benefits', 'is_active'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(job, field, data[field])
        
        job.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'job': job.to_dict(),
            'message': 'Offre d\'emploi mise à jour avec succès'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Supprimer une offre d'emploi (soft delete)"""
    try:
        job = Job.query.get_or_404(job_id)
        
        # Soft delete - marquer comme inactif
        job.is_active = False
        job.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Offre d\'emploi désactivée avec succès'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

