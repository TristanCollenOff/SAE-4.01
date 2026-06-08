import sqlite3
import os
from typing import List, Optional
from app.models.Logs import Logs
from app.models.LogsDAOInterface import LogsDAOInterface

class LogsDAO(LogsDAOInterface):
    
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
                    """INSERT INTO fichier_log (type_action, message, date_fichierlog, id_organisation) 
                       VALUES (?, ?, ?, ?)""",
                    (log.type_action, log.message, log.date_fichierlog, log.id_organisation)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Erreur DAO lors de l'ajout du log : {e}")
            return False
        
    def get_all_logs(self) -> List[Logs]:
        """Récupère tous les logs triés par date décroissante"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM fichier_log ORDER BY date_fichierlog DESC"
                )
                rows = cursor.fetchall()
                return [Logs.from_dict(dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la récupération des logs : {e}")
            return []
    
    def get_log_by_id(self, log_id: int) -> Optional[Logs]:
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM fichier_log WHERE id_log = ?",
                    (log_id,)
                )
                row = cursor.fetchone()
                return Logs.from_dict(dict(row)) if row else None
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la récupération du log {log_id} : {e}")
            return None
    
    def get_logs_by_organisation(self, org_id: int) -> List[Logs]:
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM fichier_log WHERE id_organisation = ? ORDER BY date_fichierlog DESC",
                    (org_id,)
                )
                rows = cursor.fetchall()
                return [Logs.from_dict(dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la récupération des logs de l'organisation {org_id} : {e}")
            return []
    
    def get_logs_by_type(self, log_type: str) -> List[Logs]:
        """Récupère tous les logs d'un type d'action spécifique"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM fichier_log WHERE type_action = ? ORDER BY date_fichierlog DESC",
                    (log_type,)
                )
                rows = cursor.fetchall()
                return [Logs.from_dict(dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la récupération des logs de type {log_type} : {e}")
            return []
    
    def search_logs(self, search_term: str) -> List[Logs]:
        """Recherche des logs par terme de recherche (uniquement dans le message désormais)"""
        try:
            search_pattern = f"%{search_term.lower()}%"
            with self._get_connection() as conn:
                cursor = conn.execute(
                    """SELECT * FROM fichier_log 
                       WHERE LOWER(message) LIKE ?
                       ORDER BY date_fichierlog DESC""",
                    (search_pattern,)
                )
                rows = cursor.fetchall()
                return [Logs.from_dict(dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la recherche de logs : {e}")
            return []
    
    def delete_log(self, log_id: int) -> bool:
        """Supprime un log par son id_log"""
        try:
            with self._get_connection() as conn:
                conn.execute(
                    "DELETE FROM fichier_log WHERE id_log = ?",
                    (log_id,)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la suppression du log {log_id} : {e}")
            return False
    
    def delete_old_logs(self, days: int) -> int:

        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "DELETE FROM fichier_log WHERE date_fichierlog < datetime('now', '-' || ? || ' days')",
                    (days,)
                )
                conn.commit()
                return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la suppression des anciens logs : {e}")
            return 0