from app import app
from flask import render_template, request, redirect, url_for, session
from app.services.user_service import UserService
from app.services.log_service import log_login, log_failed_login, log_logout
from app.services.permissions import normalize_role, can
from functools import wraps

user_service = UserService()
us = UserService()

# -----------------------------
# DÉCORATEURS
# -----------------------------
def reqlogged(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def reqrole(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if normalize_role(session.get("role")) != normalize_role(role):
                return "Accès refusé", 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# -----------------------------
# LOGIN
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("nom_utilisateur", "").strip()
        password = request.form.get("motdepasse", "").strip()

        if not username or not password:
            return render_template(
                "login.html",
                msg_error="❌ Veuillez remplir tous les champs",
                nom_utilisateur=username
            )

        result = user_service.login(username, password)

        # ❌ LOGIN FAIL
        if result is None:
            log_failed_login(username, "Identifiants invalides")

            return render_template(
                "login.html",
                msg_error="❌ Nom utilisateur ou mot de passe incorrect",
                nom_utilisateur=username
            )

        # ⛔ BLOQUÉ
        if result == "blocked":
            return render_template(
                "login.html",
                msg_error="⛔ Compte temporairement bloqué",
                nom_utilisateur=username
            )

        user = result

        # SESSION
        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role
        session["logged"] = True

        log_login(user)

        if user.role == "marketing":
           return redirect(url_for("supervisor.supervisor_check"))

        return redirect(url_for("organisation.choose_organisation"))
    
    return render_template("login.html")



# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():

    if "user_id" in session:

        username = session.get("username")

        if username:
            user = user_service.getUserByUsername(username)

            if isinstance(user, list) and len(user) > 0:
                user = user[0]

            if user:
                log_logout(user)

    session.clear()
    return redirect(url_for("login"))