from flask import Blueprint, render_template, request, jsonify, session, abort, redirect, url_for
from app.controllers.LoginController import reqlogged
from app.models.LecteurDAO import LecteurDAO
from app.services.access_control import require_permission
from app.services.permissions import normalize_role, get_role_permissions
import sqlite3
from app import app

musique_bp = Blueprint("musique", __name__, url_prefix="/musique")
dao = LecteurDAO()


def get_permissions(role):
    """Retourne les permissions de contrôle musical selon le rôle."""
    role = normalize_role(role)
    perms = get_role_permissions(role)

    if role == "admin":
        return {
            "can_play": True,
            "can_pause": True,
            "can_control_volume": True,
            "can_skip": True,
            "can_control_multiple": True,
        }

    if perms.get("control_music"):
        return {
            "can_play": True,
            "can_pause": True,
            "can_control_volume": True,
            "can_skip": True,
            "can_control_multiple": True,
        }

    return {
        "can_play": False,
        "can_pause": False,
        "can_control_volume": False,
        "can_skip": False,
        "can_control_multiple": False,
    }


def get_zones(lecteurs):
    zones = set()
    for lecteur in lecteurs:
        if lecteur.adresse_lecteur:
            zones.add(lecteur.adresse_lecteur)
    return sorted(list(zones))


def get_sites(lecteurs):
    db_path = app.root_path + '/database.db'
    sites = {}
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        for lecteur in lecteurs:
            if hasattr(lecteur, 'id_organisation'):
                cursor = conn.execute(
                    "SELECT id_organisation, nom_organisation FROM Organisation WHERE id_organisation = ?",
                    (lecteur.id_organisation,)
                )
                org = cursor.fetchone()
                if org and org['id_organisation'] not in sites:
                    sites[org['id_organisation']] = org['nom_organisation']
        conn.close()
    except Exception:
        for lecteur in lecteurs:
            if lecteur.adresse_lecteur:
                site_id = f"site_{lecteur.adresse_lecteur}"
                if site_id not in sites:
                    sites[site_id] = f"Site {lecteur.adresse_lecteur}"
    return sites


@musique_bp.route("/", methods=['GET'])
@reqlogged
@require_permission("control_music", "view_lecteur_status", "choose_slot")
def musique():
    role = normalize_role(session.get("role", "commercial"))
    permissions = get_permissions(role)

    lecteurs = dao.find_all()
    zones = get_zones(lecteurs)
    sites = get_sites(lecteurs)
    lecteur_actif = lecteurs[0] if lecteurs else None

    piste_actuelle = {
        "titre": "Ambiance Matin",
        "artiste": "Playlist d'ambiance",
        "duree": "3:45",
        "position": "1:20",
        "lecteur_id": lecteur_actif.id_lecteur if lecteur_actif else None,
        "lecteur_nom": lecteur_actif.nom_lecteur if lecteur_actif else "Aucun lecteur"
    }

    programmation = {
        "en_cours": {
            "playlist": "Ambiance Matin",
            "heure_debut": "08:00",
            "heure_fin": "12:00"
        },
        "prevue": {
            "playlist": "Ambiance Après-midi",
            "heure_debut": "12:00",
            "heure_fin": "18:00"
        }
    }

    metadata = {"title": "Contrôle Musical", "pagename": "musique"}
    return render_template(
        "musique.html",
        metadata=metadata,
        lecteurs=lecteurs,
        zones=zones,
        sites=sites,
        permissions=permissions,
        piste_actuelle=piste_actuelle,
        programmation=programmation,
        role=role,
        readonly=not permissions["can_play"],
    )


@musique_bp.route("/control", methods=['POST'])
@reqlogged
@require_permission("control_music")
def control():
    role = normalize_role(session.get("role", "commercial"))
    permissions = get_permissions(role)

    data = request.get_json()
    action = data.get("action")
    target_type = data.get("target_type")
    target_id = data.get("target_id")

    if action in ["prev", "next"] and not permissions["can_skip"]:
        return jsonify({"success": False, "error": "Permission refusée"}), 403

    if action == "volume" and not permissions["can_control_volume"]:
        return jsonify({"success": False, "error": "Permission refusée"}), 403

    lecteurs_cibles = []
    if target_type == "lecteur":
        lecteur = dao.find_one(target_id)
        if lecteur:
            lecteurs_cibles = [lecteur]
    elif target_type == "zone":
        all_lecteurs = dao.find_all()
        lecteurs_cibles = [l for l in all_lecteurs if l.adresse_lecteur == target_id]
    elif target_type == "site":
        lecteurs_cibles = dao.find_all()

    results = []
    for lecteur in lecteurs_cibles:
        if lecteur.est_en_ligne():
            results.append({
                "lecteur_id": lecteur.id_lecteur,
                "lecteur_nom": lecteur.nom_lecteur,
                "success": True,
                "action": action
            })
        else:
            results.append({
                "lecteur_id": lecteur.id_lecteur,
                "lecteur_nom": lecteur.nom_lecteur,
                "success": False,
                "error": "Hors ligne"
            })

    en_ligne = [r for r in results if r["success"]]
    desynchronise = len(en_ligne) < len(lecteurs_cibles)

    return jsonify({
        "success": True,
        "results": results,
        "synchronized": not desynchronise,
        "en_ligne": len(en_ligne),
        "total": len(lecteurs_cibles)
    })


@musique_bp.route("/status", methods=['POST'])
@reqlogged
@require_permission("control_music", "view_lecteur_status")
def get_status():
    data = request.get_json()
    target_type = data.get("target_type")
    target_id = data.get("target_id")

    lecteurs_cibles = []
    if target_type == "lecteur":
        lecteur = dao.find_one(target_id)
        if lecteur:
            lecteurs_cibles = [lecteur]
    elif target_type == "zone":
        all_lecteurs = dao.find_all()
        lecteurs_cibles = [l for l in all_lecteurs if l.adresse_lecteur == target_id]
    elif target_type == "site":
        lecteurs_cibles = dao.find_all()

    status_list = []
    for lecteur in lecteurs_cibles:
        status_list.append({
            "lecteur_id": lecteur.id_lecteur,
            "lecteur_nom": lecteur.nom_lecteur,
            "en_ligne": lecteur.est_en_ligne(),
            "derniere_synchro": lecteur.derniere_synchro,
            "piste": "Ambiance Matin",
            "position": "1:20"
        })

    en_ligne = [s for s in status_list if s["en_ligne"]]
    synchronized = len(en_ligne) == len(status_list) and len(status_list) > 0

    return jsonify({
        "status_list": status_list,
        "synchronized": synchronized,
        "en_ligne": len(en_ligne),
        "total": len(status_list)
    })
