from ClientManager import ClineManager
from createSpotifyPlaylist import CreateSpotifyPlaylist
from SpotifySetUp import CONFIG



if __name__ == "__main__":
    print(' ')
    client_mngr = ClineManager()
    playlist = CreateSpotifyPlaylist(client=client_mngr)
    query = 'punk rock'
    # Search spotify for playlist using our query
    ids = playlist.search_spotify_playlist(query=CONFIG['QUERY'], limit=CONFIG['LIMIT'])
    # Get the tracks inside the playlist
    playlist_tracks = playlist.get_tracks_for_new_playlist(ids, popular=CONFIG['POPULAR'])
    # # Create a new playlist
    new_playlist_id = playlist.create_spotify_playlist(playlist_name=CONFIG['TITLE'])
    # # Add all the songs we have
    playlist.add_tracks_to_playlist(new_playlist_id, playlist_tracks)
    print(f'https://open.spotify.com/playlist/{new_playlist_id}')