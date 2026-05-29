from flask import Blueprint, render_template, request, jsonify, session, abort
from app.controllers.LoginController import reqlogged
from app.models.LecteurDAO import LecteurDAO
import sqlite3
import os
from app import app
from datetime import datetime

sites_zones_bp = Blueprint("sites_zones", __name__, url_prefix="/sites-zones")
dao = LecteurDAO()

def get_zones_from_db():
    """Récupère les zones depuis la base de données"""
    db_path = app.root_path + '/database.db'
    zones = {}
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        # Récupérer tous les lecteurs avec leurs zones
        cursor = conn.execute("SELECT DISTINCT adresse_lecteur FROM Lecteur WHERE adresse_lecteur IS NOT NULL AND adresse_lecteur != ''")
        zone_names = [row[0] for row in cursor.fetchall()]
        
        for zone_name in zone_names:
            # Récupérer les lecteurs de cette zone
            cursor_lecteurs = conn.execute(
                "SELECT * FROM Lecteur WHERE adresse_lecteur = ?",
                (zone_name,)
            )
            lecteurs_data = cursor_lecteurs.fetchall()
            
            # Calculer le statut global
            en_ligne = 0
            hors_ligne = 0
            derniere_synchro = None
            
            for lecteur_row in lecteurs_data:
                # Simuler est_en_ligne (logique simplifiée)
                derniere_synchro_lecteur = lecteur_row.get('derniere_synchro')
                if derniere_synchro_lecteur and derniere_synchro_lecteur != 'Jamais':
                    en_ligne += 1
                    if not derniere_synchro or derniere_synchro_lecteur > derniere_synchro:
                        derniere_synchro = derniere_synchro_lecteur
                else:
                    hors_ligne += 1
            
            # Déterminer le statut global
            if hors_ligne == 0 and en_ligne > 0:
                statut_global = "OK"
            elif hors_ligne > 0 and en_ligne > 0:
                statut_global = "incidents"
            else:
                statut_global = "down"
            
            zones[zone_name] = {
                'nom': zone_name,
                'nb_lecteurs': len(lecteurs_data),
                'en_ligne': en_ligne,
                'hors_ligne': hors_ligne,
                'statut_global': statut_global,
                'derniere_synchro': derniere_synchro or "Jamais",
                'archived': False  # Simulé
            }
        
        conn.close()
    except Exception as e:
        print(f"Erreur lors de la récupération des zones: {e}")
        zones = {}
    
    return zones

def get_sites_from_db():
    """Récupère les sites depuis la base de données"""
    db_path = app.root_path + '/database.db'
    sites = {}
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        # Récupérer les organisations
        cursor = conn.execute("SELECT * FROM Organisation")
        orgs = cursor.fetchall()
        
        for org in orgs:
            # Récupérer les lecteurs de ce site
            cursor_lecteurs = conn.execute(
                "SELECT * FROM Lecteur WHERE id_organisation = ?",
                (org['id_organisation'],)
            )
            lecteurs_data = cursor_lecteurs.fetchall()
            
            # Calculer le statut global
            en_ligne = 0
            hors_ligne = 0
            zones_in_site = set()
            
            for lecteur_row in lecteurs_data:
                derniere_synchro_lecteur = lecteur_row.get('derniere_synchro')
                if derniere_synchro_lecteur and derniere_synchro_lecteur != 'Jamais':
                    en_ligne += 1
                else:
                    hors_ligne += 1
                
                if lecteur_row.get('adresse_lecteur'):
                    zones_in_site.add(lecteur_row['adresse_lecteur'])
            
            # Déterminer le statut global
            if hors_ligne == 0 and en_ligne > 0:
                statut_global = "OK"
            elif hors_ligne > 0 and en_ligne > 0:
                statut_global = "incidents"
            else:
                statut_global = "down"
            
            sites[org['id_organisation']] = {
                'id': org['id_organisation'],
                'nom': org['nom_organisation'],
                'nb_lecteurs': len(lecteurs_data),
                'nb_zones': len(zones_in_site),
                'en_ligne': en_ligne,
                'hors_ligne': hors_ligne,
                'statut_global': statut_global,
                'zones': list(zones_in_site),
                'archived': False  # Simulé
            }
        
        conn.close()
    except Exception as e:
        print(f"Erreur lors de la récupération des sites: {e}")
        # Données de démo
        sites = {
            1: {
                'id': 1,
                'nom': 'Site Principal',
                'nb_lecteurs': 5,
                'nb_zones': 3,
                'en_ligne': 4,
                'hors_ligne': 1,
                'statut_global': 'incidents',
                'zones': ['Hall Principal', 'Couloir Nord', 'Salle de réunion'],
                'archived': False
            }
        }
    
    return sites

