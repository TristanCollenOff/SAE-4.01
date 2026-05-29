from app.models.UserDAO import UserSqliteDAO as UserDAO
from app.models.User import User

class UserService():
    """Classe dédiée à la logique des utilisateurs"""

    def __init__(self):
        self.udao = UserDAO()

    # -------------------
    # Création utilisateur
    # -------------------
    def create_user(self, username, password, role='utilisateur', prenom="", nom="", age=None, email=""):
        """
        Crée un utilisateur et applique toutes les vérifications :
        - mot de passe fort
        - unicité username/email
        """
        return self.udao.createUser(username, password, role, prenom, nom, age, email)

    # -------------------
    # Récupérer utilisateur
    # -------------------
    def getUserByUsername(self, nom_utilisateur):
        res = self.udao.findByUsername(nom_utilisateur)
        if type(res) is not list: 
            res = [res] 
        return res

    def getUsers(self):
        return self.udao.findAll()

    # -------------------
    # Connexion
    # -------------------
    def login(self, nom_utilisateur, motdepasse):
        """
        Retourne :
        - User si login OK
        - 'blocked' si compte temporairement bloqué
        - None si login incorrect
        """
        result = self.udao.verifyUser(nom_utilisateur, motdepasse)
        if result == "blocked":
            return "blocked"
        elif result:
            # Login OK → reset tentative
            self.udao.resetLoginAttempts(result.id)
            result.start_session()  # session active dans User
            return result
        else:
            # Login échoué → incrémente tentative
            user = self.udao.findByUsername(nom_utilisateur)
            if user:
                self.udao.recordFailedLogin(user.id)
            return None

    # -------------------
    # Changement mot de passe
    # -------------------
    def change_password(self, user_id, new_password):
        return self.udao.changePassword(user_id, new_password)

    # -------------------
    # Contrôle d'accès
    # -------------------
    def has_access(self, user: User, resource_role):
        """
        Vérifie si un utilisateur a accès à une ressource selon son rôle
        """
        return user.has_access(resource_role)

    # -------------------
    # Réinitialisation mot de passe via email
    # -------------------
    def reset_password(self, email, new_password):
        all_users = self.udao.findAll()
        user = next((u for u in all_users if u.email == email), None)
        if user:
            return self.udao.changePassword(user.id, new_password)
        return False

    def block_user(self, user_id, minutes=60):
     return self.udao.block_user(user_id, minutes)

    def unblock_user(self, user_id):
     return self.udao.unblock_user(user_id)
   
    def getUserById(self, user_id):
     return self.udao.findById(user_id)



