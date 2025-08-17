from flask import Blueprint, request, jsonify
from src.models.job import Job, db
from src.models.application import Application

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/jobs', methods=['GET'])
def get_jobs():
    """Récupérer toutes les offres d'emploi actives"""
    try:
        # Paramètres de filtrage
        location = request.args.get('location')
        department = request.args.get('department')
        employment_type = request.args.get('employment_type')
        salary_min = request.args.get('salary_min', type=int)
        salary_max = request.args.get('salary_max', type=int)
        search = request.args.get('search')
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Construire la requête
        query = Job.query.filter(Job.is_active == True)
        
        # Appliquer les filtres
        if location:
            query = query.filter(Job.location.ilike(f'%{location}%'))
        
        if department:
            query = query.filter(Job.department.ilike(f'%{department}%'))
        
        if employment_type:
            query = query.filter(Job.employment_type == employment_type)
        
        if salary_min:
            query = query.filter(Job.salary_min >= salary_min)
        
        if salary_max:
            query = query.filter(Job.salary_max <= salary_max)
        
        if search:
            search_filter = f'%{search}%'
            query = query.filter(
                db.or_(
                    Job.title.ilike(search_filter),
                    Job.description.ilike(search_filter),
                    Job.requirements.ilike(search_filter)
                )
            )
        
        # Ordonner par date de création (plus récent en premier)
        query = query.order_by(Job.created_at.desc())
        
        # Paginer
        jobs_paginated = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'jobs': [job.to_dict() for job in jobs_paginated.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': jobs_paginated.total,
                'pages': jobs_paginated.pages,
                'has_next': jobs_paginated.has_next,
                'has_prev': jobs_paginated.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@jobs_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Récupérer une offre d'emploi spécifique"""
    try:
        job = Job.query.get_or_404(job_id)
        
        if not job.is_active:
            return jsonify({
                'success': False,
                'error': 'Cette offre d\'emploi n\'est plus disponible'
            }), 404
        
        return jsonify({
            'success': True,
            'job': job.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@jobs_bp.route('/jobs/featured', methods=['GET'])
def get_featured_jobs():
    """Récupérer les offres d'emploi en vedette (pour le carrousel)"""
    try:
        # Limiter à 6 offres pour le carrousel
        limit = request.args.get('limit', 6, type=int)
        
        jobs = Job.query.filter(
            Job.is_active == True,
            Job.salary_max <= 3500  # Filtrer par salaire max de 3500€
        ).order_by(Job.created_at.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'jobs': [job.to_dict() for job in jobs]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@jobs_bp.route('/jobs/stats', methods=['GET'])
def get_jobs_stats():
    """Récupérer les statistiques des offres d'emploi"""
    try:
        total_jobs = Job.query.filter(Job.is_active == True).count()
        total_applications = Application.query.count()
        
        # Statistiques par département
        departments = db.session.query(
            Job.department, 
            db.func.count(Job.id).label('count')
        ).filter(Job.is_active == True).group_by(Job.department).all()
        
        # Statistiques par localisation
        locations = db.session.query(
            Job.location, 
            db.func.count(Job.id).label('count')
        ).filter(Job.is_active == True).group_by(Job.location).all()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_jobs': total_jobs,
                'total_applications': total_applications,
                'departments': [{'name': dept, 'count': count} for dept, count in departments],
                'locations': [{'name': loc, 'count': count} for loc, count in locations]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

