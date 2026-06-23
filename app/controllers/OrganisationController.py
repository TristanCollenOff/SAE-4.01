from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3
import os

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
        session["id_organisation"] = id_organisation
        conn.close()
        return redirect(url_for("mood.mood"))

    cursor = conn.execute("""
        SELECT o.id_organisation, o.nom_organisation
        FROM organisation o
        JOIN affilier a ON a.id_organisation = o.id_organisation
        WHERE a.id_utilisateur = ?
    """, (session["user_id"],))

    organisations = cursor.fetchall()
    conn.close()

    return render_template("choose_organisation.html", organisations=organisations)