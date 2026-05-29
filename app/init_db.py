import os
import sqlite3
from datetime import datetime, timedelta
from app import app
from app.models.UserDAO import UserSqliteDAO

def init_db():
    # 1. On cible les bons chemins (BDD et Schema dans /app)
    db_path = os.path.join(app.root_path, 'database.db')
    schema_path = os.path.join(app.root_path, 'schema.sql')

    print(f"--- Initialisation de la base : {db_path} ---")

    # 2. Création de la structure (Tables)
    if not os.path.exists(schema_path):
        print(f"❌ Erreur : '{schema_path}' introuvable.")
        return

    try:
        with sqlite3.connect(db_path) as conn:
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.commit()
        print("✅ Tables créées.")
    except sqlite3.Error as e:
        print(f"❌ Erreur SQL : {e}")
        return

    # 3. Insertion des utilisateurs (Admin, Antoine, etc.)
    try:
        udao = UserSqliteDAO()
        utilisateurs = [
            {"nom": "Admin", "mdp": "Admin@12345", "role": "admin", "email": "admin@test.com"},
            {"nom": "Antoine", "mdp": "Antoine@12345", "role": "utilisateur", "email": "antoine@test.com"},
            {"nom": "Superviseur", "mdp": "Superviseur@12345", "role": "superviseur", "email": "superviseur@test.com"}
        ]
       
        for u in utilisateurs:
            if not udao.findByUsername(u["nom"]):
                udao.createUser(u["nom"], u["mdp"], u["role"], email=u["email"])
                print(f" 👤 Utilisateur '{u['nom']}' créé.")

        # 4. Insertion Organisation et TON Lecteur AirPods
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO Organisation (id_organisation, nom_organisation) VALUES (1, 'Magasin Rythmo')")
            
            # ICI : On met l'IP de TA Raspberry pour que ça marche direct
            cursor.execute("""
                INSERT OR IGNORE INTO Lecteur 
                (id_lecteur, nom_lecteur, adresseIP, etat_lecteur, adresse_lecteur, id_organisation) 
                VALUES (1, 'Lecteur RPi5', '10.192.104.28', 'UP', 'Rayon Frais', 1)
            """)
            conn.commit()
        print("✅ Organisation et Lecteur RPi5 configurés.")

        # 5. Génération des playlists de démo
        print("\n--- Génération des données de démo ---")
        generate_demo_playlists(db_path)

    except Exception as e:
        print(f"❌ Erreur lors de l'insertion : {e}")


def generate_demo_playlists(db_path):
    """
    Génère des playlists de démo avec des fichiers musicaux fictifs
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si des playlists existent déjà
        cursor.execute("SELECT COUNT(*) FROM Playlist")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"ℹ️  {count} playlist(s) existante(s), génération ignorée.")
            conn.close()
            return
        
        # 1. Créer des fichiers musicaux de démo
        fichiers_demo = [
            # Musiques pour playlist Matin
            ("Morning Vibes", "/musique/matin/musiquematin1.mp3", 210),
            ("Sunrise Energy", "/musique/matin/musiquematin2.mp3", 195),
            ("Fresh Start", "/musique/matin/musiquematin3.mp3", 180),
            
            # Musiques pour playlist midi
            ("Afternoon Groove", "/musique/midi/musiquemidi1.mp3", 200),
            ("Chill Hours", "/musique/midi/musiquemidi2.mp3", 215),
            ("Sunny Day", "/musique/musiquemidi/musiquemidi2.mp3", 190),
            
            # Musiques pour playlist Soirée
            ("Evening Mood", "/musique/soir/musiquesoir1.mp3", 240),
            ("Sunset Chill", "/musique/soir/musiquesoir2.mp3", 230),
            ("Night Vibes", "/musique/soir/musiquesoir3.mp3", 220),

            # Musique pour playlist Secours
            ("Emergency Loop", "/music/fallback/emergency_loop.mp3", 180),
            
            # Musiques pour playlist Test (incomplète)
            ("Test Track 1", "/music/test/test1.mp3", 150),
            ("Test Track 2", "/music/test/test2.mp3", 160),
            ("Test Track 3", "", 170),  # Fichier manquant pour tester les erreurs
        ]
        
        print("📀 Insertion des fichiers musicaux...")
        for nom, emplacement, duree in fichiers_demo:
            cursor.execute("""
                INSERT INTO Fichier (nom, emplacement, duree_fichier)
                VALUES (?, ?, ?)
            """, (nom, emplacement, duree))
        
        # 2. Créer les playlists
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        playlists_demo = [
            {
                "nom": "Playlist Matin",
                "date_creation": week_ago,
                "date_maj": today,
                "publie": 1,
                "fichiers": ["musiquematin1", "Sunrise Energy", "Fresh Start"]
            },
            {
                "nom": "Ambiance Après-midi",
                "date_creation": week_ago,
                "date_maj": yesterday,
                "publie": 1,
                "fichiers": ["Afternoon Groove", "Chill Hours", "Sunny Day", "Smooth Sailing", "Easy Listening", 
                            "Peaceful Moments", "Relaxing Beats", "Soft Melodies"]
            },
            {
                "nom": "Ambiance Soirée",
                "date_creation": week_ago,
                "date_maj": today,
                "publie": 1,
                "fichiers": ["Evening Mood", "Sunset Chill", "Night Vibes", "Dinner Jazz", "Mellow Evening", 
                            "Cozy Night", "Starlight"]
            },
            {
                "nom": "Secours Loop",
                "date_creation": week_ago,
                "date_maj": week_ago,
                "publie": 1,
                "fichiers": ["Emergency Loop"]
            },
            {
                "nom": "Playlist Test",
                "date_creation": today,
                "date_maj": today,
                "publie": 0,  # Brouillon
                "fichiers": ["Test Track 1", "Test Track 2", "Test Track 3"]
            }
        ]
        
        print("🎵 Insertion des playlists...")
        for playlist in playlists_demo:
            # Insérer la playlist
            cursor.execute("""
                INSERT INTO Playlist (nom_playlist, date_creation, date_derniere_maj, publie)
                VALUES (?, ?, ?, ?)
            """, (playlist["nom"], playlist["date_creation"], playlist["date_maj"], playlist["publie"]))
            
            id_playlist = cursor.lastrowid
            print(f"  ✅ Playlist '{playlist['nom']}' créée (ID: {id_playlist})")
            
            # Associer les fichiers à la playlist
            for nom_fichier in playlist["fichiers"]:
                cursor.execute("SELECT id_fichier FROM Fichier WHERE nom = ?", (nom_fichier,))
                fichier_result = cursor.fetchone()
                
                if fichier_result:
                    id_fichier = fichier_result[0]
                    cursor.execute("""
                        INSERT INTO Est_composé_d_une (id_playlist, id_fichier)
                        VALUES (?, ?)
                    """, (id_playlist, id_fichier))
        
        conn.commit()
        conn.close()
        
        print(f"\n✅ {len(playlists_demo)} playlists de démo créées avec succès!")
        print("\n📊 Résumé:")
        print(f"  - {len(fichiers_demo)} fichiers musicaux créés")
        print(f"  - Playlists publiées: {sum(1 for p in playlists_demo if p['publie'] == 1)}")
        print(f"  - Playlists en brouillon: {sum(1 for p in playlists_demo if p['publie'] == 0)}")
        
    except sqlite3.Error as e:
        print(f"❌ Erreur SQL lors de la génération des playlists: {e}")
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")


if __name__ == '__main__':
    init_db()