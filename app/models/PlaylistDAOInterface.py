from abc import ABC, abstractmethod

class PlaylistDAOInterface(ABC):

    @abstractmethod
    def find_all(self):
        """
        Retourne toutes les playlists sous forme d'objets Playlist
        """
        pass

    @abstractmethod
    def find_one(self, id_playlist):
        """
        Retourne une playlist correspondant à l'id ou None
        """
        pass
