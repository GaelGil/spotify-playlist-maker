import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

scope = "user-library-read,user-top-read,playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


# craete a playlist
# bot = sp.user_playlist_create(user=os.environ['spotifyUserID'], name='another', public=True, collaborative=False, description='a bot created this')

# this will get us the playlist id
# bot['id']


# list of track uris
# track = ['spotify:track:2wBXASKIIkUPjHn0n8nfrY', 'spotify:track:05hlj6UAsd0iSAajxQTEhD']


# add songs into playlist
# sp.playlist_add_items(playlist_id='7sEqgazYNiMwiki1V9Lv4A', items=track, position=None)


# print(sp.playlist(playlist_id='7sEqgazYNiMwiki1V9Lv4A'))

playlistName = 'girls and gays'

pl =  sp.search(q=playlistName, type='playlist', limit=50)
# print(pl)
# get the 0th playlist uri
# print(pl['playlists']['items'][0]['uri'])


# print(sp.playlist(playlist_id='7sEqgazYNiMwiki1V9Lv4A'))

tracksInPlaylist = sp.playlist(playlist_id='spotify:playlist:68PjCnmfHOdWHNt2szkwiD')
# 
# print(tracksInPlaylist['tracks']['items'][0]['track']['popularity'])
# print(tracksInPlaylist['tracks']['items'][0]['track']['uri'])


def getMostPopularSongs(spotifyPlaylistID:str):
    """
    This function will go through a playlist and find its most popular songs
    """
    tracksInPlaylist = sp.playlist(playlist_id=spotifyPlaylistID)
    
    listOfMostPopular = []
    mostPopular = tracksInPlaylist['tracks']['items'][0]['track']['popularity']

    for track in tracksInPlaylist['tracks']['items']:
        if track['track'] == None:
            pass
        else:
            popularity = track['track']['popularity']
            uri = track['track']['uri']
            if popularity > mostPopular:
                mostPopular = popularity
                printNames(uri)
                listOfMostPopular.append({uri:popularity})

    return 0




def printNames(uri:str):
    # print(sp.track(uri).keys())
    name = sp.track(uri)
    print(name['name'])



def getPlaylists(query:str):
    """
    This function will get 10 playlist from a search query
    """
    playlists =  sp.search(q=query, type='playlist', limit=50)
    for playlist in playlists['playlists']['items']:
        # print(playlist['uri'])
        playlistUri = playlist['uri']
        getMostPopularSongs(playlistUri)



    


# getMostPopularSongs('spotify:playlist:68PjCnmfHOdWHNt2szkwiD')

# print()
getPlaylists('girls and gays')


