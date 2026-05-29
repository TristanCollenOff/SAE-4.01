# LoginController.py
from app import app
from flask import render_template, request, redirect, url_for, session
from app.services.user_service import UserService
from app.services.log_service import log_login, log_failed_login, log_logout
from functools import wraps

# Service utilisateur
user_service = UserService()
us = user_service  # pour AdminController et IndexController

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
    """Vérifie que l'utilisateur connecté a le rôle requis"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get("role") != role:
                return "Accès refusé : rôle requis = " + role
            return f(*args, **kwargs)
        return decorator
    return decorator

# -----------------------------
# Route login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Récupération sécurisée des champs du formulaire
        username = request.form.get('nom_utilisateur', '').strip()
        password = request.form.get('motdepasse', '').strip()

        # Vérification que les champs ne sont pas vides
        if not username or not password:
            return "Veuillez remplir tous les champs"

        user = user_service.login(username, password)

        # ❌ utilisateur ou mot de passe incorrect
        if user is None:
            # Log de la tentative échouée
            log_failed_login(username, "Mot de passe incorrect")
            
            return render_template(
                "login.html",
                msg_error="❌ Utilisateur ou mot de passe incorrect. Veuillez réessayer.",
                nom_utilisateur=username
            )
        elif user:
            # ✅ Session correcte
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session['logged'] = True
            session['nom_utilisateur'] = user.username

            # Log de connexion réussie
            log_login(user)

            return redirect(url_for("index"))
        else:
            # Cas générique d'erreur
            log_failed_login(username, "Identifiants invalides")
            return "Nom utilisateur ou mot de passe incorrect"
            
    return render_template("login.html")

# -----------------------------
# Route logout
# -----------------------------
@app.route("/logout")
def logout():
    if 'user_id' in session:
        temp_user = user_service.getUserByUsername(session['username'])
        if temp_user:
            user = temp_user[0]
            log_logout(user)
        session.clear()
    return redirect(url_for("login"))