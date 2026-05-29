import sqlite3
from app import app
from app.models.PlaylistDAOInterface import PlaylistDAOInterface
from app.models.Playlist import Playlist

class PlaylistDAO(PlaylistDAOInterface):

    def _get_connection(self):
        conn = sqlite3.connect(app.root_path + "/database.db")
        conn.row_factory = sqlite3.Row
        return conn

    def find_all(self):
        conn = self._get_connection()
        cursor = conn.execute("SELECT * FROM Playlist ORDER BY date_derniere_maj DESC")

        playlists = []
        for row in cursor.fetchall():
            nb_pistes, duree_totale, problemes = self._get_playlist_stats(conn, row['id_playlist'])
            statut = "valide" if nb_pistes >= 5 else "incomplet"

            playlists.append(
                Playlist(
                    id_playlist=row['id_playlist'],
                    nom_playlist=row['nom_playlist'],
                    date_creation=row['date_creation'],
                    date_derniere_maj=row['date_derniere_maj'],
                    date_fin_playlist=row['date_fin_playlist'] if 'date_fin_playlist' in row.keys() else None,
                    type_playlist="principale",
                    nb_pistes=nb_pistes,
                    duree_totale=duree_totale,
                    statut=statut,
                    problemes=problemes,
                    publie=row['publie']
                )
            )

        conn.close()
        return playlists

    def find_one(self, id_playlist):
        conn = self._get_connection()
        cursor = conn.execute("SELECT * FROM Playlist WHERE id_playlist = ?", (id_playlist,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        nb_pistes, duree_totale, problemes = self._get_playlist_stats(conn, row['id_playlist'])
        statut = "valide" if nb_pistes >= 5 else "incomplet"

        conn.close()
        return Playlist(
            id_playlist=row['id_playlist'],
            nom_playlist=row['nom_playlist'],
            date_creation=row['date_creation'],
            date_derniere_maj=row['date_derniere_maj'],
            date_fin_playlist=row['date_fin_playlist'] if 'date_fin_playlist' in row.keys() else None,
            type_playlist="principale",
            nb_pistes=nb_pistes,
            duree_totale=duree_totale,
            statut=statut,
            problemes=problemes,
            publie=row['publie']
        )

    def _get_playlist_stats(self, conn, id_playlist):
        """
        Compte le nombre de pistes, calcule la durée totale et détecte les problèmes
        """
        cursor = conn.execute(
            "SELECT f.*, e.id_playlist FROM Est_composé_d_une e "
            "JOIN Fichier f ON e.id_fichier = f.id_fichier "
            "WHERE e.id_playlist = ?",
            (id_playlist,)
        )
        rows = cursor.fetchall()

        nb_pistes = len(rows)
        duree_totale = 0
        problemes = []

        for row in rows:
            # Utiliser l'accès direct par clé au lieu de .get()
            duree = row['duree_fichier'] if row['duree_fichier'] else 180
            duree_totale += duree

            # Vérifier si la colonne existe et si elle est vide
            emplacement = row['emplacement'] if 'emplacement' in row.keys() else None
            if not emplacement:
                problemes.append(f"Fichier manquant: {row['nom']}")

        if nb_pistes < 5:
            problemes.append("Moins de 5 pistes")

        return nb_pistes, duree_totale, problemes