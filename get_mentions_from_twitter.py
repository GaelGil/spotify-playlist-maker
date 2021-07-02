"""
This module gets the mentions on twitter and creates a spotify playlist then retweets it
back to the user who requested it.
"""
import os
import re
import tweepy
from createSpotifyPlaylist import create_spotify_playlist_from_search


auth = tweepy.OAuthHandler(os.environ['consumer_key'], os.environ['consumer_secret_key'])
auth.set_access_token(os.environ['access_token'], os.environ['access_token_secret'])
api = tweepy.API(auth)


def get_search_query(tweet: str) -> str:
    """
    Function to get search query from tweet
    This fuction will remove the @mention to get the search query. For example
    `@gg_bot a search query` will return 'a search query'

    Parameters
    ----------
    tweet: str
        A string containg a search query and twitter name

    Returns
    -------
    str
        The same input string without the twitter username
    """
    tweet = str(tweet)
    # removes the user (@user)
    tweet = re.sub(r'[@][a-zA-Z0-9_.+-]+', '', tweet)
    return tweet


def get_uri(playlist: str) -> str:
    """
    Function to get a spotify playlist uri (playlist id)
    This fuction will remove the 'spotify:playlist:' from 'spotify:playlist:uri` and return
    `uri` (id).

    Parameters
    ----------
    playlist: str
        A string containg a spotify playlist uri

    Returns
    -------
    str
        The same input string without `spotify:playlist:`
    """
    return re.sub(r'^spotify\Wplaylist\W', '', playlist)


def get_mentions():
    """get the @mentions from twitter"""
    mentions = api.mentions_timeline()
    for mention in mentions:
        tweet = mention.text
        user = mention.user.screen_name

    return tweet, user


def reply_playlist(user:str, query:str, uri:str) -> None:
    """reply to user if playlist has been created"""
    retweet = f'@{user} Your playlist {query} has been created. It can be found here https://open.spotify.com/playlist/{uri} Thank you!'
    api.update_status(retweet)
    return 0


def create_spotify_playlist() -> None:
    """function to get create a spotify playlist for a twiter user"""
    tweet, user = get_mentions()
    query = str(get_search_query(tweet))
    if user != '@gg_b':
        # create the playlist
        playlist = create_spotify_playlist_from_search(query, user)
        # turn the playlist id from spotify:playlist:playlistID to playlistID
        uri = get_uri(playlist)
        reply_playlist(user, query, uri)
    return 0
