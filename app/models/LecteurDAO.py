import sqlite3
import os
from app import app
from app.models.Lecteur import Lecteur

class LecteurDAO:


    def __init__(self):
        # On trouve le chemin du dossier 'app' (un niveau au-dessus de 'models')
        APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # La base est directement dans 'app' selon tes dires
        self.db_path = os.path.join(APP_DIR, 'database.db')
        
        # Pour être SÛR, on affiche le chemin dans la console au démarrage
        print(f"--- CONFIGURATION DAO ---")
        print(f"Recherche de la BDD ici : {self.db_path}")
        if os.path.exists(self.db_path):
            print("STATUT : Fichier trouve !")
        else:
            print("STATUT : Fichier INTROUVABLE !")

    def find_all(self):
        """Récupère la liste de TOUS les lecteurs."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM Lecteur")
            rows = cursor.fetchall()
            conn.close()

            lecteurs = []
            for row in rows:
                lecteur = Lecteur(
                    row['id_lecteur'],
                    row['nom_lecteur'],
                    row['adresseIP'],
                    row['etat_lecteur'],
                    row['derniere_synchro'],
                    row['adresse_lecteur']
                )
                lecteurs.append(lecteur)
            return lecteurs
        except Exception as e:
            print(f"Erreur find_all : {e}")
            return []

    def find_one(self, id_lecteur):
        """Récupère UN SEUL lecteur grâce à son ID."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM Lecteur WHERE id_lecteur = ?", (id_lecteur,))
            row = cursor.fetchone()
            conn.close()

            if row:
                return Lecteur(
                    row['id_lecteur'],
                    row['nom_lecteur'],
                    row['adresseIP'],
                    row['etat_lecteur'],
                    row['derniere_synchro'],
                    row['adresse_lecteur']
                )
            return None
        except Exception as e:
            print(f"Erreur find_one : {e}")
            return None
        
    def create(self, nom_lecteur, adresseIP, adresse_lecteur):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # On ajoute id_organisation (met 1 par défaut pour tes tests)
            query = """
                INSERT INTO Lecteur (nom_lecteur, adresseIP, adresse_lecteur, etat_lecteur, derniere_synchro, id_organisation)
                VALUES (?, ?, ?, 'Hors ligne', 'Jamais', 1)
            """
            
            cursor.execute(query, (nom_lecteur, adresseIP, adresse_lecteur))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erreur création lecteur : {e}")
            return False
    def update_nom(self, id_lecteur, nouveau_nom):
        """Met à jour uniquement le nom du lecteur"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # On cible uniquement la colonne nom_lecteur
            cursor.execute("UPDATE Lecteur SET nom_lecteur = ? WHERE id_lecteur = ?", (nouveau_nom, id_lecteur))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erreur update_nom : {e}")
            return False
        def delete(self, id_lecteur):
            """ Supprime un lecteur définitivement """
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM Lecteur WHERE id_lecteur = ?", (id_lecteur,))
                
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print(f"Erreur suppression lecteur : {e}")
                return False
            
    def set_online(self, id_lecteur):
            """ Note que le lecteur est EN LIGNE et met à jour l'heure """
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                # On met 'OK' et l'heure actuelle
                cursor.execute("UPDATE Lecteur SET etat_lecteur = 'UP', derniere_synchro = datetime('now', 'localtime') WHERE id_lecteur = ?", (id_lecteur,))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print(f"Erreur set_online : {e}")
                return False
    def changer_playlist(self, id_lecteur, nom_playlist):
        """Change la playlist active (matin, midi ou soir)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE Lecteur SET playlist_active = ? WHERE id_lecteur = ?", (nom_playlist, id_lecteur))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erreur changement playlist : {e}")
            return False

    def toggle_alerte(self, id_lecteur, etat):
        """Active ou désactive l'alerte d'urgence (0 ou 1)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE Lecteur SET alerte_active = ? WHERE id_lecteur = ?", (etat, id_lecteur))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erreur alerte : {e}")
            return False