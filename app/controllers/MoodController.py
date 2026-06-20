from app import app
from flask import render_template, session, redirect, url_for

@app.route("/mood")
def mood():
    return render_template("mood.html")

@app.route("/set_theme/<theme>")
def set_theme(theme):

    themes_valides = ["nature", "triste", "joyeux", "chill", "default"]

    if theme not in themes_valides:
        theme = "default"

    session["theme"] = theme
    return redirect(url_for("index"))