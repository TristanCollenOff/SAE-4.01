class Planification:
    def __init__(
        self,
        id_lecteur,
        id_playlist,
        jour_semaine,
        heure_debut,
        heure_fin,
        date_specifique=None,
        id_planification=None
    ):
        self.id_planification = id_planification
        self.id_lecteur = id_lecteur
        self.id_playlist = id_playlist
        self.jour_semaine = jour_semaine
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin
        self.date_specifique = date_specifique
