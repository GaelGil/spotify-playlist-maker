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


# get_spotify_playlists return a list of playlist uris from a dictrionary of data
def test_get_spotify_playlists():
    assert get_spotify_playlists(playlist_data) == playlist_uris


# get_popular_songs returns a list of popular tracks from a dictionary of data
# def test_get_popular_songs():
    # assert get_popular_songs(data of a playlist dictionary) == a list of songs


# add_tracks_to_playlist returns a list of of lists of tracks created from a list of tracks
def test_add_tracks_to_playlist():
    assert add_tracks_to_playlist(track_data) == track_data['tracks']
