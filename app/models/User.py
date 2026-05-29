# User.py
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

class User:
    MAX_LOGIN_ATTEMPTS = 3
    BLOCK_TIME = timedelta(minutes=10)

    def __init__(self, row):
        self.id = row["id_utilisateur"]
        self.username = row["nom_utilisateur"]
        self.role = row["role"] if "role" in row.keys() else "utilisateur"
        self.firstname = row["prenom"] if "prenom" in row.keys() else ""
        self.lastname = row["nom"] if "nom" in row.keys() else ""
        self.age = row["age"] if "age" in row.keys() else None
        self.email = row["email"] if "email" in row.keys() else ""
        self.password_hash = row["motdepasse"] if "motdepasse" in row.keys() else ""
        self.login_attempts = row["login_attempts"] if "login_attempts" in row.keys() else 0

        self.block_until = None
        if "block_until" in row.keys() and row["block_until"]:
            try:
                self.block_until = datetime.strptime(row["block_until"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                self.block_until = None

        self.last_login = None
        if "last_login" in row.keys() and row["last_login"]:
            try:
                self.last_login = datetime.strptime(row["last_login"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                self.last_login = None

        self.session_active = False

    # Mot de passe
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Tentatives login
    def can_attempt_login(self):
        if self.block_until:
            if datetime.now() < self.block_until:
                return False
            else:
                self.login_attempts = 0
                self.block_until = None
        return True

    def record_failed_login(self):
        self.login_attempts += 1
        if self.login_attempts >= User.MAX_LOGIN_ATTEMPTS:
            extra_minutes = max(0, (self.login_attempts - User.MAX_LOGIN_ATTEMPTS) * 5)
            self.block_until = datetime.now() + User.BLOCK_TIME + timedelta(minutes=extra_minutes)

    # Sessions
    def start_session(self):
        self.session_active = True
        self.last_login = datetime.now()

    def end_session(self):
        self.session_active = False

    def block_user(self, user_id, minutes=60):
        self.udao.block_user(user_id, minutes)

    def unblock_user(self, user_id):
        self.udao.unblock_user(user_id)

    # Contrôle d’accès
    def has_access(self, resource_role):
        if self.role == "superviseur":
            return True
        return self.role == resource_role

    # Logs simplifiés
    def log_action(self, action, logs_list):
        logs_list.append({
            "user_id": self.id,
            "username": self.username,
            "action": action,
            "timestamp": datetime.now()
        })

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

