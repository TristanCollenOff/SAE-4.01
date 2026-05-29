import sqlite3
from app import app
from datetime import datetime

DB_PATH = app.root_path + '/database.db'

# On définit LOG_TYPES pour corriger l'ImportError dans LogsController
LOG_TYPES = {
    'INFO': 'info',
    'WARNING': 'warning',
    'ERROR': 'error',
    'ALERTE': 'error'
}

def add_log(log_type, username, message):
    """Enregistre un log avec le type exact pour les statistiques du template"""
    try:
        conn = sqlite3.connect(DB_PATH)
        # Utilisation des colonnes type_log et username pour le template
        conn.execute('''
            INSERT INTO FichierLog (type_log, username, message, date_fichierlog)
            VALUES (?, ?, ?, ?)
        ''', (log_type, username, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de l'écriture du log : {e}")

# --- Fonctions pour les Controllers ---

def log_login(user):
    # 'info' incrémente le compteur "Infos" dans logs.html
    add_log(LOG_TYPES['INFO'], user.username, "S'est connecté")

def log_logout(user):
    add_log(LOG_TYPES['INFO'], user.username, "S'est déconnecté")

def log_failed_login(username, reason="Mot de passe incorrect"):
    """Log une tentative de connexion échouée"""
    add_log(LOG_TYPES['ERROR'], username, f"Tentative de connexion échouée : {reason}")

def log_action(user, action_msg):
    # Rétablit la fonction pour AdminController.py
    username = user.username if hasattr(user, 'username') else str(user)
    add_log(LOG_TYPES['WARNING'], username, action_msg)