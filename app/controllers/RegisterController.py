from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.UserDAO import UserSqliteDAO

register_bp = Blueprint('register', __name__, template_folder='../templates')

user_service = UserSqliteDAO()

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"


@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        prenom = request.form.get('prenom', '').strip()
        nom = request.form.get('nom', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # Vérification des champs
        if not username or not email or not password:
            flash("Veuillez remplir tous les champs obligatoires.", "danger")
            return render_template('register.html')

        # Essayer de créer l'utilisateur
        try:
            success = user_service.createUser(
                username=username,
                password=password,
                prenom=prenom,
                nom=nom,
                email=email,
                role='utilisateur'
            )
            if success:
                flash("Compte créé avec succès ! Vous pouvez maintenant vous connecter.", "success")
                return redirect(url_for('login'))  # Assure-toi que ton login() est dans LoginController
            else:
                flash("Nom d’utilisateur ou email déjà utilisé.", "danger")
                return render_template('register.html')

        except ValueError as ve:
            flash(str(ve), "danger")
            return render_template('register.html')

    # GET → juste afficher le formulaire
    return render_template('register.html')
