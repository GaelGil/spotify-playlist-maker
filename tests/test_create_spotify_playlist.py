import json
import re
import pytest
from functionsToTest import get_spotify_playlists, get_popular_songs, add_tracks_to_playlist


# Accessing supplied data
playlist_data_file = open('../data/playlist_data.json',)
playlist_data = json.load(playlist_data_file)
playlist_uris = ['spotify:playlist:1VcPVOXrGPsbDXgaeNyX6q', 'spotify:playlist:0vvXsWCC9xrXsKd4FyS8kM', 'spotify:playlist:35xI4hSJ8MdO1xkXwsd56a', 'spotify:playlist:3LFIBdP7eZXJKqf3guepZ1', 'spotify:playlist:5FmmxErJczcrEwIFGIviYo']

track_data_file = open('../data/tracks_data.json',)
track_data = json.load(track_data_file)


def test_get_spotify_playlists():
    """
    This function tests get_spotify_playlists. It assserts that the function 
    will return a list of spotify playlist ids (also known as uris). The
    function will look through some json/dict and retrive the uris and return
    them as a list. This test is given some data that has been tested on the 
    real functions and a real output to validate it. 
    """
    assert get_spotify_playlists(playlist_data) == playlist_uris


def test_add_tracks_to_playlist():
    """
    This function tests add_tracks_to_playlist
    """
    assert add_tracks_to_playlist(track_data) == track_data['tracks']
