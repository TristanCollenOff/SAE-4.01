import sqlite3
import os
from typing import List, Optional
from app.models.Logs import Logs
from app.models.LogsDAOInterface import LogsDAOInterface

class LogsDAO(LogsDAOInterface):
    """Data Access Object pour les logs"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            self.db_path = os.path.join(os.path.dirname(__file__), '../database.db')
        else:
            self.db_path = db_path
    
    def _get_connection(self):
        """Crée et retourne une connexion à la base de données"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def add_log(self, log: Logs) -> bool:
        try:
            with self._get_connection() as conn:
                conn.execute(
                    """INSERT INTO FichierLog (user_id, username, type_log, message, date_fichierlog) 
                   VALUES (?, ?, ?, ?, datetime('now'))""",
                    (log.user_id, log.username, log.type_log, log.message)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Erreur DAO : {e}")
            return False
        
    def get_all_logs(self) -> List[Logs]:
        """
        Récupère tous les logs
        
        Returns:
            List[Logs]: Liste de tous les logs triés par date décroissante
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM FichierLog ORDER BY date_fichierlog DESC"
                )
                rows = cursor.fetchall()
                return [Logs.from_dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la récupération des logs : {e}")
            return []
    
    def get_log_by_id(self, log_id: int) -> Optional[Logs]:
        """
        Récupère un log par son ID
        
        Args:
            log_id: ID du log
            
        Returns:
            Optional[Logs]: Le log trouvé ou None
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM FichierLog WHERE id_fichierlog = ?",
                    (log_id,)
                )
                row = cursor.fetchone()
                return Logs.from_dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la récupération du log {log_id} : {e}")
            return None
    
    def get_logs_by_user(self, user_id: int) -> List[Logs]:
        """
        Récupère tous les logs d'un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            List[Logs]: Liste des logs de l'utilisateur
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM FichierLog WHERE user_id = ? ORDER BY date_fichierlog DESC",
                    (user_id,)
                )
                rows = cursor.fetchall()
                return [Logs.from_dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la récupération des logs de l'utilisateur {user_id} : {e}")
            return []
    
    def get_logs_by_type(self, log_type: str) -> List[Logs]:
        """
        Récupère tous les logs d'un type spécifique
        
        Args:
            log_type: Type de log
            
        Returns:
            List[Logs]: Liste des logs du type spécifié
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM FichierLog WHERE type_log = ? ORDER BY date_fichierlog DESC",
                    (log_type,)
                )
                rows = cursor.fetchall()
                return [Logs.from_dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la récupération des logs de type {log_type} : {e}")
            return []
    
    def search_logs(self, search_term: str) -> List[Logs]:
        """
        Recherche des logs par terme de recherche (dans username ou message)
        
        Args:
            search_term: Terme à rechercher
            
        Returns:
            List[Logs]: Liste des logs correspondants
        """
        try:
            search_pattern = f"%{search_term.lower()}%"
            with self._get_connection() as conn:
                cursor = conn.execute(
                    """SELECT * FROM FichierLog 
                       WHERE LOWER(username) LIKE ? OR LOWER(message) LIKE ?
                       ORDER BY date_fichierlog DESC""",
                    (search_pattern, search_pattern)
                )
                rows = cursor.fetchall()
                return [Logs.from_dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la recherche de logs : {e}")
            return []
    
    def delete_log(self, log_id: int) -> bool:
        """
        Supprime un log par son ID
        
        Args:
            log_id: ID du log à supprimer
            
        Returns:
            bool: True si la suppression a réussi, False sinon
        """
        try:
            with self._get_connection() as conn:
                conn.execute(
                    "DELETE FROM FichierLog WHERE id_fichierlog = ?",
                    (log_id,)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la suppression du log {log_id} : {e}")
            return False
    
    def delete_old_logs(self, days: int) -> int:
        """
        Supprime les logs plus anciens que X jours
        
        Args:
            days: Nombre de jours
            
        Returns:
            int: Nombre de logs supprimés
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "DELETE FROM FichierLog WHERE date_fichierlog < datetime('now', '-' || ? || ' days')",
                    (days,)
                )
                conn.commit()
                return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la suppression des anciens logs : {e}")
            return 0