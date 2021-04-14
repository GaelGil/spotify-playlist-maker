"""
- use correct dosctrings: https://numpydoc.readthedocs.io/en/latest/format.html
- use comments appropriately
"""
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class CreateSpotifyPlaylist:
    """
    TODO: add class-level docstring
    """
    def __init__(self):
        """
        TODO: add an init-level docstring
        """
        self.spotify_client = self.auth_spotify()
        self.popular_tracks_list = []


    @classmethod
    def auth_spotify(cls):
        """
        This function will get the spotify client so we can use the api by authenticating. It will
        also set the scopes so we are able to use the tools that we need such as
        `playlist-modify-public` to create public spotify playlist
        """
        scope = "user-library-read,user-top-read,playlist-modify-public"
        spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        return spotify_client



    def get_spotify_playlists(self, query:str):
        """
        This function will get spotify playlists from a search query
        """
        # search for playlist that match the query on spotify
        playlists =  self.spotify_client.search(q=query, type='playlist', limit=20)

        # find the most popular songs from that playlist
        for playlist in playlists['playlists']['items']:
            playlist_uri = playlist['uri']
            self.get_popular_songs(playlist_uri)
        return 0



    def get_popular_songs(self, spotify_playlist_id:str):
        """
        This function takes in a string (spotify playlist uri) as its argument. It then gets that
        playlists info to then get the most popular songs.
        """
        # get spotify playlist
        playlist_tracks = self.spotify_client.playlist(playlist_id=spotify_playlist_id)
        # select the first tracks popularity number
        most_popular = playlist_tracks['tracks']['items'][0]['track']['popularity']

        # search for most popular tracks
        for track in playlist_tracks['tracks']['items']:
            if track['track'] is None:
                pass
            else:
                popularity = track['track']['popularity'] # get popularity number
                uri = track['track']['uri'] # get uri for the track
                # add popular tracks to list of popularity
                if uri not in self.popular_tracks_list and popularity > most_popular:
                    self.popular_tracks_list.append(uri)
        return 0



    def create_spotify_playlist(self, playlist_name:str, for_user:str):
        """Functio to create spotify playlist

        This function will create a new spotify playlist with the title provied by 'playlist_name'
        and `for_user`. Once we have created the new spotify playlist we return the playlist id for
        later use.

        Parameters
        ----------
        playlist_name : str
            The name of the new spotify playlist.
        for_user : str
            The name of the user who requested a playlist.

        Returns
        -------
        str
            A string containg the new spotify playlist id.

        """

        playlist_name = f'{playlist_name} for user {for_user}'

        new_playlist = self.spotify_client.user_playlist_create(
            user=os.environ['spotifyUserID'],
            name=playlist_name, public=True,
            collaborative=False,
            description='a bot created this'
            )
        return new_playlist['id']



    def add_tracks_to_playlist(self, playlist_id:str):
        """
        This function will addd tracks to a playlist
        """
        list_one = self.popular_tracks_list[:len(self.popular_tracks_list)//2]
        list_two = self.popular_tracks_list[len(self.popular_tracks_list)//2:]

        self.spotify_client.playlist_add_items(
            playlist_id=playlist_id,
            items=list_one,
            position=None
        )
        self.spotify_client.playlist_add_items(
            playlist_id=playlist_id,
            items=list_two,
            position=None
        )

        return 0



def create_spotify_playlist_from_search(query:str, name:str):
    """
    This function will create a spotify playlist given a search query
    """
    new_playlist = CreateSpotifyPlaylist()
    # search for playlists
    new_playlist.get_spotify_playlists(query)
    # create a new playlist
    new_spotify_playlist_id = new_playlist.create_spotify_playlist(query, name)
    # add songs to playlist
    new_playlist.add_tracks_to_playlist(new_spotify_playlist_id)

    return new_spotify_playlist_id
