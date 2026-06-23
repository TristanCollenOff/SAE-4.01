import os
import bcrypt
import re
import sqlite3
from datetime import datetime, timedelta

from app.models.User import User
from app.models.UserDAOInterface import UserDAOInterface


class UserSqliteDAO(UserDAOInterface):

    MAX_LOGIN_ATTEMPTS = 3
    BLOCK_TIME = timedelta(minutes=10)

    def __init__(self):
        self.databasename = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'database.db')
        )

    # ---------------- DB ----------------
    def _getDbConnection(self):
        conn = sqlite3.connect(self.databasename)
        conn.row_factory = sqlite3.Row
        return conn

    # ---------------- HASH ----------------
    def _generatePwdHash(self, password):
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    # ---------------- PASSWORD RULES ----------------
    def _is_password_strong(self, password):
        return (
            len(password) >= 10 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"\d", password) and
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
        )

    # ---------------- CREATE USER ----------------
    def createUser(self, username, password, role='commercial',
                   prenom="", nom="", email=""):

        if not self._is_password_strong(password):
            raise ValueError("Mot de passe trop faible")

        hashed = self._generatePwdHash(password)

        conn = self._getDbConnection()
        try:
            conn.execute("""
                INSERT INTO utilisateur
                (nom_utilisateur, motdepasse, prenom, nom, email, nom_role)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, hashed, prenom, nom, email, role))

            conn.commit()
            return True

        except sqlite3.IntegrityError:
            return False

        finally:
            conn.close()

    # ---------------- FIND USER ----------------
    def findByUsername(self, username):
        conn = self._getDbConnection()

        row = conn.execute("""
            SELECT * FROM utilisateur
            WHERE nom_utilisateur = ?
        """, (username,)).fetchone()

        conn.close()
        return User(row) if row else None

    # ---------------- LOGIN (CORRIGÉ JOIN connexion) ----------------
    def verifyUser(self, username, password):

        conn = self._getDbConnection()

        user_row = conn.execute("""
            SELECT u.*, c.login_attempts, c.block_until
            FROM utilisateur u
            LEFT JOIN connexion c
                ON u.id_utilisateur = c.id_utilisateur
            WHERE u.nom_utilisateur = ?
        """, (username,)).fetchone()

        if not user_row:
            conn.close()
            return None

        user = User(user_row)

        # ---------------- BLOCK CHECK ----------------
        block_until = None
        if user_row["block_until"]:
            try:
                block_until = datetime.strptime(
                    user_row["block_until"],
                    "%Y-%m-%d %H:%M:%S"
                )
            except:
                block_until = None

        if block_until and datetime.now() < block_until:
            conn.close()
            return "blocked"

        # ---------------- PASSWORD CHECK ----------------
        if bcrypt.checkpw(
            password.encode("utf-8"),
            user_row["motdepasse"].encode("utf-8")
        ):
            conn.execute("""
                UPDATE connexion
                SET login_attempts = 0,
                    block_until = NULL,
                    last_login = ?
                WHERE id_utilisateur = ?
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user.id
            ))

            conn.commit()
            conn.close()
            return user

        # ---------------- FAIL LOGIN ----------------
        attempts = (user_row["login_attempts"] or 0) + 1

        block_time = None
        if attempts >= self.MAX_LOGIN_ATTEMPTS:
            block_time = datetime.now() + self.BLOCK_TIME

        conn.execute("""
            UPDATE connexion
            SET login_attempts = ?,
                block_until = ?
            WHERE id_utilisateur = ?
        """, (
            attempts,
            block_time.strftime("%Y-%m-%d %H:%M:%S") if block_time else None,
            user.id
        ))

        conn.commit()
        conn.close()
        return None

    # ---------------- FIND ALL ----------------
    def findAll(self):
        conn = self._getDbConnection()

        rows = conn.execute("""
            SELECT u.*, c.login_attempts, c.block_until, c.last_login
            FROM utilisateur u
            LEFT JOIN connexion c
                ON u.id_utilisateur = c.id_utilisateur
        """).fetchall()

        conn.close()
        return [User(dict(r)) for r in rows]

    # ---------------- CHANGE PASSWORD ----------------
    def changePassword(self, user_id, new_password):

        if not self._is_password_strong(new_password):
            raise ValueError("Mot de passe trop faible")

        hashed = self._generatePwdHash(new_password)

        conn = self._getDbConnection()
        conn.execute("""
            UPDATE utilisateur
            SET motdepasse = ?
            WHERE id_utilisateur = ?
        """, (hashed, user_id))

        conn.commit()
        conn.close()
        return True

    # ---------------- BLOCK USER ----------------
    def block_user(self, user_id, minutes=60):

        block_until = datetime.now() + timedelta(minutes=minutes)

        conn = self._getDbConnection()
        conn.execute("""
            UPDATE connexion
            SET block_until = ?
            WHERE id_utilisateur = ?
        """, (
            block_until.strftime("%Y-%m-%d %H:%M:%S"),
            user_id
        ))

        conn.commit()
        conn.close()

    # ---------------- UNBLOCK USER ----------------
    def unblock_user(self, user_id):

        conn = self._getDbConnection()
        conn.execute("""
            UPDATE connexion
            SET block_until = NULL,
                login_attempts = 0
            WHERE id_utilisateur = ?
        """, (user_id,))

        conn.commit()
        conn.close()

    # ---------------- FIND BY ID ----------------
    def findById(self, user_id):

        conn = self._getDbConnection()

        row = conn.execute("""
            SELECT u.*, c.login_attempts, c.block_until, c.last_login
            FROM utilisateur u
            LEFT JOIN connexion c
                ON u.id_utilisateur = c.id_utilisateur
            WHERE u.id_utilisateur = ?
        """, (user_id,)).fetchone()

        conn.close()
        return User(row) if row else None