import sqlite3
import os
from app.models.Planification import Planification

class PlanificationDAO:
    def __init__(self):
        self.db_path = os.path.join(
            os.path.dirname(__file__),
            '../database.db'
        )

    def add(self, p):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO planification (
                    heure_debut, heure_fin, date_, id_playlist
                )
                VALUES (?, ?, ?, ?)
            """, (
                p.heure_debut,
                p.heure_fin,
                getattr(p, "jour_semaine", None) or getattr(p, "date_", None) or getattr(p, "date_specifique", None),
                p.id_playlist
            ))
            conn.commit()

    def get_by_lecteur(self, id_lecteur):
        query = """
        SELECT 
            p.id_planification,
            l.id_lecteur,
            p.id_playlist,
            p.heure_debut,
            p.heure_fin,
            p.date_,
            pl.nom_playlist
        FROM planification p
        LEFT JOIN playlist pl ON p.id_playlist = pl.id_playlist
        JOIN organisation o ON pl.id_organisation = o.id_organisation
        JOIN lecteur l ON o.id_organisation = l.id_organisation
        WHERE l.id_lecteur = ?
        ORDER BY 
            p.heure_debut
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, (id_lecteur,))
            rows = cursor.fetchall()
        
        planifications = []
        for row in rows:
            # CORRECTION : Utilisation des arguments nommés pour respecter le constructeur
            planif = Planification(
                id_lecteur=row[1],
                id_playlist=row[2],
                jour_semaine=row[5],  # p.date_ correspond au jour de la semaine (Lundi, Mardi...)
                heure_debut=row[3],
                heure_fin=row[4],
                id_planification=row[0]
            )
            # Ajout du nom de la playlist comme attribut dynamique
            planif.nom_playlist = row[6]
            planifications.append(planif)
        
        return planifications
    
    def find_one(self, id_planif):
        """Récupère une planification par son ID"""
        query = "SELECT id_planification, id_playlist, heure_debut, heure_fin, date_ FROM planification WHERE id_planification = ?"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, (id_planif,))
            row = cursor.fetchone()
        
        if not row:
            return None
        
        # Pour find_one, on n'a pas directement l'id_lecteur dans la table planification, 
        # on peut lui passer None ou faire une jointure si nécessaire.
        return Planification(
            id_lecteur=None,
            id_playlist=row[1],
            heure_debut=row[2],
            heure_fin=row[3],
            jour_semaine=row[4],
            id_planification=row[0]
        )
    
    def delete(self, id_planif):
        """Supprime une planification"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM planification WHERE id_planification = ?", (id_planif,))
            conn.commit()