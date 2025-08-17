#!/usr/bin/env python3
"""
Script pour populer la base de données avec des offres d'emploi Google en français
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.models.job import Job, db

def create_sample_jobs():
    """Créer des offres d'emploi d'exemple"""
    
    jobs_data = [
        {
            'title': 'Ingénieur Logiciel Senior',
            'description': '''Rejoignez notre équipe d'ingénierie pour développer des produits innovants utilisés par des milliards d'utilisateurs dans le monde entier. Vous travaillerez sur des projets passionnants utilisant les dernières technologies et contribuerez à façonner l'avenir de la technologie.

Responsabilités:
• Concevoir et développer des applications web et mobiles à grande échelle
• Collaborer avec des équipes multidisciplinaires pour livrer des produits de qualité
• Optimiser les performances et la scalabilité des systèmes existants
• Mentorer les développeurs juniors et contribuer à la culture technique

Environnement de travail:
Vous évoluerez dans un environnement stimulant avec accès aux dernières technologies, formations continues et opportunités de croissance professionnelle.''',
            'requirements': '''Qualifications requises:
• Master en informatique ou équivalent
• 5+ années d'expérience en développement logiciel
• Expertise en Python, Java ou C++
• Expérience avec les architectures distribuées
• Maîtrise des bases de données relationnelles et NoSQL

Qualifications souhaitées:
• Expérience avec Google Cloud Platform
• Connaissance des méthodologies Agile/Scrum
• Contributions open source
• Expérience en machine learning''',
            'salary_min': 2800,
            'salary_max': 3500,
            'location': 'Paris, France',
            'department': 'Engineering',
            'employment_type': 'CDI',
            'benefits': '''Avantages:
• Salaire compétitif avec bonus annuel
• Assurance santé premium
• 25 jours de congés payés + RTT
• Télétravail hybride (3 jours/semaine)
• Formation continue et certifications
• Restaurant d'entreprise gratuit
• Salle de sport et cours de yoga
• Transport remboursé à 100%'''
        },
        {
            'title': 'Data Scientist',
            'description': '''Transformez les données en insights précieux pour améliorer nos produits et services. Vous analyserez des téraoctets de données pour découvrir des tendances et développer des modèles prédictifs.

Missions principales:
• Analyser de grands volumes de données pour identifier des opportunités
• Développer des modèles de machine learning pour améliorer nos algorithmes
• Créer des tableaux de bord et visualisations pour les équipes métier
• Collaborer avec les équipes produit pour définir les métriques clés

Impact:
Vos analyses influenceront directement les décisions stratégiques et l'amélioration de l'expérience utilisateur pour des millions d'utilisateurs.''',
            'requirements': '''Profil recherché:
• Master/PhD en statistiques, mathématiques ou informatique
• 3+ années d'expérience en data science
• Expertise en Python/R et SQL
• Maîtrise des frameworks ML (TensorFlow, PyTorch)
• Expérience avec BigQuery, Hadoop ou Spark

Compétences appréciées:
• Expérience en deep learning
• Connaissance des méthodes statistiques avancées
• Capacité à communiquer des insights complexes
• Expérience en A/B testing''',
            'salary_min': 2500,
            'salary_max': 3200,
            'location': 'Paris, France',
            'department': 'Data & Analytics',
            'employment_type': 'CDI',
            'benefits': '''Package complet:
• Rémunération attractive avec equity
• Mutuelle famille prise en charge
• Congés illimités (minimum 25 jours)
• Budget formation de 3000€/an
• Équipement informatique haut de gamme
• Crèche d'entreprise
• Conciergerie d'entreprise
• Événements team building réguliers'''
        },
        {
            'title': 'Chef de Produit Digital',
            'description': '''Dirigez la stratégie produit pour nos applications mobiles utilisées par des millions d'utilisateurs. Vous définirez la vision produit et coordonnerez les équipes techniques pour livrer des expériences exceptionnelles.

Responsabilités clés:
• Définir la roadmap produit en collaboration avec les stakeholders
• Analyser les besoins utilisateurs et les tendances du marché
• Coordonner les équipes design, engineering et marketing
• Suivre les KPIs et optimiser les performances produit

Évolution:
Opportunité d'évoluer vers un poste de VP Product dans nos bureaux internationaux.''',
            'requirements': '''Expérience requise:
• 4+ années en product management
• MBA ou formation équivalente
• Expérience avec les méthodologies Lean/Agile
• Maîtrise des outils d'analytics (Google Analytics, Mixpanel)
• Anglais courant (environnement international)

Qualités recherchées:
• Leadership naturel et capacité à fédérer
• Orientation data-driven
• Créativité et vision stratégique
• Excellente communication écrite et orale''',
            'salary_min': 3000,
            'salary_max': 3500,
            'location': 'Paris, France',
            'department': 'Product',
            'employment_type': 'CDI',
            'benefits': '''Avantages premium:
• Package salarial très compétitif
• Stock options avec potentiel élevé
• Flexibilité totale sur les horaires
• Budget voyage pour conférences internationales
• Coaching professionnel personnalisé
• Abonnement premium aux plateformes d'apprentissage
• Véhicule de fonction ou budget mobilité
• Participation aux bénéfices'''
        },
        {
            'title': 'Spécialiste Marketing Digital',
            'description': '''Développez et exécutez des campagnes marketing innovantes pour promouvoir nos produits auprès de millions d'utilisateurs. Vous utiliserez les derniers outils et techniques pour maximiser l'engagement et la conversion.

Missions:
• Créer et optimiser des campagnes publicitaires multi-canaux
• Analyser les performances et ROI des campagnes
• Développer le contenu marketing (vidéos, articles, infographies)
• Gérer les réseaux sociaux et la communauté en ligne

Créativité:
Liberté totale pour expérimenter avec de nouveaux formats et canaux marketing.''',
            'requirements': '''Profil idéal:
• 3+ années en marketing digital
• Maîtrise de Google Ads, Facebook Ads, LinkedIn Ads
• Expérience en SEO/SEM et marketing automation
• Compétences en design (Photoshop, Figma)
• Excellente maîtrise du français et de l'anglais

Atouts supplémentaires:
• Expérience en growth hacking
• Connaissance des outils d'analytics avancés
• Créativité et sens artistique développé
• Expérience en marketing d'influence''',
            'salary_min': 2200,
            'salary_max': 2800,
            'location': 'Lyon, France',
            'department': 'Marketing',
            'employment_type': 'CDI',
            'benefits': '''Environnement stimulant:
• Salaire évolutif selon performance
• Bonus trimestriels sur objectifs
• Télétravail jusqu'à 4 jours/semaine
• Budget créatif pour vos projets
• Accès aux événements marketing premium
• Formation continue en marketing digital
• Tickets restaurant et transport
• Ambiance startup dans un grand groupe'''
        },
        {
            'title': 'Ingénieur DevOps',
            'description': '''Automatisez et optimisez notre infrastructure cloud pour supporter des millions d'utilisateurs simultanés. Vous travaillerez sur des systèmes à très grande échelle avec les technologies les plus avancées.

Défis techniques:
• Gérer une infrastructure multi-cloud (GCP, AWS, Azure)
• Automatiser les déploiements avec CI/CD
• Optimiser les performances et la disponibilité
• Implémenter la sécurité et la conformité

Innovation:
Vous contribuerez à développer des outils internes utilisés par toute l'organisation.''',
            'requirements': '''Compétences techniques:
• 4+ années d'expérience en DevOps/SRE
• Maîtrise de Kubernetes, Docker, Terraform
• Expérience avec les clouds publics (GCP préféré)
• Scripting avancé (Python, Bash, Go)
• Connaissance des outils de monitoring (Prometheus, Grafana)

Expertise souhaitée:
• Certification cloud (GCP, AWS, Azure)
• Expérience en sécurité infrastructure
• Connaissance des pratiques GitOps
• Expérience avec les bases de données distribuées''',
            'salary_min': 2600,
            'salary_max': 3300,
            'location': 'Paris, France',
            'department': 'Infrastructure',
            'employment_type': 'CDI',
            'benefits': '''Package technique:
• Rémunération top marché
• Budget hardware illimité
• Formations et certifications payées
• Conférences techniques internationales
• Horaires flexibles total
• Équipe technique de haut niveau
• Projets open source encouragés
• Sabbatique payé après 5 ans'''
        },
        {
            'title': 'UX/UI Designer Senior',
            'description': '''Créez des expériences utilisateur exceptionnelles pour nos applications utilisées quotidiennement par des millions de personnes. Vous définirez les standards de design et influencerez l'avenir de nos interfaces.

Responsabilités créatives:
• Concevoir des interfaces intuitives et esthétiques
• Réaliser des recherches utilisateur et tests d'usabilité
• Créer des prototypes interactifs et wireframes
• Collaborer étroitement avec les équipes produit et engineering

Impact:
Vos créations amélioreront directement l'expérience de millions d'utilisateurs dans le monde.''',
            'requirements': '''Portfolio requis:
• 5+ années d'expérience en UX/UI design
• Portfolio démontrant des projets web et mobile
• Maîtrise de Figma, Sketch, Adobe Creative Suite
• Expérience en design system et atomic design
• Connaissance des principes d'accessibilité (WCAG)

Compétences valorisées:
• Expérience en recherche utilisateur
• Notions de front-end (HTML/CSS/JS)
• Animation et micro-interactions
• Design thinking et méthodologies agiles''',
            'salary_min': 2400,
            'salary_max': 3100,
            'location': 'Paris, France',
            'department': 'Design',
            'employment_type': 'CDI',
            'benefits': '''Environnement créatif:
• Salaire compétitif + bonus créatif
• Budget matériel design illimité
• Studio de création avec dernières technologies
• Formations design et conférences
• Flexibilité créative totale
• Collaboration avec designers mondiaux
• Exposition internationale de vos créations
• Congés créatifs pour inspiration'''
        }
    ]
    
    with app.app_context():
        # Supprimer les jobs existants
        Job.query.delete()
        
        # Créer les nouveaux jobs
        for job_data in jobs_data:
            job = Job(**job_data)
            db.session.add(job)
        
        db.session.commit()
        print(f"✅ {len(jobs_data)} offres d'emploi créées avec succès!")

if __name__ == '__main__':
    create_sample_jobs()

