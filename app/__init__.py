from flask import Flask, session, redirect, url_for, g
from datetime import datetime, timedelta

# -------------------------
# Création de l'application
# -------------------------
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'ma_cle_secrete_unique'
app.config["SESSION_COOKIE_SECURE"] = True


# -------------------------
# Configuration session
# -------------------------
SESSION_TIMEOUT = 30  # minutes

# -------------------------
# Middleware pour déconnexion automatique
# -------------------------
@app.before_request
def check_session_timeout():
    if 'user_id' in session:
        last_active = session.get('last_active')
        now = datetime.now()

        if last_active:
            if isinstance(last_active, str):
                last_active = datetime.fromisoformat(last_active)

            delta = (now - last_active).total_seconds() / 60
            if delta > SESSION_TIMEOUT:
                session.clear()
                return redirect(url_for('login'))

        session['last_active'] = now.isoformat()


# -------------------------
# INJECTION DE current_user
# -------------------------

from app.models.UserDAO import UserSqliteDAO

@app.before_request
def load_user():
    user_id = session.get("user_id")
    if user_id:
        user = UserSqliteDAO().findById(user_id)
        g.current_user = user
    else:
        g.current_user = None

@app.context_processor
def inject_user():
    return dict(current_user=g.get("current_user", None))


# -------------------------
# Filtre Jinja
# -------------------------
def toFrench(name):
    if name.lower() == "squirtle":
        return "carapuce"
    return name

app.jinja_env.filters['french'] = toFrench


# -------------------------
# Importer les routes
# -------------------------
from app.controllers import *
