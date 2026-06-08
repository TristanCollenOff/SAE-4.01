import sqlite3
from app import app
from datetime import datetime

DB_PATH = app.root_path + '/database.db'

LOG_TYPES = {
    'INFO': 'INFO',
    'WARNING': 'WARNING',
    'ERROR': 'ERROR',
    'CONNEXION': 'CONNEXION'
}

def add_log(log_type: str, id_organisation: int, message: str):
    """Enregistre un log en base de données selon le schéma officiel"""
    try:
        conn = sqlite3.connect(DB_PATH)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn.execute('''
            INSERT INTO fichier_log (type_action, message, date_fichierlog, id_organisation)
            VALUES (?, ?, ?, ?)
        ''', (log_type, message, current_time, id_organisation))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de l'écriture du log : {e}")

def log_login(user):

    id_org = getattr(user, 'id_organisation', 1) 
    add_log(LOG_TYPES['CONNEXION'], id_org, f"L'utilisateur {user.nom_utilisateur} s'est connecté")

def log_logout(user):
    id_org = getattr(user, 'id_organisation', 1)
    add_log(LOG_TYPES['CONNEXION'], id_org, f"L'utilisateur {user.nom_utilisateur} s'est déconnecté")

def log_failed_login(id_organisation, username, reason="Mot de passe incorrect"):
    """Log une tentative de connexion échouée (nécessite l'id de l'organisation cible ou par défaut)"""
    add_log(LOG_TYPES['ERROR'], id_organisation, f"Tentative de connexion échouée pour {username} : {reason}")

def log_action(user, action_msg):
    """Log une action utilisateur pour AdminController.py"""
    id_org = getattr(user, 'id_organisation', 1)
    username = user.nom_utilisateur if hasattr(user, 'nom_utilisateur') else str(user)

    full_message = f"[{username}] {action_msg}"
    add_log(LOG_TYPES['WARNING'], id_org, full_message)