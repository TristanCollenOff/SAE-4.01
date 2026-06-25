import os
import sqlite3
import bcrypt
from datetime import datetime, timedelta


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def init_db():

    BASE_DIR = os.path.dirname(__file__)

    db_path = os.path.join(BASE_DIR, "database.db")
    schema_path = os.path.join(BASE_DIR, "schema.sql")

    print(f"--- Initialisation de la base : {db_path} ---")

    if not os.path.exists(schema_path):
        print("❌ schema.sql introuvable")
        return

    try:
        with sqlite3.connect(db_path) as conn:
            with open(schema_path, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.commit()

        print("✅ Tables créées")

    except sqlite3.Error as e:
        print(f"❌ Erreur SQL : {e}")
        return

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            roles = [
                ("admin", "Administrateur"),
                ("marketing", "Marketing"),
                ("commercial", "Commercial"),
            ]

            cursor.executemany(
                "INSERT OR IGNORE INTO role VALUES (?, ?)",
                roles
            )

            conn.commit()

        print("✅ Rôles OK")

    except Exception as e:
        print(f"❌ Erreur rôles : {e}")

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            users = [
                ("Admin", hash_password("Admin@12345"), "Admin", "System", "admin@test.com", "admin"),
                ("Commercial", hash_password("Commercial@12345"), "Antoine", "User", "commercial@test.com", "commercial"),
                ("Marketing", hash_password("Marketing@12345"), "Marie", "User", "marketing@test.com", "marketing"),
            ]

            cursor.executemany(
                """
                INSERT OR IGNORE INTO utilisateur
                (nom_utilisateur, motdepasse, prenom, nom, email, nom_role)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                users
            )

            conn.commit()

        print("👤 Users OK (bcrypt)")

    except Exception as e:
        print("❌ Erreur users :", e)

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            organisations = [
                (1, "FNAC"),
                (2, "NASA"),
                (3, "Gare SNCF"),
                (4, "Université"),
                (5, "Aéroport"),
                (6, "Salle de sport"),
            ]

            cursor.executemany(
                """
                INSERT OR IGNORE INTO organisation
                (id_organisation, nom_organisation)
                VALUES (?, ?)
                """,
                organisations
            )

            lecteurs = [
                (1, "Lecteur FNAC", "10.192.104.28", "UP", "Accueil", "FNAC", 0, 1),
                (2, "Lecteur NASA", "10.192.104.29", "UP", "Rayon Frais", "NASA", 0, 2),
                (3, "Lecteur Gare SNCF", "10.192.104.30", "UP", "Hall principal", "Gare SNCF", 0, 3),
                (4, "Lecteur Université", "10.192.104.31", "UP", "Bibliothèque", "Université", 0, 4),
                (5, "Lecteur Aéroport", "10.192.104.32", "UP", "Terminal 1", "Aéroport", 0, 5),
                (6, "Lecteur Salle de sport", "10.192.104.33", "UP", "Accueil sport", "Salle de sport", 0, 6),
            ]

            cursor.executemany(
                """
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
                VALUES (?, ?, ?, ?, ?, DATE('now'), ?, ?, ?)
                """,
                lecteurs
            )

            conn.commit()

        print("✅ Organisations + lecteurs OK")

    except Exception as e:
        print(f"❌ Erreur org/lecteur : {e}")

    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT id_utilisateur FROM utilisateur")
            users = cursor.fetchall()

            cursor.execute("SELECT id_organisation FROM organisation")
            organisations = cursor.fetchall()

            for (user_id,) in users:
                for (id_organisation,) in organisations:
                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO affilier
                        (id_utilisateur, id_organisation)
                        VALUES (?, ?)
                        """,
                        (user_id, id_organisation)
                    )

            conn.commit()

        print("✅ Affiliation OK")

    except Exception as e:
        print(f"❌ Erreur affilier : {e}")

    
    print("\n--- Génération démo ---")
    generate_demo_playlists(db_path)


def generate_demo_playlists(db_path):

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        today = datetime.now().strftime("%Y-%m-%d")
        week = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        fin = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT OR IGNORE INTO type_fichier
            VALUES ('audio/mp3')
        """)

        cursor.execute("SELECT COUNT(*) FROM playlist")
        if cursor.fetchone()[0] > 0:
            print("ℹ playlists déjà présentes")
            conn.close()
            return

        ambiances = {
            "default": {
                "playlist": "Playlist en cours",
                "dossier": "en_cours",
                "musiques": [
                    ("Onde Première", 205),
                    ("Tempo Initial", 188),
                    ("Musique", 214),
                    ("Pulse d'Accueil", 196),
                    ("Harmonie Centrale", 202),
                ],
            },
            "joyeux": {
                "playlist": "Playlist Joyeuse",
                "dossier": "joyeux",
                "musiques": [
                    ("Soleil Pop", 198),
                    ("Sourire Urbain", 185),
                    ("Happy Groove", 211),
                    ("Énergie Positive", 192),
                    ("Confettis Sonores", 204),
                ],
            },
            "triste": {
                "playlist": "Playlist Mélancolique",
                "dossier": "triste",
                "musiques": [
                    ("Pluie Bleue", 220),
                    ("Souvenir Lent", 207),
                    ("Piano Gris", 231),
                    ("Mélodie Perdue", 216),
                    ("Nuages", 199),
                ],
            },
            "nature": {
                "playlist": "Playlist Nature",
                "dossier": "nature",
                "musiques": [
                    ("Forêt Calme", 218),
                    ("Rivière Douce", 224),
                    ("Vent Léger", 206),
                    ("Feuilles Vertes", 213),
                    ("Horizon Nature", 229),
                ],
            },
            "romantique": {
                "playlist": "Playlist Romantique",
                "dossier": "romantique",
                "musiques": [
                    ("Cœur de Velours", 215),
                    ("Slow Love", 208),
                    ("Rose Spatiale", 221),
                    ("Baiser Musical", 212),
                    ("Douce Romance", 226),
                ],
            },
            "voyage_spacial": {
                "playlist": "Playlist Voyage Spacial",
                "dossier": "voyage_spacial",
                "musiques": [
                    ("Midnight Drive", 217),
                    ("Lune Synth", 203),
                    ("Étoiles Basses", 219),
                    ("Silence Urbain", 210),
                    ("Bleu Spatial", 228),
                ],
            },
        }

        for ambiance in ambiances.values():
            id_fichiers = []

            for index, (nom_musique, duree) in enumerate(ambiance["musiques"], start=1):
                chemin = f"/musique/{ambiance['dossier']}/m{index}.mp3"

                cursor.execute(
                    """
                    INSERT INTO fichier
                    (nom, chemin, duree_fichier, date_maj, type_fichier)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (nom_musique, chemin, duree, today, "audio/mp3")
                )

                id_fichiers.append(cursor.lastrowid)

            cursor.execute(
                """
                INSERT INTO playlist (
                    nom_playlist,
                    date_creation,
                    date_fin_playlist,
                    date_derniere_maj,
                    publie,
                    id_organisation
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    ambiance["playlist"],
                    week,
                    fin,
                    today,
                    1,
                    1
                )
            )

            id_playlist = cursor.lastrowid

            for id_fichier in id_fichiers:
                cursor.execute(
                    """
                    INSERT INTO Contenir
                    (id_playlist, id_fichier)
                    VALUES (?, ?)
                    """,
                    (id_playlist, id_fichier)
                )

        conn.commit()
        conn.close()

        print("✅ Démo playlists par ambiance OK")

    except Exception as e:
        print(f"❌ erreur démo : {e}")


if __name__ == "__main__":
    init_db()