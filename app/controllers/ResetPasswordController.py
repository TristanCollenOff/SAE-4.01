from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.UserDAO import UserSqliteDAO
import random, string

reset_bp = Blueprint('reset', __name__)
userDAO = UserSqliteDAO()

@reset_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    step = 'request'  # étape par défaut

    if request.method == 'POST':
        # Étape 1 : demander code
        if 'username' in request.form and 'email' in request.form:
            username = request.form['username']
            email = request.form['email']
            user = userDAO.findByUsername(username)
            if user and user.email == email:
                code = ''.join(random.choices(string.digits, k=6))
                session['reset_code'] = code
                session['reset_user'] = username
                flash(f"Code envoyé à {email} (pour test : {code})", "info")
                step = 'verify'
            else:
                flash("Nom utilisateur ou email incorrect.", "danger")
                step = 'request'

        # Étape 2 : vérifier code
        elif 'code' in request.form:
            code = request.form['code']
            if code == session.get('reset_code'):
                step = 'new_password'
            else:
                flash("Code incorrect.", "danger")
                step = 'verify'

        # Étape 3 : nouveau mot de passe
        elif 'new_password' in request.form:
            new_pwd = request.form['new_password']
            username = session.get('reset_user')
            user = userDAO.findByUsername(username)
            if user:
                userDAO.changePassword(user.id, new_pwd)
                flash("Mot de passe réinitialisé avec succès !", "success")
                session.pop('reset_code', None)
                session.pop('reset_user', None)
                return redirect(url_for('login'))

    return render_template('reset_password.html', step=step)
