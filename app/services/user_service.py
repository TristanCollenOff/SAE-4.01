from app.models.UserDAO import UserSqliteDAO as UserDAO
from app.models.User import User


class UserService:

    def __init__(self):
        self.udao = UserDAO()

    # -------------------
    # CREATE USER
    # -------------------
    def create_user(self, username, password, role='utilisateur',
                    prenom="", nom="", age=None, email=""):
        return self.udao.createUser(username, password, role, prenom, nom, email)

    # -------------------
    # GET USER BY USERNAME
    # -------------------
    def getUserByUsername(self, username):
        return self.udao.findByUsername(username)

    # -------------------
    # GET ALL USERS
    # -------------------
    def getUsers(self):
        return self.udao.findAll()

    # -------------------
    # LOGIN FLOW
    # -------------------
    def login(self, username, password):
        result = self.udao.verifyUser(username, password)

        if result == "blocked":
            return "blocked"

        if result:
            result.start_session()
            return result

        return None

    # -------------------
    # PASSWORD
    # -------------------
    def change_password(self, user_id, new_password):
        return self.udao.changePassword(user_id, new_password)

    # -------------------
    # ACCESS CONTROL
    # -------------------
    def has_access(self, user: User, resource_role):
        return user.has_access(resource_role)

    # -------------------
    # RESET PASSWORD
    # -------------------
    def reset_password(self, email, new_password):
        users = self.udao.findAll()
        user = next((u for u in users if u.email == email), None)

        if user:
            return self.udao.changePassword(user.id, new_password)

        return False

    # -------------------
    # BLOCK / UNBLOCK
    # -------------------
    def block_user(self, user_id, minutes=60):
        return self.udao.block_user(user_id, minutes)

    def unblock_user(self, user_id):
        return self.udao.unblock_user(user_id)

    # -------------------
    # GET BY ID
    # -------------------
    def getUserById(self, user_id):
        return self.udao.findById(user_id)