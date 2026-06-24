import sqlite3
import csv
import io
import datetime
import os
from app import app
from flask import Blueprint, Response, redirect, render_template, session, abort, request, url_for, flash
from app.controllers.LoginController import reqlogged, reqrole
from app.services.access_control import require_permission
from app.services.log_service import add_log, LOG_TYPES
from app.models.LogsDAO import LogsDAO
from app.models.LecteurDAO import LecteurDAO

log_bp = Blueprint("logs", __name__, url_prefix="/logs")
ldao = LogsDAO()


@log_bp.route("/", methods=['GET'])
@reqlogged
@require_permission("view_history")
def logs():
    """Affiche l'historique complet avec correction du bug de répétition d'organisation."""
    db_path = os.path.join(os.path.dirname(__file__), '../database.db')
    logs_data = []
    filter_search = request.args.get("user", "").strip()
    filter_type = request.args.get("type", "").strip()

    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row

            # En sélectionnant explicitement f.id_organisation, on évite que SQLite écrase les données
            query = """
                SELECT 
                    f.id_log,
                    f.type_action,
                    f.message,
                    f.date_fichierlog,
                    f.id_organisation,
                    o.nom_organisation
                FROM fichier_log f
                LEFT JOIN organisation o ON f.id_organisation = o.id_organisation
                WHERE 1=1
            """
            params = []

            if filter_search:
                query += " AND LOWER(f.message) LIKE ?"
                search_pattern = f"%{filter_search.lower()}%"
                params.append(search_pattern)

            if filter_type:
                query += " AND f.type_action = ?"
                params.append(filter_type)

            query += " ORDER BY f.date_fichierlog DESC LIMIT 1000"

            # On convertit explicitement en liste de dictionnaires pour Jinja
            raw_rows = conn.execute(query, params).fetchall()
            logs_data = [dict(row) for row in raw_rows]

            types_query = "SELECT DISTINCT type_action FROM fichier_log WHERE type_action IS NOT NULL ORDER BY type_action"
            log_types = [row['type_action'] for row in conn.execute(types_query).fetchall()]

    except sqlite3.OperationalError as e:
        print(f"Erreur SQLite lors de la récupération des logs : {e}")
        log_types = []

    metadata = {
        "title": "Historique de diffusion",
        "pagename": "logs"
    }

    return render_template(
        "logs.html",
        metadata=metadata,
        logs=logs_data,
        filter_user=filter_search,
        filter_type=filter_type,
        log_types=log_types,
        readonly=not session.get("role") == "admin",
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


@app.route('/logs/export')
@reqlogged
@require_permission("export_history")
def export_logs_csv():
    logs = ldao.get_all_logs()
    proxy = io.StringIO()
    proxy.write('\ufeff')
    writer = csv.writer(proxy, delimiter=';')
    writer.writerow(['ID_Log', 'Type_Action', 'message', 'date'])

    for log in logs:
        writer.writerow([
            log.id_log,
            log.type_action,
            log.message,
            log.date_fichierlog
        ])

    date_str = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%M")
    filename = f"export_logs_{date_str}.csv"

    csv_data = proxy.getvalue()
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )
