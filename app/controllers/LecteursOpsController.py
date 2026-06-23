from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from app.controllers.LoginController import reqlogged
from app.models.LecteurDAO import LecteurDAO
from app.services.access_control import require_permission
from app.services.permissions import normalize_role
from app.services.log_service import add_log, LOG_TYPES
import sqlite3
import os
from datetime import datetime
from app import app

lecteurs_ops_bp = Blueprint("lecteurs_ops", __name__, url_prefix="/lecteurs-ops")
commercial_bp = Blueprint("commercial", __name__, url_prefix="/commercial")
dao = LecteurDAO()


def get_lecteur_health(lecteur):
    health = {'stabilite': 'bonne', 'down_frequents': False, 'derive_sync': 0, 'erreurs_recentes': [], 'uptime_percent': 98.5}
    if not lecteur.est_en_ligne():
        health.update({'stabilite': 'faible', 'down_frequents': True, 'uptime_percent': 85.2})
    return health


def get_lecteur_current_state(lecteur):
    return {'playlist_assignee': 'Ambiance Matin', 'volume': 75, 'mode': 'lecture', 'dernier_contact': lecteur.derniere_synchro}


@lecteurs_ops_bp.route("/", methods=['GET'])
@reqlogged
@require_permission("manage_lecteurs", "view_lecteur_status")
def lecteurs_ops():
    role = normalize_role(session.get("role", "commercial"))
    all_lecteurs = dao.find_all()
    lecteurs_enriched = [
        {'lecteur': l, 'health': get_lecteur_health(l), 'current_state': get_lecteur_current_state(l)}
        for l in all_lecteurs
    ]
    return render_template(
        "lecteurs_ops.html",
        metadata={"title": "État des lecteurs", "pagename": "lecteurs_ops"},
        lecteurs_enriched=lecteurs_enriched,
        role=role,
        readonly=role == "commercial",
    )


@commercial_bp.route("/", methods=["GET", "POST"])
@reqlogged
@require_permission("add_ad", "add_announcement", "plan_ad", "urgent_announcement")
def commercial_hub():
    role = normalize_role(session.get("role", "commercial"))
    lecteurs = dao.find_all()

    if request.method == "POST":
        action = request.form.get("action")
        id_lecteur = request.form.get("id_lecteur", type=int)
        titre = request.form.get("titre", "").strip()
        contenu_type = request.form.get("contenu_type", "publicite")

        if action == "urgent" and id_lecteur:
            return redirect(url_for("api_lancer_pub", id_lecteur=id_lecteur))

        if titre and id_lecteur:
            id_org = session.get("id_organisation", 1)
            label = "publicité" if contenu_type == "publicite" else "annonce"
            add_log(
                LOG_TYPES['INFO'],
                id_org,
                f"[{session.get('username', 'Commercial')}] a ajouté une {label} : {titre}",
            )
            flash(f"{label.capitalize()} « {titre} » enregistrée.", "success")
            return redirect(url_for("commercial.commercial_hub"))

    metadata = {"title": "Espace Commercial", "pagename": "commercial"}
    return render_template(
        "commercial.html",
        metadata=metadata,
        lecteurs=lecteurs,
        role=role,
    )


@app.route('/api/lancer_pub/<int:id_lecteur>')
@reqlogged
@require_permission("urgent_announcement", "add_ad")
def api_lancer_pub(id_lecteur):
    """Déclenche une annonce urgente sur un lecteur."""
    try:
        heure = datetime.now().hour
        if 6 <= heure < 11:
            fichier_pub = "pubmatin1.mp3"
        elif 11 <= heure < 18:
            fichier_pub = "pubmidi1.mp3"
        else:
            fichier_pub = "pubsoir1.mp3"

        db_path = os.path.join(app.root_path, "database.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE lecteur SET etat_lecteur = 'pub', emplacement = ? WHERE id_lecteur = ?",
            (fichier_pub, id_lecteur),
        )
        conn.commit()
        conn.close()

        id_org = session.get("id_organisation", 1)
        add_log(
            LOG_TYPES['INFO'],
            id_org,
            f"[{session.get('username', 'Commercial')}] a déclenché une annonce urgente sur le lecteur {id_lecteur}",
        )

        return jsonify({"status": "success", "message": f"Signal envoyé : {fichier_pub}", "fichier": fichier_pub})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/ping/<int:id_lecteur>')
def api_ping(id_lecteur):
    try:
        db_path = os.path.join(app.root_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT etat_lecteur, emplacement FROM lecteur WHERE id_lecteur = ?", (id_lecteur,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return jsonify({
                "statut": "success",
                "action": "play",
                "playlist": "matin",
                "volume": 75,
                "emplacement": row['emplacement']
            })
        return jsonify({"statut": "error", "message": "Lecteur introuvable"}), 404
    except Exception as e:
        return jsonify({"statut": "error", "message": str(e)}), 500


@app.route('/api/pub_terminee/<int:id_lecteur>')
def api_pub_terminee(id_lecteur):
    try:
        db_path = os.path.join(app.root_path, "database.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE lecteur SET etat_lecteur = 'ambiance' WHERE id_lecteur = ?", (id_lecteur,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
