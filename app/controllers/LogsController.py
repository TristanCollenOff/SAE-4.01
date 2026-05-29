import sqlite3
import os
from app import app
from flask import Blueprint, redirect, render_template, session, abort, request, url_for, flash
from app.controllers.LoginController import reqlogged
from app.services.log_service import add_log, LOG_TYPES
from app.models.LecteurDAO import LecteurDAO

log_bp = Blueprint("logs", __name__, url_prefix="/logs")

def admin_required():
    """Vérifie que l'utilisateur connecté est administrateur"""
    if session.get("role") not in ["admin", "Administrateur"]:
        abort(403)

@log_bp.route("/", methods=['GET'])
@reqlogged
def logs():
    """Affiche la page des logs avec possibilité de filtrage"""
    admin_required()
    
    db_path = os.path.join(os.path.dirname(__file__), '../database.db')
    logs_data = []
    
    # Récupération des paramètres de filtre
    filter_user = request.args.get("user", "").strip()
    filter_type = request.args.get("type", "").strip()
    
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Construction de la requête avec filtres
            query = "SELECT * FROM FichierLog WHERE 1=1"
            params = []
            
            if filter_user:
                query += " AND (LOWER(username) LIKE ? OR LOWER(message) LIKE ?)"
                search_pattern = f"%{filter_user.lower()}%"
                params.extend([search_pattern, search_pattern])
            
            if filter_type:
                query += " AND type_log = ?"
                params.append(filter_type)
            
            query += " ORDER BY date_fichierlog DESC LIMIT 1000"
            
            logs_data = conn.execute(query, params).fetchall()
            
            # Récupération des types de logs uniques pour le filtre
            types_query = "SELECT DISTINCT type_log FROM FichierLog WHERE type_log IS NOT NULL ORDER BY type_log"
            log_types = [row['type_log'] for row in conn.execute(types_query).fetchall()]

    except sqlite3.OperationalError as e:
        print(f"Erreur SQLite lors de la récupération des logs : {e}")
        log_types = []

    metadata = {
        "title": "Journal des Logs",
        "pagename": "logs"
    }
    
    return render_template(
        "logs.html",
        metadata=metadata,
        logs=logs_data,
        filter_user=filter_user,
        filter_type=filter_type,
        log_types=log_types
    )

@app.route('/action_alerte/<int:id_lecteur>/<int:etat>')
def action_alerte_uniquelogs(id_lecteur, etat):
    dao = LecteurDAO()
    lecteur = dao.find_one(id_lecteur)
    
    if lecteur:
        success = dao.toggle_alerte(id_lecteur, etat)
        if success:
            action_verbe = "activé" if etat == 1 else "arrêté"
            utilisateur = session.get('username', 'Système')
            
            # On appelle directement add_log avec le type 'error' pour l'alerte
            from app.services.log_service import add_log, LOG_TYPES
            add_log(LOG_TYPES['ALERTE'], utilisateur, f"a {action_verbe} l'alerte sur : {lecteur.nom_lecteur}")
            
            flash(f"Alerte {action_verbe} avec succès.", "success")
    return redirect(url_for('voir_lecteur', id_lecteur=id_lecteur))