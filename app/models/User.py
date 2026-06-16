# User.py
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

class User:

    MAX_LOGIN_ATTEMPTS = 3
    BLOCK_TIME = timedelta(minutes=10)

    def __init__(self, row):
        self.id = row["id_utilisateur"]

        # IMPORTANT : standardisation des noms
        self.username = row["nom_utilisateur"]
        self.role = row["nom_role"] if "nom_role" in row.keys() else "utilisateur"

        self.firstname = row["prenom"] if "prenom" in row.keys() else ""
        self.lastname = row["nom"] if "nom" in row.keys() else ""
        self.email = row["email"] if "email" in row.keys() else ""

        self.password_hash = row["motdepasse"]

        # sécurité login
        self.login_attempts = row["login_attempts"] if "login_attempts" in row.keys() else 0

        self.block_until = None
        if "block_until" in row.keys() and row["block_until"]:
            try:
                self.block_until = datetime.strptime(row["block_until"], "%Y-%m-%d %H:%M:%S")
            except:
                self.block_until = None

        self.last_login = None
        if "last_login" in row.keys() and row["last_login"]:
            try:
                self.last_login = datetime.strptime(row["last_login"], "%Y-%m-%d %H:%M:%S")
            except:
                self.last_login = None

        self.session_active = False

    # ---------------- SESSION ----------------
    def start_session(self):
        self.session_active = True
        self.last_login = datetime.now()

    def end_session(self):
        self.session_active = False

    # ---------------- LOGIN BLOCK LOGIC ----------------
    def can_attempt_login(self):
        if self.block_until and datetime.now() < self.block_until:
            return False

        if self.block_until and datetime.now() >= self.block_until:
            self.login_attempts = 0
            self.block_until = None

        return True

    def record_failed_login(self):
        self.login_attempts += 1

        if self.login_attempts >= self.MAX_LOGIN_ATTEMPTS:
            self.block_until = datetime.now() + self.BLOCK_TIME

    # ---------------- ROLE ----------------
    def has_access(self, resource_role):
        if self.role == "superviseur":
            return True
        return self.role == resource_role

    # ---------------- FLASK COMPAT ----------------
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)