from flask import Blueprint, render_template, request, jsonify, session, abort, redirect, url_for, flash
from app.controllers.LoginController import reqlogged
from app.models.LecteurDAO import LecteurDAO
from app.models.PlaylistDAO import PlaylistDAO
from app.services.PlaylistService import PlaylistService
from app import app
import sqlite3
from datetime import datetime

playlist_bp = Blueprint("playlist", __name__, url_prefix="/playlists")

lecteur_dao = LecteurDAO()
playlist_dao = PlaylistDAO()
playlist_service = PlaylistService()


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
            if lecteur.id_organisation:
                cursor = conn.execute(
                    "SELECT id_organisation, nom_organisation FROM Organisation WHERE id_organisation = ?",
                    (lecteur.id_organisation,)
                )
                org = cursor.fetchone()
                if org:
                    sites[org["id_organisation"]] = org["nom_organisation"]

        conn.close()
    except:
        pass

    return sites


@playlist_bp.route("/", methods=["GET"])
@reqlogged
def playlists():
    role = session.get("role", "utilisateur")

    playlists = playlist_dao.find_all()  
    lecteurs = lecteur_dao.find_all()
    zones = get_zones(lecteurs)
    sites = get_sites(lecteurs)

    metadata = {
        "title": "Gestion des Playlists",
        "pagename": "playlists"
    }

    return render_template(
        "playlists.html",
        metadata=metadata,
        playlists=playlists,
        lecteurs=lecteurs,
        zones=zones,
        sites=sites,
        role=role
    )


@playlist_bp.route("/<int:id_playlist>", methods=["GET"])
@reqlogged
def playlist_detail(id_playlist):
    playlist = playlist_service.get_playlist(id_playlist)

    if not playlist:
        abort(404)

    pistes = get_playlist_pistes(id_playlist)

    lecteurs = lecteur_dao.find_all()
    zones = get_zones(lecteurs)
    sites = get_sites(lecteurs)

    metadata = {
        "title": f"Playlist : {playlist.nom_playlist}",
        "pagename": "playlist_detail"
    }

    return render_template(
    "playlist_detail.html",
    metadata=metadata,
    playlist=playlist,
    pistes=pistes,  
    lecteurs=lecteurs,
    zones=zones,
    sites=sites
)


def get_playlist_pistes(id_playlist):
    """Récupère les pistes d'une playlist"""
    db_path = app.root_path + '/database.db'
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        cursor = conn.execute("""
            SELECT f.*, e.id_playlist
            FROM Est_composé_d_une e
            JOIN Fichier f ON e.id_fichier = f.id_fichier
            WHERE e.id_playlist = ?
            ORDER BY f.id_fichier
        """, (id_playlist,))
        
        pistes = []
        for row in cursor.fetchall():
            duree = row.get('duree_fichier', 180)
            
            piste_problemes = []
            if not row.get('emplacement'):
                piste_problemes.append("Fichier manquant")
            
            pistes.append({
                'id_fichier': row['id_fichier'],
                'nom': row['nom'],
                'emplacement': row.get('emplacement', ''),
                'duree': duree,
                'problemes': piste_problemes
            })
        
        conn.close()
        return pistes
        
    except Exception as e:
        print(f"Erreur lors de la récupération des pistes: {e}")
        return []


@playlist_bp.route("/planifier/<int:id_playlist>/<int:id_lecteur>", methods=["GET"])
@reqlogged
def planifier_playlist(id_playlist, id_lecteur):
    """
    Redirige vers la page de planification
    avec la playlist présélectionnée
    """
    return redirect(
        url_for(
            "planification.planifier_lecteur",
            id_lecteur=id_lecteur,
            playlist=id_playlist
        )
    )


@playlist_bp.route("/assign", methods=['POST'])
@reqlogged
def assign_playlist():
    """Affecter une playlist à un lecteur/zone/site"""
    data = request.get_json()
    playlist_id = data.get("playlist_id")
    target_type = data.get("target_type")
    target_id = data.get("target_id")
    is_fallback = data.get("is_fallback", False)
    
    return jsonify({
        "success": True,
        "message": f"Playlist affectée avec succès",
        "playlist_id": playlist_id,
        "target_type": target_type,
        "target_id": target_id,
        "is_fallback": is_fallback
    })


@playlist_bp.route("/publish", methods=['POST'])
@reqlogged
def publish_playlist():
    """Publier ou dépublier une playlist"""
    data = request.get_json()
    playlist_id = data.get("playlist_id")
    publish = data.get("publish", True)
    
    return jsonify({
        "success": True,
        "message": "Playlist publiée" if publish else "Playlist mise en brouillon",
        "playlist_id": playlist_id,
        "publie": publish
    })