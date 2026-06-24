from app.models.PlanificationDAO import PlanificationDAO
from app.services.log_service import add_log

class PlanificationService:
    def __init__(self):
        self.dao = PlanificationDAO()

    def planifier(self, planif, username):
        self.dao.add(planif)
        # Utilisation de jour_semaine de l'objet de manière sécurisée
        jour = getattr(planif, 'jour_semaine', 'Inconnu')
        add_log("info", username, f"A planifié une playlist pour le jour : {jour}")