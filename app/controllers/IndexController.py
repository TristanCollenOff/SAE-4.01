import sqlite3
from flask import render_template, request, redirect, url_for, jsonify
from app import app
from app.controllers.LoginController import reqlogged, us
from app.models.LecteurDAO import LecteurDAO

# --- ACCUEIL ---
@app.route("/", methods=['GET'])
@reqlogged
def index():
    utilisateurs = us.getUsers()
    db_path = app.root_path + '/database.db'
    stats = {"nb_users": 0, "nb_lecteurs": 0, "nb_logs": 0}
    
    if utilisateurs:
        stats["nb_users"] = len(utilisateurs)

    try:
        conn = sqlite3.connect(db_path)
        stats["nb_lecteurs"] = conn.execute('SELECT COUNT(*) FROM Lecteur').fetchone()[0]
        # On tente de compter les logs, si la table existe
        try:
            stats["nb_logs"] = conn.execute('SELECT COUNT(*) FROM FichierLog').fetchone()[0]
        except:
            pass
        conn.close()
    except:
        pass 

    metadata = {"title": "Accueil Rythmo", "pagename": "index"}
    return render_template('index.html', metadata=metadata, stats=stats)


# --- LA LISTE DES LECTEURS (Celle qui plantait) ---
@app.route("/lecteurs", methods=['GET'])
@reqlogged
def page_lecteurs():  # <--- J'ai renommé en 'page_lecteurs' (pas d'ID ici !)
    dao = LecteurDAO()
    liste_lecteurs = dao.find_all()
    metadata = {"title": "Gestion des Lecteurs", "pagename": "lecteurs"}
    return render_template("lecteurs.html", metadata=metadata, lecteurs=liste_lecteurs)


# --- LE DÉTAIL D'UN LECTEUR ---
@app.route("/lecteur/<int:id_lecteur>")
@reqlogged
def voir_lecteur(id_lecteur): # <--- C'est LUI qui prend l'ID
    dao = LecteurDAO()
    lecteur = dao.find_one(id_lecteur)
    metadata = {"title": "Détail du lecteur", "pagename": "lecteur_detail"}
    
    return render_template("lecteur_detail.html", lecteur=lecteur, metadata=metadata)


# --- AJOUTER ---
@app.route("/lecteur/add", methods=['GET', 'POST'])
@reqlogged
def ajouter_lecteur():
    if request.method == 'POST':
        nom = request.form['nom_lecteur']
        ip = request.form['adresseIP']
        emplacement = request.form['adresse_lecteur']
        
        dao = LecteurDAO()
        dao.create(nom, ip, emplacement)
        return redirect(url_for('page_lecteurs')) # Renvoie vers la liste correcte

    metadata = {"title": "Ajouter un lecteur", "pagename": "add_lecteur"}
    return render_template('lecteur_add.html', metadata=metadata)


# --- SUPPRIMER ---
@app.route("/lecteur/delete/<int:id_lecteur>", methods=['POST'])
@reqlogged
def supprimer_lecteur(id_lecteur):
    dao = LecteurDAO()
    dao.delete(id_lecteur)
    return redirect(url_for('page_lecteurs')) # Renvoie vers la liste correcte

@app.route("/api/ping/<int:id_lecteur>")
def ping_lecteur(id_lecteur):
    try:
        dao = LecteurDAO()
        # 1. On met à jour l'heure dans la BDD (C'est ce qui rend le bouton VERT)
        dao.set_online(id_lecteur)
        
        # 2. On répond avec des ordres clairs en JSON
        return jsonify({
            "statut": "success",
            "action": "play",
            "volume": 80
        })
    except Exception as e:
        print(f"Erreur lors du ping : {e}")
        return jsonify({"statut": "error"}), 500