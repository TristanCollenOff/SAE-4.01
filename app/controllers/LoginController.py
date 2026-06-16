# LoginController.py
# LoginController.py
from app import app
from flask import render_template, request, redirect, url_for, session
from app.services.user_service import UserService
from app.services.log_service import log_login, log_failed_login, log_logout
from functools import wraps

# Service utilisateur
user_service = UserService()

# -----------------------------
# Décorateurs
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
            if session.get("role") != role:
                return f"Accès refusé : rôle requis = {role}"
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

        # -----------------------------
        # CAS 1 : utilisateur bloqué
        # -----------------------------
        if result == "blocked":
            return render_template(
                "login.html",
                msg_error="⛔ Compte temporairement bloqué. Réessayez plus tard.",
                nom_utilisateur=username
            )

        # -----------------------------
        # CAS 2 : erreur login
        # -----------------------------
        if result is None:
            log_failed_login(username, "Identifiants invalides")

            return render_template(
                "login.html",
                msg_error="❌ Nom utilisateur ou mot de passe incorrect",
                nom_utilisateur=username
            )

        # -----------------------------
        # CAS 3 : login OK
        # -----------------------------
        user = result

        session["user_id"] = user.id
        session["username"] = user.nom_utilisateur
        session["role"] = user.nom_role
        session["logged"] = True

        log_login(user)

        return redirect(url_for("index"))

    return render_template("login.html")


# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():

    if "user_id" in session:
        temp_user = user_service.getUserByUsername(session["username"])

        if temp_user:
            user = temp_user[0]
            log_logout(user)

    session.clear()
    return redirect(url_for("login"))