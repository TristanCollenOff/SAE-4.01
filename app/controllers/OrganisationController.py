from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3
import os
# IMPORTATION de ton service de journalisation
from app.services.log_service import add_log

organisation_bp = Blueprint("organisation", __name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")


@organisation_bp.route("/choose-organisation", methods=["GET", "POST"])
def choose_organisation():
    if not session.get("logged"):
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    if request.method == "POST":
        id_organisation = request.form.get("id_organisation")
        
        # 1. On enregistre le VRAI choix (on le caste en int pour correspondre à ton schéma de clés)
        session["id_organisation"] = int(id_organisation)
        
        # 2. On récupère le nom de l'organisation choisie pour fabriquer un beau message
        cursor = conn.execute(
            "SELECT nom_organisation FROM organisation WHERE id_organisation = ?", 
            (id_organisation,)
        )
        org_row = cursor.fetchone()
        nom_org = org_row["nom_organisation"] if org_row else f"Organisation #{id_organisation}"
        
        # 3. INTERCEPTION : On génère le log lié à la bonne organisation
        username = session.get("username", "Utilisateur")
        add_log(
            "CONNEXION", 
            session["id_organisation"], 
            f"L'utilisateur {username} a basculé sur l'espace : {nom_org}"
        )
        
        conn.close()
        return redirect(url_for("mood.mood"))

    # Affichage du formulaire (GET)
    cursor = conn.execute("""
        SELECT o.id_organisation, o.nom_organisation
        FROM organisation o
        JOIN affilier a ON a.id_organisation = o.id_organisation
        WHERE a.id_utilisateur = ?
    """, (session["user_id"],))

    organisations = cursor.fetchall()
    conn.close()

    return render_template("choose_organisation.html", organisations=organisations)