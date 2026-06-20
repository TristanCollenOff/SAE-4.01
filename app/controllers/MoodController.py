from flask import Blueprint, render_template, session, redirect, url_for, request
from urllib.parse import urlparse

mood_bp = Blueprint("mood", __name__)

THEMES_VALIDES = ["nature", "triste", "joyeux", "romantique", "default"]


def _safe_redirect_target():
    next_url = request.args.get("next") or request.referrer
    if not next_url:
        return url_for("index")

    parsed = urlparse(next_url)
    if parsed.netloc:
        return url_for("index")

    path = parsed.path or "/"
    if path.startswith("/set_theme/") or path.startswith("/logout"):
        return url_for("index")

    if parsed.query:
        return f"{path}?{parsed.query}"
    return path


@mood_bp.route("/mood")
def mood():
    return render_template("mood.html", hide_layout=True)


@mood_bp.route("/set_theme/<theme>")
def set_theme(theme):

    if theme not in THEMES_VALIDES:
        theme = "default"

    if theme == "chill":
        theme = "romantique"

    session["theme"] = theme
    session.modified = True

    return redirect(_safe_redirect_target())