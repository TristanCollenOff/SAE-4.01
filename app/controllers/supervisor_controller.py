from flask import Blueprint, render_template, request, session, redirect, url_for

supervisor_bp = Blueprint("supervisor", __name__)

SECRET_WORD = "playlist"


@supervisor_bp.route("/supervisor", methods=["GET", "POST"])
def supervisor_check():

    if request.method == "POST":
        mot = request.form.get("mot", "").strip().lower()

        if mot == SECRET_WORD:
            session["supervisor_verified"] = True
            return redirect(url_for("mood.mood"))

        return render_template("supervisor_check.html", error="❌ Mauvais mot")

    return render_template("supervisor_check.html")