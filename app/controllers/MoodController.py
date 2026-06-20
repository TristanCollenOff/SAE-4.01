from flask import Blueprint, render_template, session, redirect, url_for

mood_bp = Blueprint("mood", __name__)

@mood_bp.route("/mood")
def mood():
    return render_template("mood.html", hide_layout=True)


@mood_bp.route("/set_theme/<theme>")
def set_theme(theme):

    themes_valides = ["nature", "triste", "joyeux", "romantique", "default"]

    if theme not in themes_valides:
        theme = "default"

    if theme == "chill":
        theme = "romantique"

    session["theme"] = theme
    session.modified = True

    return redirect(url_for("index"))