def get_lecteurs_by_zone(zone_name):
    """Récupère les lecteurs d'une zone"""
    all_lecteurs = dao.find_all()
    return [l for l in all_lecteurs if l.adresse_lecteur == zone_name]

def get_lecteurs_by_site(site_id):
    """Récupère les lecteurs d'un site"""
    all_lecteurs = dao.find_all()
    # Simplifié : on retourne tous les lecteurs pour la démo
    return all_lecteurs

@sites_zones_bp.route("/", methods=['GET'])
@reqlogged
def sites_zones():
    """Page principale de gestion des sites et zones"""
    role = session.get("role", "utilisateur")
    
    # Récupérer les données
    sites = get_sites_from_db()
    zones = get_zones_from_db()
    all_lecteurs = dao.find_all()
    
    # Organiser les lecteurs par zone
    lecteurs_par_zone = {}
    for zone_name, zone_data in zones.items():
        lecteurs_par_zone[zone_name] = get_lecteurs_by_zone(zone_name)
    
    metadata = {"title": "Gestion Sites & Zones", "pagename": "sites_zones"}
    return render_template(
        "sites_zones.html",
        metadata=metadata,
        sites=sites,
        zones=zones,
        lecteurs_par_zone=lecteurs_par_zone,
        all_lecteurs=all_lecteurs,
        role=role
    )

@sites_zones_bp.route("/create-site", methods=['POST'])
@reqlogged
def create_site():
    """Créer un nouveau site"""
    data = request.get_json()
    nom_site = data.get("nom")
    
    # Logique de création (simulée)
    # En production, insérer dans la base de données
    
    return jsonify({
        "success": True,
        "message": f"Site '{nom_site}' créé avec succès",
        "site_id": 999  # Simulé
    })

@sites_zones_bp.route("/create-zone", methods=['POST'])
@reqlogged
def create_zone():
    """Créer une nouvelle zone"""
    data = request.get_json()
    nom_zone = data.get("nom")
    site_id = data.get("site_id")
    
    # Logique de création (simulée)
    
    return jsonify({
        "success": True,
        "message": f"Zone '{nom_zone}' créée avec succès"
    })

@sites_zones_bp.route("/assign-lecteur", methods=['POST'])
@reqlogged
def assign_lecteur():
    """Assigner un lecteur à une zone"""
    data = request.get_json()
    lecteur_id = data.get("lecteur_id")
    zone_name = data.get("zone_name")
    
    # Logique d'assignation (simulée)
    # En production, mettre à jour adresse_lecteur dans la base
    
    return jsonify({
        "success": True,
        "message": f"Lecteur assigné à la zone '{zone_name}'"
    })

@sites_zones_bp.route("/group-action", methods=['POST'])
@reqlogged
def group_action():
    """Action groupée sur une zone ou un site"""
    data = request.get_json()
    action = data.get("action")  # playlist, volume, restart
    target_type = data.get("target_type")  # zone, site
    target_id = data.get("target_id")
    value = data.get("value")  # Pour volume, playlist_id, etc.
    
    # Logique d'action groupée (simulée)
    
    return jsonify({
        "success": True,
        "message": f"Action '{action}' appliquée à {target_type} '{target_id}'",
        "affected": 5  # Nombre de lecteurs affectés
    })
