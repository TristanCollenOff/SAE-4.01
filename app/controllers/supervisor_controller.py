from flask import Blueprint, render_template, request, session, redirect, url_for
import random
from app.services.captcha_service import CaptchaService

supervisor_bp = Blueprint("supervisor", __name__)

# Liste des mots possibles
WORDS = ["playlist", "musique", "montagne", "piano", "jouer", "cerise", "chocolat"]

captcha_service = CaptchaService()


@supervisor_bp.route("/supervisor", methods=["GET", "POST"])
def supervisor_check():

    # mot choisi au hasard (stocké en session)
    if "supervisor_word" not in session:
        session["supervisor_word"] = random.choice(WORDS)

    secret = session["supervisor_word"]

    # Générer le style CSS pour le CAPTCHA
    captcha_style = captcha_service.generate_captcha_style(secret)

    if request.method == "POST":

        mot = request.form.get("secret_word", "").strip().upper()

        if mot == secret.upper():
            session["supervisor_verified"] = True
            session.pop("supervisor_word", None)  # reset mot
            return redirect(url_for("mood.mood"))

        # Régénérer le style en cas d'erreur
        captcha_style = captcha_service.generate_captcha_style(secret)

        return render_template(
            "supervisor_check.html",
            error="❌ Mauvais mot",
            word=secret,
            captcha_style=captcha_style
        )

    return render_template(
        "supervisor_check.html",
        word=secret,
        captcha_style=captcha_style
    )