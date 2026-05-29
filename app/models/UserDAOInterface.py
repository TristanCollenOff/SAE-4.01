class UserDAOInterface:
    """Interface pour le DAO user"""

    def createUser(self, username, password, role='utilisateur', prenom="", nom="", age=None, email=""):
        """
        Crée un utilisateur.
        - Vérifie la complexité du mot de passe
        - Vérifie unicité username/email
        """
        pass

    def findByUsername(self, username):
        """
        Trouve un utilisateur par son nom d'utilisateur
        Retourne une instance User ou None
        """
        pass

    def verifyUser(self, username, password):
        """
        Vérifie les informations de connexion et retourne :
        - l'instance User si login OK
        - "blocked" si le compte est temporairement bloqué
        - None si login incorrect
        """
        pass

    def findAll(self):
        """Retourne la liste de tous les utilisateurs"""
        pass

    def changePassword(self, user_id, new_password):
        """
        Permet de changer le mot de passe d'un utilisateur
        - Vérifie la complexité du mot de passe
        """
        pass

    def recordFailedLogin(self, user_id):
        """
        Incrémente le nombre de tentatives échouées et bloque si nécessaire
        """
        pass

    def resetLoginAttempts(self, user_id):
        """
        Réinitialise les tentatives après login réussi ou fin de blocage
        """
        pass


	
