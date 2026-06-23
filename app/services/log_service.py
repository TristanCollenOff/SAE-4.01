import sqlite3
from app import app
from datetime import datetime

DB_PATH = app.root_path + '/database.db'

# Centralisation des types d'actions (parfaitement alignés avec ton schema.sql et logs.html)
LOG_TYPES = {
    'INFO': 'INFO',
    'WARNING': 'WARNING',
    'ERROR': 'ERROR',
    'CONNEXION': 'CONNEXION',
    'ALERTE': 'ALERTE'
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
    """Log la connexion d'un utilisateur (gère username ou nom_utilisateur)"""
    id_org = getattr(user, 'id_organisation', 1) 
    
    # Sécurité anti-AttributeError : s'adapte à n'importe quel modèle d'objet User
    username = getattr(user, 'username', getattr(user, 'nom_utilisateur', str(user)))
    
    add_log(LOG_TYPES['CONNEXION'], id_org, f"L'utilisateur {username} s'est connecté")

def log_logout(user):
    """Log la déconnexion d'un utilisateur (gère username ou nom_utilisateur)"""
    id_org = getattr(user, 'id_organisation', 1)
    
    # Même sécurité anti-AttributeError
    username = getattr(user, 'username', getattr(user, 'nom_utilisateur', str(user)))
    
    add_log(LOG_TYPES['CONNEXION'], id_org, f"L'utilisateur {username} s'est déconnecté")

def log_failed_login(id_organisation, username, reason="Mot de passe incorrect"):
    """Log une tentative de connexion échouée"""
    add_log(LOG_TYPES['ERROR'], id_organisation, f"Tentative de connexion échouée pour {username} : {reason}")

def log_action(user, action_msg):
    """Log une action utilisateur pour AdminController.py"""
    id_org = getattr(user, 'id_organisation', 1)
    
    # Sécurité pour extraire correctement le nom d'utilisateur peu importe l'attribut
    username = getattr(user, 'username', getattr(user, 'nom_utilisateur', str(user)))

    full_message = f"[{username}] {action_msg}"
    add_log(LOG_TYPES['WARNING'], id_org, full_message)