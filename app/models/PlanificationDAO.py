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
                INSERT INTO Planification (
                    id_lecteur, id_playlist, jour_semaine, heure_debut, heure_fin
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                p.id_lecteur,
                p.id_playlist,
                p.jour_semaine,
                p.heure_debut,
                p.heure_fin
            ))
            conn.commit()

    def get_by_lecteur(self, id_lecteur):
        query = """
        SELECT 
            p.id_planification,
            p.id_lecteur,
            p.id_playlist,
            p.jour_semaine,
            p.heure_debut,
            p.heure_fin,
            p.date_specifique,
            pl.nom_playlist
        FROM Planification p
        LEFT JOIN Playlist pl ON p.id_playlist = pl.id_playlist
        WHERE p.id_lecteur = ?
        ORDER BY 
            CASE p.jour_semaine
                WHEN 'Lundi' THEN 1
                WHEN 'Mardi' THEN 2
                WHEN 'Mercredi' THEN 3
                WHEN 'Jeudi' THEN 4
                WHEN 'Vendredi' THEN 5
                WHEN 'Samedi' THEN 6
                WHEN 'Dimanche' THEN 7
            END,
            p.heure_debut
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, (id_lecteur,))
            rows = cursor.fetchall()
        
        planifications = []
        for row in rows:
            planif = Planification(
                row[1],  # id_lecteur
                row[2],  # id_playlist
                row[3],  # jour_semaine
                row[4],  # heure_debut
                row[5],  # heure_fin
                row[6],  # date_specifique
                row[0],  # id_planification
            )
            # Ajouter le nom de la playlist comme attribut dynamique
            planif.nom_playlist = row[7]  # nom_playlist depuis la jointure
            planifications.append(planif)
        
        return planifications
    
    def find_one(self, id_planif):
        """Récupère une planification par son ID"""
        query = "SELECT * FROM Planification WHERE id_planification = ?"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, (id_planif,))
            row = cursor.fetchone()
        
        if not row:
            return None
        
        return Planification(
            row[1],  # id_lecteur
            row[2],  # id_playlist
            row[3],  # jour_semaine
            row[4],  # heure_debut
            row[5],  # heure_fin
            row[6],  # date_specifique
            row[0],  # id_planification
        )
    
    def delete(self, id_planif):
        """Supprime une planification"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM Planification WHERE id_planification = ?", (id_planif,))
            conn.commit()