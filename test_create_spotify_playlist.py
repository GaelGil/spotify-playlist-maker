import json
import re
import pytest
from functionsToTest import get_spotify_playlists, get_popular_songs, add_tracks_to_playlist
  
# Accessing supplied data
playlist_data_file = open('./data/playlist_data.json',)
playlist_data = json.load(playlist_data_file)
playlist_uris = ['spotify:playlist:1VcPVOXrGPsbDXgaeNyX6q', 'spotify:playlist:0vvXsWCC9xrXsKd4FyS8kM', 'spotify:playlist:35xI4hSJ8MdO1xkXwsd56a', 'spotify:playlist:3LFIBdP7eZXJKqf3guepZ1', 'spotify:playlist:5FmmxErJczcrEwIFGIviYo']

track_data_file = open('./data/tracks_data.json',)
track_data = json.load(track_data_file)


def validate_uri(uri: str, type: str) -> bool:
    valid_uri = False
    playlist_pattern = re.compile(r'^spotify\Wplaylist\W')
    track_pattern = re.compile(r'^spotify\Wtrack\W')

    if type == 'playlist':
        uri_clean = playlist_pattern.match(uri)
    else:
        uri_clean = re.sub(r'^spotify\Wtrack\W', '', uri)
    
    if uri_clean:
        valid_uri = True
    
    # print(uri_clean)

    return valid_uri



# assert that this function gets spotify playlists uri. Match a playlist uri using regex
def test_get_spotify_playlists():
    playlists = get_spotify_playlists(playlist_data)
    # print(playlists)
    assert validate_uri(playlists) == [True] * len(playlists)


# # assert that this function returns a list of tracks
# def test_get_popular_songs(list: track_data['tracks']):
#     tracks = get_popular_songs(track_data)
#     for i in tracks:
#         assert validate_uri(i, 'track') == True




# @pytest.mark.parametrize([playlist_data], playlist_uris)
# def test_get_spotify_playlists(input_data: list, output_data:list):
#     assert get_spotify_playlists(input_data) == output_data


# assert that this function returns a list of lists
# def test_add_tracks_to_playlist():
    # assert

