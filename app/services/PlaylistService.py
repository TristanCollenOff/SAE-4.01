from app.models.PlaylistDAO import PlaylistDAO

class PlaylistService:

    def __init__(self):
        self.dao = PlaylistDAO()

    def get_playlists_disponibles(self):
        """
        Retourne uniquement les playlists publiées et valides
        """
        playlists = self.dao.find_all()
        return [p for p in playlists if p.publie and p.statut == "valide"]

    def get_playlist(self, id_playlist):
        """
        Retourne une playlist par son id
        """
        return self.dao.find_one(id_playlist)

