# API Practice

check out this project [here](https://twitter.com/_gg_bot) - some description of what you should be seeing

## Setup: General
Some intial steps that can be taken to set up the project are to install the `requirements.txt`. Steps
that will require more set up will be to get developer accounts. This whole project requires to have
a twitter developer account and spotify developer account. You can choose to only have a spotify 
developer account and run this for yourself without the `twitter.py`. Lastly all the access tokens given
by the developer accounts you will need to add to your `.bash_profile` or `.zshrc` file. Make sure to
name them as they are in the `twitter.py` and `createSpotifyPlaylist.py` files for easy use. Also don't 
forget to source the files.

## Setup: Twitter
To get your twitter developer account you can go [here](https://developer.twitter.com/en/apply-for-access). 
Once you apply you might have to wait to get access. Once you have access you will need to create an 
app on your dashboard. Now that you have your app you can save your access tokens that you were given
so you can use those later. One thing to keep in mind is to  enable `read and write` permissions.
If you have set `read only` you can just change the settings on your app dashboard but you will need
to reset your access tokens as well. 


## Setup: Spotify
To get your spotify developer account you can go [here](https://developer.spotify.com/dashboard/).
You will need to connect your spotify account with your developer account to be able to use the api.
Once youve done that it will give you your access tokens. 


## Test 
Now that you have everything set up you can now test it. Depending on how you have set things up you
can run this in two different ways. If you only want to run this to create playlist for yourself you
can just call the function `create_spotify_playlist_from_search(query:str, name:str)` inside
`createSpotifyPlaylist.py`. `query` will be the type of playlists you want to search for and `name`
will be used in the description of the spotify playlist created. Once you have set that up you can 
simply run `python3 createSpotifyPlaylist.py` and check your spotify account for your playlist.

If you want to run this with twitter. All you need to do is run `python3 twiiter.py`.  This will check
your twitter for @mentions and create spotify playlists based on those. 

