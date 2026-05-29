from flask import Blueprint, render_template, request, jsonify, session, abort, redirect
from app.controllers.LoginController import reqlogged
from app.models.LecteurDAO import LecteurDAO
import sqlite3
import os
from app import app
from datetime import datetime, timedelta

# Ton Blueprint
lecteurs_ops_bp = Blueprint("lecteurs_ops", __name__, url_prefix="/lecteurs-ops")
dao = LecteurDAO()

# --- FONCTIONS DE SANTÉ ET AUDIT (GARDÉES TEL QUEL) ---
def get_lecteur_health(lecteur):
    health = {'stabilite': 'bonne', 'down_frequents': False, 'derive_sync': 0, 'erreurs_recentes': [], 'uptime_percent': 98.5}
    if not lecteur.est_en_ligne():
        health.update({'stabilite': 'faible', 'down_frequents': True, 'uptime_percent': 85.2})
    return health

def get_lecteur_audit(lecteur_id):
    return [{'date': '2025-01-16 14:30:00', 'user': 'admin', 'action': 'Configuration modifiée', 'details': 'Volume changed'}]

def get_lecteur_current_state(lecteur):
    return {'playlist_assignee': 'Ambiance Matin', 'volume': 75, 'mode': 'lecture', 'dernier_contact': lecteur.derniere_synchro}

# --- ROUTES DU BLUEPRINT ---

@lecteurs_ops_bp.route("/", methods=['GET'])
@reqlogged
def lecteurs_ops():
    role = session.get("role", "utilisateur")
    all_lecteurs = dao.find_all()
    lecteurs_enriched = [{'lecteur': l, 'health': get_lecteur_health(l), 'current_state': get_lecteur_current_state(l)} for l in all_lecteurs]
    return render_template("lecteurs_ops.html", metadata={"title": "Gestion", "pagename": "lecteurs_ops"}, lecteurs_enriched=lecteurs_enriched, role=role)

# --- ROUTES API (LIAISON RASPBERRY PI) ---

@app.route('/api/lancer_pub/<int:id_lecteur>')
def api_lancer_pub(id_lecteur):
    """ Met à jour la BDD pour lancer la pub """
    try:
        heure = datetime.now().hour 
        if 6 <= heure < 11: fichier_pub = "pubmatin1.mp3"
        elif 11 <= heure < 18: fichier_pub = "pubmidi1.mp3"
        else: fichier_pub = "pubsoir1.mp3"

        conn = sqlite3.connect('app/database.db')
        cursor = conn.cursor()
        # On écrit l'état 'pub' et le nom du fichier
        cursor.execute("UPDATE Lecteur SET etat_lecteur = 'pub', emplacement = ? WHERE id_lecteur = ?", (fichier_pub, id_lecteur))
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "message": f"Signal envoyé : {fichier_pub}", "fichier": fichier_pub})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/ping/<int:id_lecteur>')
def api_ping(id_lecteur):
    """ Répond à la Raspberry Pi avec le contenu de la BDD """
    try:
        conn = sqlite3.connect('app/database.db')
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        # On récupère l'emplacement (le nom du mp3)
        cursor.execute("SELECT etat_lecteur, emplacement, volume FROM Lecteur WHERE id_lecteur = ?", (id_lecteur,))
        row = cursor.fetchone()
        conn.close()

        if row:
            # ICI : On renvoie TOUTES les clés, surtout 'emplacement'
            return jsonify({
                "statut": "success",
                "action": "play",
                "playlist": "matin",
                "volume": row['volume'],
                "emplacement": row['emplacement'] # <--- TA LIGNE EST ICI !
            })
        return jsonify({"statut": "error", "message": "Lecteur introuvable"}), 404
    except Exception as e:
        return jsonify({"statut": "error", "message": str(e)}), 500

@app.route('/api/pub_terminee/<int:id_lecteur>') # Décorateur ajouté !
def api_pub_terminee(id_lecteur):
    """ Remet la BDD à zéro après la pub """
    try:
        conn = sqlite3.connect('app/database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE Lecteur SET etat_lecteur = 'ambiance', emplacement = NULL WHERE id_lecteur = ?", (id_lecteur,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500