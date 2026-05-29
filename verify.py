import sqlite3
import os

# On définit les chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'app', 'database', 'database.db')

def verif():
    print("--- VERIFICATION ---")
    print(f"Recherche du fichier ici : {DB_PATH}")
    
    if not os.path.exists(DB_PATH):
        print("ERREUR : Le fichier database.db est INTROUVABLE a cet endroit.")
        print("Verifie que tu as bien un dossier 'app' avec un dossier 'database' a l'interieur.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Lecteur")
        rows = cursor.fetchall()
        print(f"SUCCES : La table Lecteur contient {len(rows)} ligne(s).")
        for row in rows:
            print(row)
    except Exception as e:
        print(f"ERREUR SQL : {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    verif()