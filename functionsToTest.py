def get_spotify_playlists(playlists) -> list:
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
    # playlists =  self.spotify_client.search(q=query, type='playlist', limit=20)
    # find the most popular songs in each playlist
    playlist_uris = []
    for playlist in playlists['playlists']['items']:
        playlist_uri = playlist['uri']
        # get_popular_songs(playlist_uri)
        playlist_uris.append(playlist_uri)

    return playlist_uris

def get_popular_songs(spotify_playlist_id:str) -> None:
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
    # playlist_tracks = self.spotify_client.playlist(playlist_id=spotify_playlist_id)
    # select the first tracks popularity number
    popular_tracks = []
    most_popular = playlist_tracks['tracks']['items'][0]['track']['popularity']
    # search for most popular tracks
    for track in playlist_tracks['tracks']['items']:
        if track['track'] is None:
            pass
        else:
            popularity = track['track']['popularity'] # get popularity number
            uri = track['track']['uri'] # get uri for the track
            # add popular tracks to list of popularity and check for duplicates
            if uri not in popular_tracks and popularity > most_popular:
                popular_tracks.append(uri)
    return popular_tracks


def add_tracks_to_playlist(popular_tracks: list) -> None:
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
    tracks_list = []
    # chceck if playlist is more than 100 songs
    if len(popular_tracks) >= 100:
        some_list = [] # list of lists of tracks
        current_list = [] # list to hold 100 tracks
        # create a list with tracks
        for i in popular_tracks:
            current_list.append(i)
            # once it reaches 100 add those list to another list and clear our initial list
            if len(current_list) >= 100 or len(current_list)%1 == 1:
                some_list.append(current_list)
                current_list = []

            print('Waiting 15 sec for next request')
            time.sleep(5)
    else:
        tracks_list = popular_tracks['tracks']

    return tracks_list