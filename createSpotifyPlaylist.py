"""
This module is used to create spotify playlist from other playlists. This is possible by using the
spotify api which allows us to search and retrive data. We use the spotify playlists to search for
playlist with a provided search query. All the playlists that are found will be search for its most
popular songs. Those songs will then be added to a new spotify playlist which will be craeted here.
This module could be run on its own to create playlist for whoever wants it or could also be run
using the module `twitter.py` thats in this project. What this will do is check the users twitter
timeline and create playlists by checking @mentions and using those as search querys. This will
require both the spotify and twitter api.
"""
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth



class CreateSpotifyPlaylist:
    """
    A class used to communicate with the Spotify api.

    Attributes
    ----------
    popular_tracks : list
        A list of popular tracks on spotify

    Methods
    -------
    get_spotify_playlists(self, query:str)
        Searches spotify for playlists

    get_popular_songs(self, spotify_playlist_id:str):
        Gets most popular songs from spotify playlist

    create_spotify_playlist(self, playlist_name:str, for_user:str)
        Creates a new spotify playlists using a name and a users name

    add_tracks_to_playlist(self, playlist_id:str)
        Adds song to a spotify playlists
    """

    def __init__(self):
        """
        Init function
        This function will call the class function `auth_spotify` and create a list for later use.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.spotify_client = self.auth_spotify()
        self.popular_tracks = []


    @classmethod
    def auth_spotify(cls):
        """
        Function to authenticate spotify
        This function will get the spotify client so we can use the api by authenticating. It will
        also set the scopes so we are able to use the tools that we need such as
        `playlist-modify-public` to create public spotify playlist

        Parameters
        ----------

        Returns
        -------
        str
            The spotify client
        """
        scope = "user-library-read,user-top-read,playlist-modify-public"
        spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        return spotify_client


    def get_spotify_playlists(self, query: str) -> None:
        """
        Function to search spotify for playlists
        This function will search spotify for playlists with the given query. For every playlist
        we will get its most popular songs to do that we call the function `get_popular_songs`.
        This function has no returns.

        Parameters
        ----------
        query : str
            The search query to find spotify playlist

        Returns
        -------
        None
        """
        # search for playlist that match the query on spotify
        playlists =  self.spotify_client.search(q=query, type='playlist', limit=5)

        # find the most popular songs in each playlist
        for playlist in playlists['playlists']['items']:
            playlist_uri = playlist['uri']
            self.get_popular_songs(playlist_uri)


    def get_popular_songs(self, spotify_playlist_id:str) -> None:
        """Function to get most popular songs from a spotify playlist

        This function will go through a spotify playlist and select the most popular tracks on the
        playlist. The popular tracks will get added to the class variable `popular_tracks`. This
        function has no returns

        Parameters
        ----------
        spotify_playlist_id : str
            The uri (id) of a spotify playlist

        Returns
        -------
        None

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
                # add popular tracks to list of popularity and check for duplicates
                if uri not in self.popular_tracks and popularity > most_popular:
                    self.popular_tracks.append(uri)


    def create_spotify_playlist(self, playlist_name:str, for_user:str) -> str:
        """Functio to create spotify playlist

        This function will create a new spotify playlist with the title provied by 'playlist_name'
        and `for_user`. Once we have created the new spotify playlist we return the playlist id for
        later use. This function has no returns

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
        # create the name of the playlist
        playlist_name = f'{playlist_name} for user {for_user}'

        # create a new playlist
        new_playlist = self.spotify_client.user_playlist_create(
            user=os.environ['spotifyUserID'],
            name=playlist_name, public=True,
            collaborative=False,
            description='a bot created this'
            )
        return new_playlist['id']


    def add_tracks_to_playlist(self, playlist_id: str) -> None:
        """Function to add songs to a spotify playlist

        This function will addd tracks to a playlist. This function has no returns

        Parameters
        ----------
        playlist_id : str
            The new spotify playlist id

        Returns
        -------
        None
        """
        # chceck if playlist is more than 100 tracks
        if len(self.popular_tracks) >= 100:
            some_list = [] # list of lists of tracks
            current_list = [] # list to hold 100 tracks
            # add tracks to current_list
            for i in self.popular_tracks:
                current_list.append(i)
                # once it reaches 100 add current_list to main_list and clear current_list
                if len(current_list) >= 100 or len(current_list)%1 == 1:
                    some_list.append(current_list)
                    current_list = []
            # add all tracks to playlist in batches
            for i in some_list:
                self.spotify_client.playlist_add_items(
                    playlist_id=playlist_id,
                    items=i,
                )
                print('Waiting 5 sec for next request')
                time.sleep(5)
        # add tracks all at once if not more than 100
        else:
            self.spotify_client.playlist_add_items(
                playlist_id=playlist_id,
                items=self.popular_tracks,
            )


def create_spotify_playlist_from_search(query:str, name:str) -> str:
    """Function to create a new spotify playlist for a user

    This function will create a new spotify playlist with the title provied by 'query'
    and `name`. The first step in creating a playlist is to search for spotify
    playlists in `get_spotify_playlists` with our search query. This function will
    fill a list of tracks to later use. The next step is to create a spotify playlist
    with using the parameters in `create_spotify_playlist` which will return an id.
    Once that is done we can finally add the tracks with the id in
    `add_tracks_to_playlist`.

    Parameters
    ----------
    query : str
        The search query to search on spotify
    name : str
        The name of the user who requested a playlist.

    Returns
    -------
    str
        A string containg the new spotify playlist id.

    """

    new_playlist = CreateSpotifyPlaylist()
    # search for playlists
    new_playlist.get_spotify_playlists(query)
    print(new_playlist.popular_tracks[0:20])
    # create a new playlist
    # new_spotify_playlist_id = new_playlist.create_spotify_playlist(query, name)
    # add songs to playlist
    # new_playlist.add_tracks_to_playlist(new_spotify_playlist_id)

    # return new_spotify_playlist_id


create_spotify_playlist_from_search('lofi', 'user')