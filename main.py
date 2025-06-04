from ClientManager import ClineManager
from CreatePlaylist import CreatePlaylist
from SpotifySetUp import CONFIG


if __name__ == "__main__":
    client_manger = ClineManager(scope=CONFIG['SCOPE'])
    playlist = CreatePlaylist(client=client_manger, config=CONFIG)
    # Search spotify for playlist using our query
    ids = playlist.search_spotify_playlist()
    # Get the tracks inside the playlist
    playlist_tracks = playlist.get_tracks_for_new_playlist(ids)
    # # Create a new playlist
    new_playlist_id = playlist.create_spotify_playlist()
    # # Add all the songs we have
    playlist.add_tracks_to_playlist(new_playlist_id, playlist_tracks)
    print(f'https://open.spotify.com/playlist/{new_playlist_id}')