import json
import re
import pytest
from functionsToTest import get_spotify_playlists, get_popular_songs, add_tracks_to_playlist
  
# Accessing supplied data
playlist_data_file = open('./data/playlist_data.json',)
playlist_data = json.load(playlist_data_file)

def validate_uri(str: uri, str: type) -> boolean:
    if type == 'playlist':
        return
    return 
    

# assert that this function gets spotify playlists uri. Match a playlist uri using regex
def test_get_spotify_playlists(dict: playlist_data):
    playlists = get_spotify_playlists(playlist_data)
    for i in playlists:
        assert validate_uri(i, 'playlist') == True


# assert that this function returns a list of tracks
def test_get_popular_songs(list: track_data):
    tracks = get_popular_songs(track_data)
    for i in tracks:
        assert validate_uri(i, 'track') == True

# assert that this function returns a list of lists
def test_add_tracks_to_playlist():
    # assert

