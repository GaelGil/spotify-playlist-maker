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
import logging

logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CreatePlaylist:
    """
    A class used to communicate with the Spotify api.

    Attributes:
        spotify_client: list
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

    def __init__(self, client, config):
        self.spotify_client = client.get_client()
        self.config = config
        
    def search_spotify_playlist(self) -> list:
        """
        Function to search spotify for playlists. This function will search spotify for playlists
        with the given query. The API will return some data that is accessed as a dict. For each
        playlist in the api data we will get their id. This will allow us to search each playlist
        by their id and get that playlist data. We then return all the ids that we have.

        Args:
            None

        Returns:
            list
        """
        # search for playlist that match the query on spotify
        playlists =  self.spotify_client.search(q=self.config['QUERY'], type='playlist', limit=self.config['LIMIT'])
        # get a list of playlist ids from the
        playlist_ids = [i['id'] for i in playlists['playlists']['items']]
        return playlist_ids


    def get_tracks_for_new_playlist(self, playlist_ids:list) -> list:
        """
        This function will search spotify for playlists given some playlist ids. We search all the playlists
        in a for loop by getting their id and searching it in spotify. We will get some data in return. That
        data will contain data such as the tracks inside the playlist. Within the playlist data we also have
        track data for each track. For example track id, popularity, name. We then get the id and the popularity
        of each track in a playlist. Depending on the parameters `popularity` and `popular` we will add a
        popular or not popular song to a our dictionary containg the ids to the spotify tracks. If `popular`
        is set to true we add the tracks with a popularity value higher than `popularity`. If its false we add
        the tracks with the popularity value lower than `popularity`.

        Args:
        playlist_ids : list
            A list of playlists ids.

        Returns:
            list
        """
        tracks = {}
        for i in range(len(playlist_ids)): # for every playlist
            playlist = self.spotify_client.playlist(playlist_id=playlist_ids[i]) # get the playlist by id
            for track in playlist['tracks']['items']: # for every track in playlist (within its items)
                track_id = track['track']['id'] # select the id
                if not track['track'] or track_id in tracks: # if track doesnt exist or track is in tracks
                    continue 
                track_popularity = track['track']['popularity'] # select popularity
                if self.config['POPULAR']: # if we are going by popular songs
                    if track_popularity >= self.config['POPULARITY']: # if song is more popular than set poupularity
                        tracks[track_id] = 0 # add to trakcs
                else: # if not going by popular songs
                    if track_popularity <= self.config['POPULARITY']: # if track is less than set popularity 
                        tracks[track_id] = 0 # add to tracks
        return list(tracks.keys()) # return the keys of the tracks dictionary
        

    def create_spotify_playlist(self) -> str:
        """
        Function to create spotify playlist. This function will create a new spotify playlist with
        the title provied by 'playlist_name' and `for_user`. Once we have created the new spotify
        playlist we return the playlist id for later use. This function has no returns

        Args:
            playlist_name : str
                The name of the new spotify playlist.

        Returns:
            str
        """
        # create a new playlist
        new_playlist = self.spotify_client.user_playlist_create(
            user=os.environ['spotifyUserID'],
            name=self.config['TITLE'], public=True,
            collaborative=False,
            description='Created Using the Spotify API'
            )
        return new_playlist['id']


    def add_tracks_to_playlist(self, playlist_id: str, tracks:list) -> None:
        """
        Function to add songs to a spotify playlist
        This function will addd tracks to a playlist. This function has no returns

        Args:
            playlist_id : str
                The new spotify playlist id
            
            tracks: list
                The tracks we want to add to the playlist

        Returns:
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
