"""
This module is used to create spotify playlist from other spotify playlists. This is possible by using the
spotify api which allows us to search and retrive data. We use the spotify playlists to search for
playlist with a provided search query. All the playlists that are found will be searched for its
most popular songs. Those songs will then be added to a new spotify playlist which will be craeted
here. This module could be run on its own to create playlist for whoever wants it or could also be
run using the module `twitter.py` thats in this project. What this will do is check the users
twitter timeline and create playlists by checking @mentions and using those as search querys. This
will require both the spotify and twitter api.
"""
import os
import time
from tkinter.tix import Tree
import spotipy
from spotipy.oauth2 import SpotifyOAuth



class CreateSpotifyPlaylist:
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

    def __init__(self):
        """
        This function will call the class function `auth_spotify` and create a list for later use.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.spotify_client = self.auth_spotify()


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


    def search_spotify_playlist(self, query:str, limit=25) -> list:
        """
        Function to search spotify for playlists. This function will search spotify for playlists
        with the given query. The API will return some data that is accessed as a dict. For each
        playlist in the api data we will get their id. This will allow us to search each playlist
        by their id and get that playlist data. We then return all the ids that we have.

        Parameters
        ----------
        query : str
            The search query to find spotify playlist
        limit: int
            The number of results we want in our search (default is 25)
        Returns
        -------
        list
            A list of spotify playlist ids
        """
        # search for playlist that match the query on spotify
        playlists =  self.spotify_client.search(q=query, type='playlist', limit=limit)
        # get a list of playlist ids from the
        playlist_ids = [i['id'] for i in playlists['playlists']['items']]
        return playlist_ids


    def get_tracks_for_new_playlist(self, playlist_ids:list, popularity=75, popular=True) -> list:
        """
        This function will search spotify for playlists given some playlist ids. We search all the playlists
        in a for loop by getting their id and searching it in spotify. We will get some data in return. That
        data will contain data such as the tracks inside the playlist. Within the playlist data we also have
        track data for each track. For example track id, popularity, name. We then get the id and the popularity
        of each track in a playlist. Depending on the parameters `popularity` and `popular` we will add a
        popular or not popular song to a our dictionary containg the ids to the spotify tracks. If `popular`
        is set to true we add the tracks with a popularity value higher than `popularity`. If its false we add
        the tracks with the popularity value lower than `popularity`.

        Parameters
        ----------
        playlist_ids : list
            A list of playlists ids.

        popularity : int
            The cut off for the popularity of the songs. (set to 75 by default)

        popular : bool
            A bool if we want lower or higher than our popularity value (True by default)

        Returns
        -------
        list
            A list of track ids to add to our new playlist.
        """
        tracks = {}
        for i in range(len(playlist_ids)):
            playlist = self.spotify_client.playlist(playlist_id=playlist_ids[i])
            tracks_in_playlist = playlist
            # for every track in every playlist
            for track in tracks_in_playlist['tracks']['items']:
                if track['track']:
                    track_popularity = track['track']['popularity']
                    track_id = track['track']['id']
                    if track_id in tracks:
                        continue
                    if popular:
                        if track_popularity >= popularity:
                            tracks[track_id] = 0
                    else:
                        if track_popularity <= popularity:
                            tracks[track_id] = 0 
        return list(tracks.keys())


    def create_spotify_playlist(self, playlist_name: str) -> str:
        """
        Function to create spotify playlist. This function will create a new spotify playlist with
        the title provied by 'playlist_name' and `for_user`. Once we have created the new spotify
        playlist we return the playlist id for later use. This function has no returns

        Parameters
        ----------
        playlist_name : str
            The name of the new spotify playlist.

        Returns
        -------
        str
            A string containg the new spotify playlist id.
        """
        # create a new playlist
        new_playlist = self.spotify_client.user_playlist_create(
            user=os.environ['spotifyUserID'],
            name=playlist_name, public=True,
            collaborative=False,
            description='Created Using the Spotify API'
            )
        return new_playlist['id']


    def add_tracks_to_playlist(self, playlist_id: str, tracks:list) -> None:
        """
        Function to add songs to a spotify playlist
        This function will addd tracks to a playlist. This function has no returns

        Parameters
        ----------
        playlist_id : str
            The new spotify playlist id
        
        tracks: list
            The tracks we want to add to the playlist

        Returns
        -------
        None
        """
        # chceck if playlist is more than 100 tracks
        if len(tracks) >= 100:
            some_list = [] # list of lists of tracks
            current_list = [] # list to hold 100 tracks
            # add tracks to current_list
            for i in tracks:
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
                items=tracks,
            )


new_playlist = CreateSpotifyPlaylist()
query = 'punk rock'
# Search spotify for playlist using our query
ids = new_playlist.search_spotify_playlist(query=query, limit=50)
# Get the tracks inside the playlist
playlist_tracks = new_playlist.get_tracks_for_new_playlist(ids, popular=True)
# # Create a new playlist
new_playlist_id = new_playlist.create_spotify_playlist(playlist_name='bot playlist')
# # Add all the songs we have
new_playlist.add_tracks_to_playlist(new_playlist_id, playlist_tracks)
print(f'https://open.spotify.com/playlist/{new_playlist_id}')

# Example playlist created
# https://open.spotify.com/playlist/0ITi27Sdu3vg0loDX1YXgw