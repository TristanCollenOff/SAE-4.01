from flask import Blueprint, render_template, request, jsonify, session, abort, redirect, url_for
from app.controllers.LoginController import reqlogged
from app.models.LecteurDAO import LecteurDAO
from app.models.PlaylistDAO import PlaylistDAO
from app.services.PlaylistService import PlaylistService
from app import app
import sqlite3

playlist_bp = Blueprint("playlist", __name__, url_prefix="/playlists")

lecteur_dao = LecteurDAO()
playlist_dao = PlaylistDAO()
playlist_service = PlaylistService()


# -----------------------------
# SECURITE SUPERVISEUR
# -----------------------------
def check_superviseur():
    if not session.get("superviseur_ok"):
        return False
    return True


def require_superviseur():
    if not check_superviseur():
        return redirect(url_for("supervisor.supervisor_check"))

# -----------------------------
# ZONES
# -----------------------------
def get_zones(lecteurs):
    zones = set()
    for lecteur in lecteurs:
        if lecteur.adresse_lecteur:
            zones.add(lecteur.adresse_lecteur)
    return sorted(list(zones))


# -----------------------------
# SITES
# -----------------------------
def get_sites(lecteurs):
    db_path = app.root_path + '/database.db'
    sites = {}

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        for lecteur in lecteurs:
            if lecteur.id_organisation:
                cursor = conn.execute(
                    "SELECT id_organisation, nom_organisation FROM organisation WHERE id_organisation = ?",
                    (lecteur.id_organisation,)
                )
                org = cursor.fetchone()
                if org:
                    sites[org["id_organisation"]] = org["nom_organisation"]

        conn.close()
    except:
        pass

    return sites


# -----------------------------
# LIST PLAYLISTS
# -----------------------------
@playlist_bp.route("/", methods=["GET"])
@reqlogged
def playlists():

    # 🔐 SUPERVISEUR CHECK
    redirect_response = require_superviseur()
    if redirect_response:
        return redirect_response

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


# -----------------------------
# DETAIL PLAYLIST
# -----------------------------
@playlist_bp.route("/<int:id_playlist>", methods=["GET"])
@reqlogged
def playlist_detail(id_playlist):

    redirect_response = require_superviseur()
    if redirect_response:
        return redirect_response

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
        zones=sites
    )


# -----------------------------
# PISTES
# -----------------------------
def get_playlist_pistes(id_playlist):

    db_path = app.root_path + '/database.db'

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        cursor = conn.execute("""
            SELECT f.*, c.id_playlist
            FROM Contenir c
            JOIN fichier f ON c.id_fichier = f.id_fichier
            WHERE c.id_playlist = ?
            ORDER BY f.id_fichier
        """, (id_playlist,))

        pistes = []

        for row in cursor.fetchall():
            duree = row.get('duree_fichier', 180)

            pistes.append({
                'id_fichier': row['id_fichier'],
                'nom': row['nom'],
                'emplacement': row.get("chemin"),
                'duree': duree
            })

        conn.close()
        return pistes

    except Exception as e:
        print(e)
        return []