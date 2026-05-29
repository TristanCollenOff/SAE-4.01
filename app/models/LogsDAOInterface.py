from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.Logs import Logs

class LogsDAOInterface(ABC):
    
    @abstractmethod
    def add_log(self, log: Logs) -> bool:
        """
        Ajoute une nouvelle entrée de log

        """
        pass
    
    @abstractmethod
    def get_all_logs(self) -> List[Logs]:
        """
        Récupère tous les logs

        """
        pass
    
    @abstractmethod
    def get_log_by_id(self, log_id: int) -> Optional[Logs]:
        """
        Récupère un log par son ID

        """
        pass
    
    @abstractmethod
    def get_logs_by_user(self, user_id: int) -> List[Logs]:
        """
        Récupère tous les logs d'un utilisateur

        """
        pass
    
    @abstractmethod
    def get_logs_by_type(self, log_type: str) -> List[Logs]:
        """
        Récupère tous les logs d'un type spécifique
 
        """
        pass
    
    @abstractmethod
    def search_logs(self, search_term: str) -> List[Logs]:
        """
        Recherche des logs par terme de recherche (dans username ou message)
        
        """
        pass
    
    @abstractmethod
    def delete_log(self, log_id: int) -> bool:
        """
        Supprime un log par son ID

        """
        pass
    
    @abstractmethod
    def delete_old_logs(self, days: int) -> int:
        """
        Supprime les logs plus anciens que X jours

        """
        pass