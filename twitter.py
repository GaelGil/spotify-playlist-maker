"""
This file gets the mentions on twitter and creates a spotify playlist then tweets it
"""
import os
import re
import tweepy
from createSpotifyPlaylist import create_spotify_playlist_from_search

auth = tweepy.OAuthHandler(os.environ['consumer_key'], os.environ['consumer_secret_key'])
auth.set_access_token(os.environ['access_token'], os.environ['access_token_secret'])
api = tweepy.API(auth)


def get_search_query(tweet:str):
    """
    This fuction will remove the @mention to get the search query. For example
    `@gg_bot a search query` will return 'a search query'
    """
    tweet = str(tweet)
    # removes the user (@user)
    tweet = re.sub(r'[@][a-zA-Z0-9_.+-]+', '', tweet)
    return tweet



def get_uri(playlist):
    """
    This will match the spotify uri code
    """
    if ''.join(list(playlist)[0:7]) == 'spotify':
        playlist= re.sub(r'^spotify\Wplaylist\W', '', playlist)

    return playlist



def twitter_reader():
    """
    This function will check if there have been any tweets tweeted @me. If there has
    it will check if it is a youtube playlist link. If its a youtube playlist link
    we will create a spotify playlist from it. If the link is not valid then it will
    tweet back with `not a valid playlist link`
    """
    at_mentions = api.mentions_timeline()
    
    for mention in at_mentions:
        tweet = mention.text 
        user = mention.user.screen_name
        # get query from the tweet
        query = str(get_search_query(tweet))
        if str(user) != '@gg_bot':
            # create the playlist
            playlist = create_spotify_playlist_from_search(query, user)
            # turn the playlist id from spotify:playlist:playlistID to playlistID
            uri = get_uri(playlist)
            # tweet back to person with the playlist id
            retweet = f'@{user} Your playlist {query} has been created. It can be found here https://open.spotify.com/playlist/{uri} Thank you!'
            api.update_status(retweet)
    return 0

twitter_reader()
