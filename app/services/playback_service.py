from datetime import datetime
import sqlite3
import os

JOURS_SEMAINE = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


def _format_duree(secondes):
    if not secondes:
        return "0:00"
    secondes = int(secondes)
    return f"{secondes // 60}:{secondes % 60:02d}"


class PlaybackService:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "database.db",
            )
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_dashboard_playback(self, id_lecteur=None):
        lecteur = self._get_lecteur(id_lecteur)
        if not lecteur:
            return self._empty_state()

        now = datetime.now()
        heure_actuelle = now.strftime("%H:%M")
        jour_actuel = JOURS_SEMAINE[now.weekday()]

        planif = self._get_planification_active(
            lecteur["id_lecteur"], jour_actuel, heure_actuelle
        )

        if planif:
            id_playlist = planif["id_playlist"]
            playlist_nom = planif["nom_playlist"]
            heure_debut = self._fmt_heure(planif["heure_debut"])
            heure_fin = self._fmt_heure(planif["heure_fin"])
            source = "planification"
        else:
            fallback = self._get_fallback_playlist(lecteur["id_organisation"])
            if not fallback:
                return self._empty_state(lecteur)
            id_playlist = fallback["id_playlist"]
            playlist_nom = fallback["nom_playlist"]
            heure_debut = None
            heure_fin = None
            source = "playlist"

        piste = self._get_first_track(id_playlist)
        planif_semaine = self._get_planif_semaine(lecteur["id_lecteur"])
        duree_sec = piste["duree_fichier"] if piste else 0

        return {
            "lecteur_id": lecteur["id_lecteur"],
            "lecteur_nom": lecteur["nom_lecteur"],
            "lecteur_en_ligne": self._lecteur_en_ligne(lecteur),
            "playlist_id": id_playlist,
            "playlist_nom": playlist_nom,
            "piste_nom": piste["nom"] if piste else playlist_nom,
            "piste_duree_sec": duree_sec,
            "piste_duree": _format_duree(duree_sec),
            "heure_debut": heure_debut,
            "heure_fin": heure_fin,
            "source": source,
            "statut_label": "En lecture" if self._lecteur_en_ligne(lecteur) else "Programmée",
            "planif_semaine": planif_semaine,
        }

    def _empty_state(self, lecteur=None):
        return {
            "lecteur_id": lecteur["id_lecteur"] if lecteur else None,
            "lecteur_nom": lecteur["nom_lecteur"] if lecteur else None,
            "lecteur_en_ligne": False,
            "playlist_id": None,
            "playlist_nom": None,
            "piste_nom": "Aucune playlist active",
            "piste_duree_sec": 0,
            "piste_duree": "0:00",
            "heure_debut": None,
            "heure_fin": None,
            "source": None,
            "statut_label": "Inactif",
            "planif_semaine": {jour: [] for jour in JOURS_SEMAINE},
        }

    def _get_lecteur(self, id_lecteur=None):
        with self._connect() as conn:
            if id_lecteur:
                row = conn.execute(
                    "SELECT * FROM lecteur WHERE id_lecteur = ?", (id_lecteur,)
                ).fetchone()
            else:
                row = conn.execute(
                    "SELECT * FROM lecteur ORDER BY id_lecteur LIMIT 1"
                ).fetchone()
        return dict(row) if row else None

    def _get_planification_active(self, id_lecteur, jour, heure):
        query = """
            SELECT p.id_playlist, pl.nom_playlist, p.heure_debut, p.heure_fin, p.date_
            FROM planification p
            JOIN playlist pl ON p.id_playlist = pl.id_playlist
            JOIN lecteur l ON pl.id_organisation = l.id_organisation
            WHERE l.id_lecteur = ?
              AND (p.date_ = ? OR p.date_ IS NULL OR TRIM(p.date_) = '')
              AND TIME(p.heure_debut) <= TIME(?)
              AND TIME(p.heure_fin) > TIME(?)
            ORDER BY p.heure_debut
            LIMIT 1
        """
        with self._connect() as conn:
            row = conn.execute(query, (id_lecteur, jour, heure, heure)).fetchone()
            if row:
                return dict(row)

            row = conn.execute(
                """
                SELECT p.id_playlist, pl.nom_playlist, p.heure_debut, p.heure_fin, p.date_
                FROM planification p
                JOIN playlist pl ON p.id_playlist = pl.id_playlist
                JOIN lecteur l ON pl.id_organisation = l.id_organisation
                WHERE l.id_lecteur = ?
                  AND TIME(p.heure_debut) <= TIME(?)
                  AND TIME(p.heure_fin) > TIME(?)
                ORDER BY p.heure_debut
                LIMIT 1
                """,
                (id_lecteur, heure, heure),
            ).fetchone()
        return dict(row) if row else None

    def _get_fallback_playlist(self, id_organisation):
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT id_playlist, nom_playlist
                FROM playlist
                WHERE id_organisation = ? AND publie = 1
                ORDER BY date_derniere_maj DESC
                LIMIT 1
                """,
                (id_organisation,),
            ).fetchone()
        return dict(row) if row else None

    def _get_first_track(self, id_playlist):
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT f.nom, f.duree_fichier
                FROM Contenir c
                JOIN fichier f ON c.id_fichier = f.id_fichier
                WHERE c.id_playlist = ?
                ORDER BY f.nom
                LIMIT 1
                """,
                (id_playlist,),
            ).fetchone()
        return dict(row) if row else None

    def _get_planif_semaine(self, id_lecteur):
        semaine = {jour: [] for jour in JOURS_SEMAINE}
        query = """
            SELECT p.date_, p.heure_debut, p.heure_fin, pl.nom_playlist
            FROM planification p
            JOIN playlist pl ON p.id_playlist = pl.id_playlist
            JOIN lecteur l ON pl.id_organisation = l.id_organisation
            WHERE l.id_lecteur = ?
            ORDER BY p.heure_debut
        """
        with self._connect() as conn:
            rows = conn.execute(query, (id_lecteur,)).fetchall()

        for row in rows:
            jour = row["date_"] if row["date_"] in JOURS_SEMAINE else None
            if not jour:
                continue
            semaine[jour].append(
                {
                    "nom": row["nom_playlist"],
                    "debut": self._fmt_heure(row["heure_debut"]),
                    "fin": self._fmt_heure(row["heure_fin"]),
                }
            )
        return semaine

    def _lecteur_en_ligne(self, lecteur):
        try:
            from app.models.Lecteur import Lecteur

            l = Lecteur(
                lecteur["id_lecteur"],
                lecteur["nom_lecteur"],
                lecteur["adresseIP"],
                lecteur["etat_lecteur"],
                lecteur["emplacement"],
                lecteur["derniere_synchro"],
                lecteur["adresse_lecteur"],
                lecteur["alerte"],
                lecteur["id_organisation"],
            )
            return l.est_en_ligne()
        except Exception:
            return lecteur.get("etat_lecteur") == "en_ligne"

    @staticmethod
    def _fmt_heure(value):
        if not value:
            return None
        return str(value)[:5]
