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
    playlists =  self.spotify_client.search(q=query, type='playlist', limit=20)
    # find the most popular songs in each playlist
    for playlist in playlists['playlists']['items']:
        playlist_uri = playlist['uri']
        self.get_popular_songs(playlist_uri)
    return

def get_popular_songs(self, spotify_playlist_id:str) -> None:
    """
    Function to get most popular songs from a spotify playlist
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
    return


def add_tracks_to_playlist(self, playlist_id: str) -> None:
    """
    Function to add songs to a spotify playlist
    This function will addd tracks to a playlist. This function has no returns

    Parameters
    ----------
    playlist_id : str
        The new spotify playlist id
    Returns
    -------
    None
    """
    # chceck if playlist is more than 100 songs
    if len(self.popular_tracks) >= 100:
        some_list = [] # list of lists of tracks
        current_list = [] # list to hold 100 tracks
        # create a list with tracks
        for i in self.popular_tracks:
            current_list.append(i)
            # once it reaches 100 add those list to another list and clear our initial list
            if len(current_list) >= 100 or len(current_list)%1 == 1:
                some_list.append(current_list)
                current_list = []
        # add all tracks to playlist in batches
        for i in some_list:
            self.spotify_client.playlist_add_items(
                playlist_id=playlist_id,
                items=i,
            )
            print('Waiting 15 sec for next request')
            time.sleep(15)
    # add tracks all at once if not more than 100
    else:
        self.spotify_client.playlist_add_items(
            playlist_id=playlist_id,
            items=self.popular_tracks,
        )
    return