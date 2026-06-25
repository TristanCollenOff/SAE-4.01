from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3
import os

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

        if not id_organisation:
            conn.close()
            return "Organisation invalide", 400

        id_organisation = int(id_organisation)

        # Sécurité serveur : l'utilisateur doit être affilié à l'organisation choisie
        cursor = conn.execute(
            """
            SELECT 1
            FROM affilier
            WHERE id_utilisateur = ?
            AND id_organisation = ?
            """,
            (session["user_id"], id_organisation)
        )

        autorise = cursor.fetchone()

        if not autorise:
            conn.close()
            return "Accès refusé à cette organisation", 403

        # Récupération du nom de l'organisation choisie
        cursor = conn.execute(
            """
            SELECT nom_organisation
            FROM organisation
            WHERE id_organisation = ?
            """,
            (id_organisation,)
        )

        org_row = cursor.fetchone()
        nom_org = org_row["nom_organisation"] if org_row else f"Organisation #{id_organisation}"

        # Enregistrement en session uniquement après validation
        session["id_organisation"] = id_organisation
        session["nom_organisation"] = nom_org

        # Log lié à la bonne organisation
        username = session.get("username", "Utilisateur")
        add_log(
            "CONNEXION",
            session["id_organisation"],
            f"L'utilisateur {username} a basculé sur l'espace : {nom_org}"
        )

        conn.close()
        return redirect(url_for("mood.mood"))

    # GET : on affiche toutes les organisations pour la démo
    cursor = conn.execute(
        """
        SELECT id_organisation, nom_organisation
        FROM organisation
        ORDER BY nom_organisation
        """
    )

    organisations = cursor.fetchall()

    # Organisations réellement autorisées pour l'utilisateur connecté
    cursor = conn.execute(
        """
        SELECT id_organisation
        FROM affilier
        WHERE id_utilisateur = ?
        """,
        (session["user_id"],)
    )

    organisations_autorisees = [
        row["id_organisation"]
        for row in cursor.fetchall()
    ]

    conn.close()

    return render_template(
        "choose_organisation.html",
        organisations=organisations,
        organisations_autorisees=organisations_autorisees
    )