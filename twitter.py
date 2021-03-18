import tweepy
import os
from createSpotifyPlaylist import createFromYoutube, createFromSearchQuery

auth = tweepy.OAuthHandler(os.environ['consumer_key'], os.environ['consumer_secret_key'])
auth.set_access_token(os.environ['access_token'], os.environ['access_token_secret'])
api = tweepy.API(auth)



def getPlaylistId(youtubePlaylist:str):
    # youtubeLink = 'https://www.youtube.com/watch?v='
    
    # youtube = list(youtubePlaylist)
    # youtube = youtube[0:32]
    # youtubeHead = ''.join(youtube)

    # if youtubeHead != youtubeLink:
    #     return ('Not Valid Link')
    # else:
    #     link = list(youtubePlaylist)[32:len(youtubePlaylist)-1]
    #     link = ''.join(link)
    #     print(link)


    # youTubePlaylistID = 0

    youTubePlaylistID = list(youtubePlaylist)
    youTubePlaylistID = youTubePlaylistID[-34:]

    return ''.join(youTubePlaylistID)


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



def getSearchQuery():
    """
    This fuction will get 
    """

def twitterReader():
    """
    This function will check if there have been any tweets tweeted @me. If there has 
    it will check if it is a youtube playlist link. If its a youtube playlist link
    we will create a spotify playlist from it. If the link is not valid then it will
    tweet back with `not a valid playlist link`
    """

    atMentions = api.mentions_timeline()

    for mention in atMentions:
        if isLink(mention) == True:
            youtubeID = getPlaylistId(mention)
            createFromYoutube(youtubeID)
        else:
            createFromSearchQuery(mention)
            
            

    pass