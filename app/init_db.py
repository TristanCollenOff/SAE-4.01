import os
import sqlite3
from datetime import datetime, timedelta
from app import app
from app.models.UserDAO import UserSqliteDAO


def init_db():

    db_path = os.path.join(app.root_path, 'database.db')
    schema_path = os.path.join(app.root_path, 'schema.sql')

    print(f"--- Initialisation de la base : {db_path} ---")

 
    if not os.path.exists(schema_path):
        print(" schema.sql introuvable")
        return

    try:
        with sqlite3.connect(db_path) as conn:
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.commit()

        print("✅ Tables créées")

    except sqlite3.Error as e:
        print(f" Erreur SQL : {e}")
        return

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        roles = [
            ("admin", "Administrateur"),
            ("superviseur", "Superviseur"),
            ("utilisateur", "Utilisateur")
        ]

        cursor.executemany(
            "INSERT OR IGNORE INTO role VALUES (?, ?)",
            roles
        )

        conn.commit()

    print("✅ Rôles OK")

   
    try:
        udao = UserSqliteDAO()

        utilisateurs = [
            ("Admin", "Admin@12345", "admin", "admin@test.com", "Admin", "System"),
            ("Antoine", "Antoine@12345", "utilisateur", "antoine@test.com", "Antoine", "User"),
            ("Superviseur", "Superviseur@12345", "superviseur", "superviseur@test.com", "Superviseur", "User")
        ]

        for username, mdp, role, email, prenom, nom in utilisateurs:

            if not udao.findByUsername(username):
                udao.createUser(
                    username,
                    mdp,
                    role,
                    email=email,
                    prenom=prenom,
                    nom=nom
                )
                print(f"👤 {username} créé")

    except Exception as e:
        print(f" Erreur users : {e}")


    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR IGNORE INTO organisation
                (id_organisation, nom_organisation)
                VALUES (1, 'Magasin Rythmo')
            """)

            cursor.execute("""
                INSERT OR IGNORE INTO lecteur (
                    id_lecteur,
                    nom_lecteur,
                    adresseIP,
                    etat_lecteur,
                    emplacement,
                    derniere_synchro,
                    adresse_lecteur,
                    alerte,
                    id_organisation
                )
                VALUES (
                    1,
                    'Lecteur RPi5',
                    '10.192.104.28',
                    'UP',
                    'Rayon Frais',
                    DATE('now'),
                    'Magasin',
                    0,
                    1
                )
            """)

            conn.commit()

        print("Organisation + lecteur OK")

    except Exception as e:
        print(f" Erreur org/lecteur : {e}")

  
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT id_utilisateur FROM utilisateur")
            users = cursor.fetchall()

            for (user_id,) in users:
                cursor.execute("""
                    INSERT OR IGNORE INTO affilier
                    (id_utilisateur, id_organisation)
                    VALUES (?, ?)
                """, (user_id, 1))

            conn.commit()

        print(" Affiliation OK")

    except Exception as e:
        print(f" Erreur affilier : {e}")

   
    print("\n--- Génération démo ---")
    generate_demo_playlists(db_path)


def generate_demo_playlists(db_path):

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        today = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT OR IGNORE INTO type_fichier
            VALUES ('audio/mp3')
        """)

        cursor.execute("SELECT COUNT(*) FROM playlist")
        if cursor.fetchone()[0] > 0:
            print("ℹ playlists déjà présentes")
            return

        fichiers = [
            ("Morning Vibes", "/musique/matin/m1.mp3", 210),
            ("Sunrise Energy", "/musique/matin/m2.mp3", 195),
            ("Fresh Start", "/musique/matin/m3.mp3", 180),
        ]

        for nom, chemin, duree in fichiers:
            cursor.execute("""
                INSERT INTO fichier
                (nom, chemin, duree_fichier, date_maj, type_fichier)
                VALUES (?, ?, ?, ?, ?)
            """, (nom, chemin, duree, today, "audio/mp3"))

        week = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        fin = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO playlist (
                nom_playlist,
                date_creation,
                date_fin_playlist,
                date_derniere_maj,
                publie,
                id_organisation
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Playlist Matin",
            week,
            fin,
            today,
            1,
            1
        ))

        id_playlist = cursor.lastrowid

        for nom, _, _ in fichiers:
            cursor.execute("SELECT id_fichier FROM fichier WHERE nom = ?", (nom,))
            res = cursor.fetchone()

            if res:
                cursor.execute("""
                    INSERT INTO Contenir
                    (id_playlist, id_fichier)
                    VALUES (?, ?)
                """, (id_playlist, res[0]))

        conn.commit()
        conn.close()

        print(" Démo OK")

    except Exception as e:
        print(f" erreur démo : {e}")


if __name__ == "__main__":
    init_db()