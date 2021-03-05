import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
import pickle
import youtube_dl
import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re



class CreateSpotifyPlaylist:
    def __init__(self):
        self.youtubeClient = self.getYoutubeClient()
        self.allTheTrackInfo = {}
        self.spotifyClient = self.authSpotify()

    def getYoutubeClient(self):
        """
        This function will take care of the authorization and credentials.
        Once we have been authenticated it will return the youtube client 
        so we can use it in our other functions.

        """
        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
        credentials = None
        # token.pickle stores the user's credentials from previously successful logins
        if os.path.exists('token.pickle'):
            print('Loading Credentials From File...')
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)


        # If there are no valid credentials available, then either refresh the token or log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                print('Refreshing Access Token...')
                credentials.refresh(Request())
            else:
                print('Fetching New Tokens...')
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json',
                    scopes=[
                        'https://www.googleapis.com/auth/youtube.readonly'
                    ]
                )

                flow.run_local_server(port=8080, prompt='consent',
                                    authorization_prompt_message='')
                credentials = flow.credentials

                # Save the credentials for the next run
                with open('token.pickle', 'wb') as f:
                    print('Saving Credentials for Future Use...')
                    pickle.dump(credentials, f)
        
        
        youtubeClient = googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)

        return youtubeClient


    def authSpotify(self):
        """
        """
        scope = "user-library-read,user-top-read,playlist-modify-public"

        spotifyClient = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        return spotifyClient


    def getYouTubePlayList(self, youTubePlaylistLink):
        """
        This function will get a playlist link of a youtube channel and
        check if its a valid playlist. If it is it will return the playlist
        id
        """
        pass


    def cleanArtistNameAndTitle(self, title, artist):
        """
        This function will find the word vevo in every string and return the string
        with out the word vevo or music video.  
        """
        wordsToRemove = ['VEVO', '(Official Music Video)', '(Official)', '(Official Video)', '-']
        # print(title)

        # removes anything inside parentheses (ie. (Official Music Video)', '(Official)', '(Official Video))
        title = re.sub("[\(\[].*?[\)\]]", "", title)

        # removes vevo from name
        vevo = artist[-4:] # select last four characters where vevo would be

        # check if the last 4 characters are vevo
        if vevo == "VEVO":
            # if they are ignore last 4 characters which are vevo
            artist = artist[:-4]
        else:
            pass
        
        title = title.replace(artist, ' ')
        title = title.replace('-', ' ')
        t = re.sub(' +', ' ', title)
        # print(t)
        # print()


        return t, artist


    def getTracksFromPlaylist(self, youTubePlaylistID):
        """
        This function will get all the tracks from the playlist that has 
        been submited. It will get all the nesecsary data that we will 
        need to create a playlist later
        """
        # youtube playlist id
        # youTubePlaylistID = "PL4o29bINVT4EG_y-k5jGoOu3-Am8Nvi10"

        # request youtube playlist data
        request = self.youtubeClient.playlistItems().list(
            part = "snippet",
            playlistId = youTubePlaylistID,
            maxResults = 50
        )
        response = request.execute()

        # a list to hold playlist data
        playlist_items = []



        # add items to playlist_items
        while request is not None:
            response = request.execute()
            playlist_items += response["items"]
            request = self.youtubeClient.playlistItems().list_next(request, response)

        
        for item in playlist_items:
            trackName, artistName = self.cleanArtistNameAndTitle(item['snippet']['title'], item['snippet']['videoOwnerChannelTitle'])   

            # get track uri
            uri = self.getSpotifyURICode(trackName, artistName)
            if uri == '':
                pass
            else:
                # add all the track information for later use
                if trackName is not None and artistName is not None:
                    self.allTheTrackInfo[trackName]= {
                        'trackName': trackName,
                        'artistName': artistName,
                        'uri': uri
                        
                    }
                else:
                    pass
            
        # print(self.allTheTrackInfo)
        print(len(self.allTheTrackInfo))
    
        return 0


    def getSpotifyURICode(self, trackName, artistName):
        """
        This function will search for the trackname and artist name using the spotify api. 
        Once we have gotten the track info we will get the uri and return it
        """

        trackInfo = self.spotifyClient.search(q='artist:' + artistName + ' track:' + trackName, type='track')


        uri = ''
        if len(trackInfo['tracks']['items']) != 0:
            uri = trackInfo['tracks']['items'][0]['uri']
        else: 
            pass


        return uri


    def createSpPlaylist():
        """
        This function will create a playlist in spotify from the songs in
        the youtube playlist
        """

        # scope = "user-library-read,user-top-read,playlist-modify-public"

        # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        results = self.spotifyClient.current_user_saved_tracks()

        newPlaylist = self.spotifyClient.user_playlist_create(user=os.environ['spotifyUserID'], name='another', public=True, collaborative=False, description='a bot created this')
        
        return newPlaylist['id']


    def addYTTracksToSpotify():
        """
        This function will add all the tracks that were found in the youtube
        playlist to the spotify playlist
        """

        spotifyPlaylistID = self.createSpPlaylist()
        trackUris = []
        for track in self.allTheTrackInfo:
            trackUris.append(track['uri'])

        self.spotifyClient.playlist_add_items(playlist_id=spotifyPlaylistID, items=trackUris, position=None)


        return 0




def controller():
    newPlaylist = CreateSpotifyPlaylist()
    artist= 'Dua Lipa'
    track= 'Levitating'
    ytPlaylist = 'PL4o29bINVT4EG_y-k5jGoOu3-Am8Nvi10'
    newPlaylist.getTracksFromPlaylist(ytPlaylist)
    # print(newPlaylist.getSpotifyURICode(track, artist))
    # addYTTracksToSpotify()
    return 0


controller()


# def twitterReader():
#     """
#     This function will check if there have been any tweets tweeted @me. If there has 
#     it will check if it is a youtube playlist link. If its a youtube playlist link
#     we will create a spotify playlist from it. If the link is not valid then it will
#     tweet back with `not a valid playlist link`
#     """
#     pass