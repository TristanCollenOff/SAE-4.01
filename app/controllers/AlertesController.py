from flask import Blueprint, render_template, request, jsonify, session
from app.controllers.LoginController import reqlogged
from app.models.LecteurDAO import LecteurDAO
from datetime import datetime, timedelta
import random

alertes_bp = Blueprint("alertes", __name__, url_prefix="/alertes")
dao = LecteurDAO()

# Types d'incidents
INCIDENT_TYPES = {
    'lecteur_down': {
        'nom': 'Lecteur DOWN',
        'icone': 'bi-x-circle-fill',
        'couleur': '#dc3545',
        'gravite_defaut': 'critique'
    },
    'desynchronisation': {
        'nom': 'Désynchronisation',
        'icone': 'bi-clock-history',
        'couleur': '#ffc107',
        'gravite_defaut': 'moyenne'
    },
    'musique_absente': {
        'nom': 'Musique absente / Silence',
        'icone': 'bi-volume-mute-fill',
        'couleur': '#ff9800',
        'gravite_defaut': 'haute'
    },
    'playlist_incorrecte': {
        'nom': 'Playlist incorrecte',
        'icone': 'bi-file-earmark-music',
        'couleur': '#17a2b8',
        'gravite_defaut': 'moyenne'
    },
    'volume_hors_limites': {
        'nom': 'Volume hors limites',
        'icone': 'bi-volume-up',
        'couleur': '#ffc107',
        'gravite_defaut': 'basse'
    }
}

GRAVITES = {
    'critique': {'nom': 'Critique', 'couleur': '#dc3545', 'ordre': 4},
    'haute': {'nom': 'Haute', 'couleur': '#ff9800', 'ordre': 3},
    'moyenne': {'nom': 'Moyenne', 'couleur': '#ffc107', 'ordre': 2},
    'basse': {'nom': 'Basse', 'couleur': '#17a2b8', 'ordre': 1}
}

ETATS = ['ouvert', 'en_cours', 'resolu', 'ignore']

