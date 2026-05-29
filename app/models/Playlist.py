class Playlist:
    def __init__(
        self,
        id_playlist=None,
        nom_playlist=None,
        date_creation=None,
        date_derniere_maj=None,
        date_fin_playlist=None,
        type_playlist="principale",
        nb_pistes=0,
        duree_totale=0,
        statut="incomplet",
        problemes=None,
        publie=True
    ):
        self.id_playlist = id_playlist
        self.nom_playlist = nom_playlist
        self.date_creation = date_creation
        self.date_derniere_maj = date_derniere_maj
        self.date_fin_playlist = date_fin_playlist
        self.type = type_playlist
        self.nb_pistes = nb_pistes
        self.duree_totale = duree_totale
        self.statut = statut
        self.problemes = problemes or []
        self.publie = publie
