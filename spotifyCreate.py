import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

scope = "user-library-read,user-top-read,playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# results = sp.current_user_saved_tracks()

# craete a playlist
# bot = sp.user_playlist_create(user=os.environ['spotifyUserID'], name='another', public=True, collaborative=False, description='a bot created this')


# this will get us the playlist id
# bot['id']


# list of songs
# track = ['spotify:track:2wBXASKIIkUPjHn0n8nfrY', 'spotify:track:05hlj6UAsd0iSAajxQTEhD']



# add songs into playlist
# sp.playlist_add_items(playlist_id='7sEqgazYNiMwiki1V9Lv4A', items=track, position=None)

print(sp.playlist(playlist_id='5AkF0NakkXHNYwFR6glS3j'))
