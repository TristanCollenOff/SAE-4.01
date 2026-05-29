from app.models.PlanificationDAO import PlanificationDAO
from app.services.log_service import add_log

class PlanificationService:
    def __init__(self):
        self.dao = PlanificationDAO()

    def planifier(self, planif, username):
        self.dao.add(planif)
        # Type 'info' pour incrémenter la case bleue du journal
        add_log("info", username, f"A planifié une playlist pour le jour : {planif.jour_semaine}")