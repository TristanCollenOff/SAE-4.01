import sqlite3
from flask import render_template, request, redirect, session, url_for, jsonify, flash, abort
from app import app
from app.controllers.LoginController import reqlogged
from app.models.LecteurDAO import LecteurDAO
from app.services.playback_service import PlaybackService
from app.services.access_control import require_permission
from app.services.permissions import normalize_role
from app.services.log_service import add_log, LOG_TYPES

# --- ACCUEIL ---
# --- ACCUEIL ---
@app.route("/", methods=['GET'])
@reqlogged
def index():
    from app.controllers.LoginController import us

    utilisateurs = us.getUsers()
    db_path = app.root_path + '/database.db'
    stats = {"nb_users": 0, "nb_lecteurs": 0, "nb_logs": 0}

    if utilisateurs:
        stats["nb_users"] = len(utilisateurs)

    try:
        conn = sqlite3.connect(db_path)
        # Correction : 'lecteur' au lieu de 'Lecteur'
        stats["nb_lecteurs"] = conn.execute('SELECT COUNT(*) FROM lecteur').fetchone()[0]
        try:
            # Correction : 'fichier_log' au lieu de 'FichierLog'
            stats["nb_logs"] = conn.execute('SELECT COUNT(*) FROM fichier_log').fetchone()[0]
        except Exception as e:
            print(f"Erreur lors du COUNT de fichier_log : {e}")
            pass
        conn.close()
    except Exception as e:
        print(f"Erreur de connexion BDD sur l'index : {e}")
        pass

    playback = PlaybackService(db_path).get_dashboard_playback()

    metadata = {"title": "Accueil Rythmo", "pagename": "index"}
    return render_template(
        'index.html',
        metadata=metadata,
        stats=stats,
        playback=playback,
        theme=session.get("theme", "default")
    )

@app.route("/lecteurs", methods=['GET'])
@reqlogged
@require_permission("manage_lecteurs")
def page_lecteurs():
    dao = LecteurDAO()
    liste_lecteurs = dao.find_all()
    metadata = {"title": "Gestion des Lecteurs", "pagename": "lecteurs"}
    return render_template("lecteurs.html", metadata=metadata, lecteurs=liste_lecteurs)


@app.route("/lecteur/<int:id_lecteur>")
@reqlogged
@require_permission("manage_lecteurs", "view_lecteur_status", "urgent_announcement")
def voir_lecteur(id_lecteur):
    dao = LecteurDAO()
    lecteur = dao.find_one(id_lecteur)
    if not lecteur:
        abort(404)

    role = normalize_role(session.get("role", "commercial"))
    metadata = {"title": "Détail du lecteur", "pagename": "lecteur_detail"}

    return render_template(
        "lecteur_detail.html",
        lecteur=lecteur,
        metadata=metadata,
        role=role,
        readonly=role == "commercial",
    )


@app.route("/lecteur/add", methods=['GET', 'POST'])
@reqlogged
@require_permission("manage_lecteurs")
def ajouter_lecteur():
    if request.method == 'POST':
        nom = request.form['nom_lecteur']
        ip = request.form['adresseIP']
        emplacement = request.form['adresse_lecteur']

        dao = LecteurDAO()
        dao.create(nom, ip, emplacement)
        return redirect(url_for('page_lecteurs'))

    metadata = {"title": "Ajouter un lecteur", "pagename": "add_lecteur"}
    return render_template('lecteur_add.html', metadata=metadata)


@app.route("/lecteur/delete/<int:id_lecteur>", methods=['POST'])
@reqlogged
@require_permission("manage_lecteurs")
def supprimer_lecteur(id_lecteur):
    dao = LecteurDAO()
    dao.delete(id_lecteur)
    return redirect(url_for('page_lecteurs'))


@app.route("/api/ping/<int:id_lecteur>")
def ping_lecteur(id_lecteur):
    try:
        dao = LecteurDAO()
        dao.set_online(id_lecteur)

        return jsonify({
            "statut": "success",
            "action": "play",
            "volume": 80
        })
    except Exception as e:
        print(f"Erreur lors du ping : {e}")
        return jsonify({"statut": "error"}), 500