def detecter_incidents():
    """Détecte les incidents à partir de l'état des lecteurs"""
    incidents = []
    lecteurs = dao.find_all()
    
    for lecteur in lecteurs:
        # Détection lecteur DOWN
        if not lecteur.est_en_ligne():
            incidents.append({
                'id': f"inc_{lecteur.id_lecteur}_down_{int(datetime.now().timestamp())}",
                'type': 'lecteur_down',
                'gravite': 'critique',
                'titre': f'Lecteur {lecteur.nom_lecteur} hors ligne',
                'description': f'Le lecteur {lecteur.nom_lecteur} ({lecteur.adresseIP}) n\'est plus accessible.',
                'zone_impactee': lecteur.adresse_lecteur or 'Non assigné',
                'lecteurs_impactes': [lecteur.nom_lecteur],
                'lecteurs_ids': [lecteur.id_lecteur],
                'debut': datetime.now() - timedelta(minutes=random.randint(5, 120)),
                'etat': 'ouvert',
                'assigne_a': None,
                'commentaires': [],
                'evenements': [
                    {
                        'date': datetime.now() - timedelta(minutes=random.randint(5, 120)),
                        'type': 'detection',
                        'message': f'Perte de connexion détectée pour {lecteur.nom_lecteur}'
                    }
                ]
            })
        
        # Détection désynchronisation (simulée)
        if lecteur.est_en_ligne() and random.random() < 0.1:  # 10% de chance
            incidents.append({
                'id': f"inc_{lecteur.id_lecteur}_desync_{int(datetime.now().timestamp())}",
                'type': 'desynchronisation',
                'gravite': 'moyenne',
                'titre': f'Désynchronisation détectée - {lecteur.nom_lecteur}',
                'description': f'Le lecteur {lecteur.nom_lecteur} présente une dérive de synchronisation de {random.randint(5, 30)} secondes.',
                'zone_impactee': lecteur.adresse_lecteur or 'Non assigné',
                'lecteurs_impactes': [lecteur.nom_lecteur],
                'lecteurs_ids': [lecteur.id_lecteur],
                'debut': datetime.now() - timedelta(minutes=random.randint(10, 60)),
                'etat': 'ouvert',
                'assigne_a': None,
                'commentaires': [],
                'evenements': [
                    {
                        'date': datetime.now() - timedelta(minutes=random.randint(10, 60)),
                        'type': 'detection',
                        'message': f'Dérive de synchronisation détectée: {random.randint(5, 30)}s'
                    }
                ]
            })
        
        # Détection volume hors limites (simulée)
        if lecteur.est_en_ligne() and random.random() < 0.05:  # 5% de chance
            volume = random.choice([15, 95])  # Trop bas ou trop haut
            incidents.append({
                'id': f"inc_{lecteur.id_lecteur}_volume_{int(datetime.now().timestamp())}",
                'type': 'volume_hors_limites',
                'gravite': 'basse',
                'titre': f'Volume hors limites - {lecteur.nom_lecteur}',
                'description': f'Le volume du lecteur {lecteur.nom_lecteur} est à {volume}% (limites recommandées: 20-90%).',
                'zone_impactee': lecteur.adresse_lecteur or 'Non assigné',
                'lecteurs_impactes': [lecteur.nom_lecteur],
                'lecteurs_ids': [lecteur.id_lecteur],
                'debut': datetime.now() - timedelta(minutes=random.randint(30, 180)),
                'etat': 'ouvert',
                'assigne_a': None,
                'commentaires': [],
                'evenements': [
                    {
                        'date': datetime.now() - timedelta(minutes=random.randint(30, 180)),
                        'type': 'detection',
                        'message': f'Volume détecté hors limites: {volume}%'
                    }
                ]
            })
    
    # Détection musique absente (simulée pour quelques lecteurs)
    if random.random() < 0.3:  # 30% de chance d'avoir un incident de ce type
        lecteur_impacte = random.choice([l for l in lecteurs if l.est_en_ligne()]) if any(l.est_en_ligne() for l in lecteurs) else None
        if lecteur_impacte:
            incidents.append({
                'id': f"inc_{lecteur_impacte.id_lecteur}_silence_{int(datetime.now().timestamp())}",
                'type': 'musique_absente',
                'gravite': 'haute',
                'titre': f'Musique absente - {lecteur_impacte.nom_lecteur}',
                'description': f'Aucun signal audio détecté sur le lecteur {lecteur_impacte.nom_lecteur} depuis plusieurs minutes.',
                'zone_impactee': lecteur_impacte.adresse_lecteur or 'Non assigné',
                'lecteurs_impactes': [lecteur_impacte.nom_lecteur],
                'lecteurs_ids': [lecteur_impacte.id_lecteur],
                'debut': datetime.now() - timedelta(minutes=random.randint(15, 90)),
                'etat': 'ouvert',
                'assigne_a': None,
                'commentaires': [],
                'evenements': [
                    {
                        'date': datetime.now() - timedelta(minutes=random.randint(15, 90)),
                        'type': 'detection',
                        'message': 'Aucun signal audio détecté'
                    }
                ]
            })
    
    return incidents

def get_incidents():
    """Récupère tous les incidents (simulé - en production, depuis la DB)"""
    # En production, récupérer depuis la base de données
    # Pour la démo, on génère des incidents
    incidents = detecter_incidents()
    
    # Ajouter quelques incidents résolus pour l'historique
    incidents_resolus = [
        {
            'id': 'inc_resolu_1',
            'type': 'playlist_incorrecte',
            'gravite': 'moyenne',
            'titre': 'Playlist incorrecte - Zone Réception',
            'description': 'La playlist assignée contenait des fichiers manquants.',
            'zone_impactee': 'Réception',
            'lecteurs_impactes': ['Lecteur Réception 1', 'Lecteur Réception 2'],
            'lecteurs_ids': [1, 2],
            'debut': datetime.now() - timedelta(hours=5),
            'resolu_le': datetime.now() - timedelta(hours=2),
            'etat': 'resolu',
            'assigne_a': 'admin',
            'commentaires': [
                {
                    'date': datetime.now() - timedelta(hours=2),
                    'user': 'admin',
                    'texte': 'Playlist corrigée et resynchronisée'
                }
            ],
            'evenements': [
                {
                    'date': datetime.now() - timedelta(hours=5),
                    'type': 'detection',
                    'message': 'Fichiers manquants détectés dans la playlist'
                },
                {
                    'date': datetime.now() - timedelta(hours=4),
                    'type': 'action',
                    'user': 'admin',
                    'message': 'Incident assigné à admin'
                },
                {
                    'date': datetime.now() - timedelta(hours=2),
                    'type': 'resolution',
                    'user': 'admin',
                    'message': 'Playlist corrigée et resynchronisée'
                }
            ]
        }
    ]
    
    return incidents + incidents_resolus

@alertes_bp.route("/", methods=['GET'])
@reqlogged
def alertes():
    """Page principale des alertes"""
    role = session.get("role", "utilisateur")
    username = session.get("username", "user")
    
    # Récupérer les incidents
    all_incidents = get_incidents()
    
    # Filtrer selon l'état demandé
    filtre_etat = request.args.get('etat', 'tous')
    if filtre_etat != 'tous':
        all_incidents = [inc for inc in all_incidents if inc['etat'] == filtre_etat]
    
    # Filtrer selon le type
    filtre_type = request.args.get('type', 'tous')
    if filtre_type != 'tous':
        all_incidents = [inc for inc in all_incidents if inc['type'] == filtre_type]
    
    # Filtrer selon la gravité
    filtre_gravite = request.args.get('gravite', 'tous')
    if filtre_gravite != 'tous':
        all_incidents = [inc for inc in all_incidents if inc['gravite'] == filtre_gravite]
    
    # Trier par gravité puis par date
    all_incidents.sort(key=lambda x: (
        GRAVITES[x['gravite']]['ordre'],
        x['debut']
    ), reverse=True)
    
    # Statistiques
    stats = {
        'total': len(get_incidents()),
        'ouverts': len([i for i in get_incidents() if i['etat'] == 'ouvert']),
        'en_cours': len([i for i in get_incidents() if i['etat'] == 'en_cours']),
        'resolus': len([i for i in get_incidents() if i['etat'] == 'resolu']),
        'critiques': len([i for i in get_incidents() if i['gravite'] == 'critique' and i['etat'] != 'resolu'])
    }
    
    metadata = {"title": "Gestion des Alertes", "pagename": "alertes"}
    return render_template(
        "alertes.html",
        metadata=metadata,
        incidents=all_incidents,
        incident_types=INCIDENT_TYPES,
        gravites=GRAVITES,
        stats=stats,
        role=role,
        username=username
    )

@alertes_bp.route("/<incident_id>", methods=['GET'])
@reqlogged
def alerte_detail(incident_id):
    """Vue détaillée d'un incident"""
    role = session.get("role", "utilisateur")
    username = session.get("username", "user")
    
    # Récupérer l'incident
    all_incidents = get_incidents()
    incident = next((inc for inc in all_incidents if inc['id'] == incident_id), None)
    
    if not incident:
        from flask import abort
        abort(404)
    
    metadata = {"title": f"Incident: {incident['titre']}", "pagename": "alerte_detail"}
    return render_template(
        "alerte_detail.html",
        metadata=metadata,
        incident=incident,
        incident_types=INCIDENT_TYPES,
        gravites=GRAVITES,
        role=role,
        username=username
    )

@alertes_bp.route("/action", methods=['POST'])
@reqlogged
def incident_action():
    """Exécuter une action sur un incident"""
    data = request.get_json()
    incident_id = data.get("incident_id")
    action = data.get("action")  # reconnaitre, assigner, resoudre, ignorer
    commentaire = data.get("commentaire", "")
    username = session.get("username", "user")
    
    # En production, mettre à jour dans la DB
    # Pour la démo, on simule
    
    messages = {
        'reconnaitre': 'Incident reconnu',
        'assigner': f'Incident assigné à {username}',
        'resoudre': 'Incident résolu',
        'ignorer': 'Incident ignoré'
    }
    
    return jsonify({
        "success": True,
        "message": messages.get(action, "Action exécutée"),
        "incident_id": incident_id,
        "action": action,
        "user": username
    })
