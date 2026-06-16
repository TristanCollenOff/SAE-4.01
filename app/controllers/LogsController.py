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
    filter_search = request.args.get("user", "").strip()  
    filter_type = request.args.get("type", "").strip()
    
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            query = "SELECT * FROM fichier_log WHERE 1=1"
            params = []
            
 
            if filter_search:
                query += " AND LOWER(message) LIKE ?"
                search_pattern = f"%{filter_search.lower()}%"
                params.append(search_pattern)
            
            if filter_type:
                query += " AND type_action = ?"
                params.append(filter_type)
            
            query += " ORDER BY date_fichierlog DESC LIMIT 1000"
            
            logs_data = conn.execute(query, params).fetchall()
            

            types_query = "SELECT DISTINCT type_action FROM fichier_log WHERE type_action IS NOT NULL ORDER BY type_action"
            log_types = [row['type_action'] for row in conn.execute(types_query).fetchall()]

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
        filter_user=filter_search,  
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
            
            id_organisation = session.get('id_organisation', lecteur.id_organisation)
            username = session.get('username', 'Système')

            add_log(LOG_TYPES['ALERTE'], id_organisation, f"[{username}] a {action_verbe} l'alerte sur le lecteur : {lecteur.nom_lecteur}")
            
            flash(f"Alerte {action_verbe} avec succès.", "success")
            
    return redirect(url_for('voir_lecteur', id_lecteur=id_lecteur))