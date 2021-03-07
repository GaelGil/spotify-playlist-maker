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
import requests




class CreateSpotifyPlaylist:
    def __init__(self):
        self.youtubeClient = self.getYoutubeClient()
        self.allTheTrackInfo = {}
        self.spotifyClient = self.authSpotify()
        self.uris = []
        self.popularTracks = []

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


    def cleanArtistNameAndTitle(self, title, artist):
        """
        This function will find the word vevo in every string and return the string
        with out the word vevo or music video.  
        """
        wordsToRemove = ['VEVO', '(Official Music Video)', '(Official)', '(Official Video)', '-']
        # print(title)

        title = title.lower()
        artist = artist.lower()
        # removes anything inside parentheses (ie. (Official Music Video)', '(Official)', '(Official Video))
        title = re.sub("[\(\[].*?[\)\]]", "", title)

        # removes vevo from name
        vevo = artist[-4:] # select last four characters where vevo would be

        # check if the last 4 characters are vevo
        if vevo == "vevo":
            # if they are ignore last 4 characters which are vevo
            artist = artist[:-4]
        else:
            pass


        # remove artist if its in the title
        # title = title.replace(artist, ' ')
        # remove dashes from title
        title = title.replace('-', ' ')
        # remove commas
        title = title.replace(',', '')
        # remove periods
        title = title.replace('.', '')
        # remove word from title
        title = title.replace('video oficial', ' ')
        # remove any white space from the title
        cleanTitle = re.sub(' +', ' ', title)
        # # remove music from artist 
        # artist =  artist.replace('music', '')
        # remove any white spcae from artist name
        artist = re.sub(' +', ' ', artist)

        
        


        # title as a list of strings
        titleWords = cleanTitle.split()

        # artist name as chars
        artistChars = list(artist)

        # print(artist)
        word = artist.split()

        # only change name if its in this format `artistname` not `artist name`
        if len(word) ==1:
            if len(titleWords) > 1:
                # first two words of title where artist can be found
                suspectedArtist = titleWords[0]+ titleWords[1]
                if artist == suspectedArtist:
                    # change artist from `artistname` to `artist name`
                    artist = titleWords[0] + " " + titleWords[1]
                    # remove artist from title
                    cleanTitle = ' '.join(titleWords[2:])
                else:
                    pass
            else:
                pass
        else:
            pass

        


        return cleanTitle, artist


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
                    self.uris.append(uri)
                else:
                    pass
            
        print('done getting info')
        return 0

    def getMostPopularSongs(spotifyPlaylistID:str):
        """
        This function will go through a playlist and find its most popular songs
        """
        # get spotify playlist
        tracksInPlaylist = sp.playlist(playlist_id=spotifyPlaylistID)
        
        # select the first tracks popularity number
        mostPopular = tracksInPlaylist['tracks']['items'][0]['track']['popularity']

        # search for most popular tracks
        for track in tracksInPlaylist['tracks']['items']:
            if track['track'] == None:
                pass
            else:
                popularity = track['track']['popularity'] # get popularity number
                uri = track['track']['uri'] # get uri for the track
                # add popular tracks to list of popularity
                if popularity > mostPopular: 
                    mostPopular = popularity
                    self.popularTracks.append({uri:popularity})

        return 0

    def getSpotifyPlaylists(self, query:str):
        """
        This function will get spotify playlists from a search query
        """
        # search for playlist that match the query on spotify
        playlists =  sp.search(q=query, type='playlist', limit=50)
        # find the most popular songs from that playlist 
        for playlist in playlists['playlists']['items']:
            playlistUri = playlist['uri']
            self.getMostPopularSongs(playlistUri)
        
        return 0

    def getSpotifyURICode(self, trackName, artistName):
        """
        This function will search for the trackname and artist name using the spotify api. 
        Once we have gotten the track info we will get the uri and return it
        """

        q = f'{trackName} {artistName}'
        trackInfo = self.spotifyClient.search(q=q, type='track')


        uri = ''
        if len(trackInfo['tracks']['items']) != 0:
            uri = trackInfo['tracks']['items'][0]['uri']
        else: 
            # print(trackName)
            # print(artistName)
            # print()
            pass


        return uri


    def createSpPlaylist(self):
        """
        This function will create a playlist in spotify from the songs in
        the youtube playlist
        """

        results = self.spotifyClient.current_user_saved_tracks()

        newPlaylist = self.spotifyClient.user_playlist_create(user=os.environ['spotifyUserID'], name='another', public=True, collaborative=False, description='a bot created this')
        
        return newPlaylist['id']


    def addYTTracksToSpotify(self):
        """
        This function will add all the tracks that were found in the youtube
        playlist to the spotify playlist
        """
        
        self.spotifyClient.playlist_add_items(
            playlist_id='spotify:playlist:5AkF0NakkXHNYwFR6glS3j', 
            items=self.uris[:len(self.uris)//2], 
            position=None
            )


        return 0


    def addPlaylistTracksToNew():
        """
        """

        self.spotifyClient.playlist_add_items(
            playlist_id='spotify:playlist:5AkF0NakkXHNYwFR6glS3j', 
            items=self.popularTracks, 
            position=None
            )


        return 0




def isLink(text:str):
    """
    This function will check if a string is a youtube link
    """
    request = requests.head(text)

    # if requests.exceptions.MissingSchema:
    #     return 404

    return request.status_code

def createFromYoutube():
    """
    This function will create
    """
    newPlaylist = CreateSpotifyPlaylist()
    ytPlaylist = 'PL4o29bINVT4EG_y-k5jGoOu3-Am8Nvi10'
    # get youtube songs
    newPlaylist.getTracksFromPlaylist(ytPlaylist)
    # create a new playlist to add them to
    newPlaylist.createSpPlaylist()
    # add tracks to new playlist
    newPlaylist.addYTTracksToSpotify()

    return 0


def createFromSearchQuery():
    newPlaylist = createSpPlaylist()
    # search for playlists
    newPlaylist.getSpotifyPlaylists()
    # create a new playlist 
    newPlaylist.createSpPlaylist()
    # add songs to playlist
    newPlaylist.addPlaylistTracksToNew()




def twitterReader():
    """
    This function will check if there have been any tweets tweeted @me. If there has 
    it will check if it is a youtube playlist link. If its a youtube playlist link
    we will create a spotify playlist from it. If the link is not valid then it will
    tweet back with `not a valid playlist link`
    """
    tweetOne = 'girls and gays'
    tweetTwo = 'https://www.youtube.com/watch?v=SlPhMPnQ58k&list=PL4o29bINVT4EG_y-k5jGoOu3-Am8Nvi10'
    if isLink(tweetOne) == 200:
        print('this should not print')
    else:
        print('it worked')


    if isLink(tweetTwo) == 200:
        print('this should print')
    else:
        print('didnt work')
    pass

twitterReader()