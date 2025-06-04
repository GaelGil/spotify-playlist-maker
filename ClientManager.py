import spotipy
from spotipy.oauth2 import SpotifyOAuth

class ClineManager:
    """
    A class used to communicate with the Spotify api.

    Attributes
    ----------
    spotify_client : list
        The spotify client

    Methods
    -------
    search_spotify_playlist(self, query:str, limit:int)
        Searches spotify for playlists.

    get_tracks_for_new_playlist(self, playlist_ids:str, popularity:int, popular:bool):
        Get a list of tracks for the new playlist.

    get_popular_tracks(self, playlist_name:str, for_user:str)
        Gets popular or unpopular songs and adds them to a list

    create_spotify_playlist(self, playlist_name:str)
        Creates a spotify playlists.
    
    add_tracks_to_playlist(self, playlist_id:str)
        Add songs in a list to a spotify playlists.
    """

    def __init__(self, scope: str):
        """
        This function will call the class function `auth_spotify` and create a list for later use.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self._spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    def get_client(self):
        """
        """
        return self._spotify_client
    