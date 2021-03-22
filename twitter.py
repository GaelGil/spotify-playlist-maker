import tweepy
import os
import re
from createSpotifyPlaylist import createFromYoutube, createFromSearchQuery

auth = tweepy.OAuthHandler(os.environ['consumer_key'], os.environ['consumer_secret_key'])
auth.set_access_token(os.environ['access_token'], os.environ['access_token_secret'])
api = tweepy.API(auth)



def getPlaylistId(youtubePlaylist:str):
    """
    """

    return 0 


def isLink(text:str):
    """
    This function will check if a string is a youtube link
    """
    httpsHeader = 'https'
    text = list(text)
    text = ''.join(text[0:5])

    if text == httpsHeader:
        return True
    else:
        pass


    return False



def getSearchQuery(tweet:str):
    """
    This fuction will get 
    """
    tweet = str(tweet)
    # removes the user (@user)
    tweet = re.sub(r'[@][a-zA-Z0-9_.+-]+', '', tweet)

    return tweet

def ignoreFirst(myString):
    ignoreThis = ['hello', 'world', 'from']
    sList = myString.split(' ')
    if ignoreThis == sList:
        return True
    return False


def getUri(playlist):
    """
    """
    if ''.join(list(playlist)[0:7]) == 'spotify':
        playlist= re.sub(r'^spotify\Wplaylist\W', '', playlist)

    return playlist



def twitterReader():
    """
    This function will check if there have been any tweets tweeted @me. If there has 
    it will check if it is a youtube playlist link. If its a youtube playlist link
    we will create a spotify playlist from it. If the link is not valid then it will
    tweet back with `not a valid playlist link`
    """

    atMentions = api.mentions_timeline()

    for mention in atMentions:
        tweet = mention.text
        user = mention.user.screen_name
        if isLink(tweet) == True:
            # get youtube playlist id
            youtubeID = getPlaylistId(tweet)
            # create a new playlist
            createFromYoutube(youtubeID)
        else:
            # get query from the tweet
            query = str(getSearchQuery(tweet))
            # print(type(query))
            # check to ignore first tweet
            firstTweeet = ignoreFirst(query)
            if firstTweeet == True:
                pass
            else:
                # create the playlist
                playlist = createFromSearchQuery(query, user)
                # turn the playlist id from spotify:playlist:playlistID to playlistID 
                uri = getUri(playlist)
                # tweet back to person with the playlist id
                api.update_status(f'@{user} Your playlist {query} has been created. It can be found here https://open.spotify.com/playlist/{uri} Thank you!')

            
            
    print('done')
    return 0

twitterReader()