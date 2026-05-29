from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.log_service import log_action
from functools import wraps
from datetime import datetime

contact_bp = Blueprint('contact', __name__, url_prefix='/contact')

def reqlogged(f):
    """Décorateur pour vérifier que l'utilisateur est connecté"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@contact_bp.route("/", methods=['GET', 'POST'])
@reqlogged
def contact():
    """Page de contact pour signaler un incident"""
    if request.method == 'POST':
        # Récupération des données du formulaire
        type_incident = request.form.get('type_incident', '').strip()
        priorite = request.form.get('priorite', 'moyenne').strip()
        titre = request.form.get('titre', '').strip()
        description = request.form.get('description', '').strip()
        lecteur_concerné = request.form.get('lecteur_concerné', '').strip()
        
        # Validation des champs obligatoires
        if not type_incident or not titre or not description:
            flash("Veuillez remplir tous les champs obligatoires.", "danger")
            return render_template('contact.html', 
                                 metadata={"title": "Signalement d'incident", "pagename": "contact"},
                                 form_data=request.form)
        
        # Récupération des informations utilisateur
        username = session.get('username', 'Utilisateur inconnu')
        user_id = session.get('user_id')
        
        # Log de l'incident
        log_message = f"Signalement d'incident - Type: {type_incident}, Priorité: {priorite}, Titre: {titre}"
        if lecteur_concerné:
            log_message += f", Lecteur: {lecteur_concerné}"
        
        if user_id:
            from app.models.UserDAO import UserSqliteDAO
            user_dao = UserSqliteDAO()
            user = user_dao.findById(user_id)
            if user:
                log_action(user, "signalement_incident", log_message)
        
        # Message de confirmation
        flash("Votre signalement a été enregistré avec succès. Notre équipe va examiner votre demande.", "success")
        
        # Redirection vers la page d'accueil
        return redirect(url_for('index'))
    
    # GET - Affichage du formulaire
    metadata = {"title": "Signalement d'incident", "pagename": "contact"}
    return render_template('contact.html', metadata=metadata)
