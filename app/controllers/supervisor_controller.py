from flask import Blueprint, render_template, request, session, redirect, url_for
import random

supervisor_bp = Blueprint("supervisor", __name__)

# Liste des mots possibles
WORDS = ["playlist", "musique", "montagne", "piano", "jouer", "cerise", "chocolat"]


@supervisor_bp.route("/supervisor", methods=["GET", "POST"])
def supervisor_check():

    # mot choisi au hasard (stocké en session)
    if "supervisor_word" not in session:
        session["supervisor_word"] = random.choice(WORDS)

    secret = session["supervisor_word"]

    if request.method == "POST":

        mot = request.form.get("mot", "").strip().lower()

        if mot == secret:
            session["supervisor_verified"] = True
            session.pop("supervisor_word", None)  # reset mot
            return redirect(url_for("mood.mood"))

        return render_template(
            "supervisor_check.html",
            error="❌ Mauvais mot",
            word=secret
        )

    return render_template(
        "supervisor_check.html",
        word=secret
    )