import os
import bcrypt
import sqlite3
from datetime import datetime, timedelta
from app import app
from app.models.User import User
from app.models.UserDAOInterface import UserDAOInterface

class UserSqliteDAO(UserDAOInterface):
    MAX_LOGIN_ATTEMPTS = 3
    BLOCK_TIME = timedelta(minutes=10)

    def __init__(self):
        self.databasename = os.path.join(os.path.dirname(__file__), '..', 'database.db')
        self.databasename = os.path.abspath(self.databasename)

        self._initTable()

    def _getDbConnection(self):
        conn = sqlite3.connect(self.databasename)
        conn.row_factory = sqlite3.Row
        return conn

    def _initTable(self):
        conn = self._getDbConnection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Utilisateur(
               id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
               nom_utilisateur VARCHAR(50) UNIQUE,
               prenom VARCHAR(50),
               nom VARCHAR(50),
               age INTEGER,
               email VARCHAR(100) UNIQUE,
               motdepasse VARCHAR(128),
               role VARCHAR(50),
               login_attempts INTEGER DEFAULT 0,
               block_until DATETIME,
               last_login DATETIME
            )
        ''')
        conn.commit()
        conn.close()

    # Hash mot de passe
    def _generatePwdHash(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Vérifie complexité mot de passe
    def _is_password_strong(self, password):
        import re
        return (
            len(password) >= 10 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"\d", password) and
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
        )

    # Créer un nouvel utilisateur
    def createUser(self, username, password, role='utilisateur', prenom="", nom="", age=None, email=""):
        if not self._is_password_strong(password):
            raise ValueError("Mot de passe trop faible")
        conn = self._getDbConnection()
        hashed_password = self._generatePwdHash(password)
        try:
            conn.execute(
                "INSERT INTO Utilisateur (nom_utilisateur, motdepasse, role, prenom, nom, age, email) "
                "VALUES (:u, :p, :r, :f, :l, :a, :e)",
                {
                    "u": username,
                    "p": hashed_password,
                    "r": role,
                    "f": prenom,
                    "l": nom,
                    "a": age,
                    "e": email
                }
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # nom_utilisateur ou email déjà existant
            return False
        finally:
            conn.close()

    # Trouver un utilisateur par username
    def findByUsername(self, username):
        conn = self._getDbConnection()
        user = conn.execute(
            "SELECT * FROM Utilisateur WHERE nom_utilisateur = :u",
            {"u": username}
        ).fetchone()
        conn.close()
        return User(user) if user else None

    # Vérifier login + tentatives + blocage
    def verifyUser(self, username, password):
        conn = self._getDbConnection()
        user_row = conn.execute(
            "SELECT * FROM Utilisateur WHERE nom_utilisateur = :u",
            {"u": username}
        ).fetchone()
        
        if not user_row:
            conn.close()
            return None

        user = User(user_row)

        # Check blocage sécurisé
        block_until = None
        if "block_until" in user_row.keys() and user_row["block_until"]:
            try:
                block_until = datetime.strptime(user_row["block_until"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                block_until = None

        if block_until and datetime.now() < block_until:
            conn.close()
            return "blocked"

        # Vérifier mot de passe
        if bcrypt.checkpw(password.encode('utf-8'), user_row["motdepasse"].encode('utf-8')):
            # Login OK → reset tentative et update last_login
            conn.execute(
                "UPDATE Utilisateur SET login_attempts = 0, block_until = NULL, last_login = :l WHERE id_utilisateur = :id",
                {"l": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "id": user.id}
            )
            conn.commit()
            conn.close()
            return user
        else:
            # Login échoué → incrémenter tentative et bloquer si nécessaire
            attempts = user_row["login_attempts"] + 1
            new_block_until = None
            if attempts >= self.MAX_LOGIN_ATTEMPTS:
                new_block_until = datetime.now() + self.BLOCK_TIME + timedelta(minutes=(attempts - self.MAX_LOGIN_ATTEMPTS) * 5)
            conn.execute(
                "UPDATE Utilisateur SET login_attempts = :att, block_until = :block WHERE id_utilisateur = :id",
                {"att": attempts,
                 "block": new_block_until.strftime("%Y-%m-%d %H:%M:%S") if new_block_until else None,
                 "id": user.id}
            )
            conn.commit()
            conn.close()
            return None

    # Trouver tous les utilisateurs
    def findAll(self):
        conn = self._getDbConnection()
        users = conn.execute("SELECT * FROM Utilisateur").fetchall()
        conn.close()
        return [User(dict(u)) for u in users]

    # Changer mot de passe
    def changePassword(self, user_id, new_password):
        if not self._is_password_strong(new_password):
            raise ValueError("Mot de passe trop faible")
        hashed = self._generatePwdHash(new_password)
        conn = self._getDbConnection()
        conn.execute(
            "UPDATE Utilisateur SET motdepasse = :p WHERE id_utilisateur = :id",
            {"p": hashed, "id": user_id}
        )
        conn.commit()
        conn.close()
        return True


# dans UserSqliteDAO
    def block_user(self, user_id, minutes=60):
     block_until = datetime.now() + timedelta(minutes=minutes)
     conn = self._getDbConnection()
     conn.execute(
        "UPDATE Utilisateur SET block_until = :b WHERE id_utilisateur = :id", 
          {"b": block_until.strftime("%Y-%m-%d %H:%M:%S"), "id": user_id}
        )
     conn.commit()
     conn.close()

    def unblock_user(self, user_id):
      conn = self._getDbConnection()
      conn.execute(
        "UPDATE Utilisateur SET block_until = NULL, login_attempts = 0 WHERE id_utilisateur = :id",
        {"id": user_id}
    )
      conn.commit()
      conn.close()


      # Dans UserSqliteDAO
    def findById(self, user_id):
      conn = self._getDbConnection()
      row = conn.execute(
        "SELECT * FROM Utilisateur WHERE id_utilisateur = :id",
        {"id": user_id}
    ).fetchone()
      conn.close()
      return User(row) if row else None


