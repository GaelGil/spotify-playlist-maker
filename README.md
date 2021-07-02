# About the project 
In this project I craeted a python module that creates spotify playlists from the most popular songs in spotify playlists. It uses a some words to search the spotify api for playlists with same words in them. From those spotify playlists that we searched we go through each and find its most popular songs. Those most popular songs get added to the playlist we are trying to craete. 

Check out this project [here](https://twitter.com/_gg_bot). This is a link to my twitter that is connected to this project. What you will find here is my timeline where you will see tweets that I have tweeted at myself to test out this project. You will also see replies to those tweets with links to spotify playlists that were created using this project.


## Setup Info

This whole project requires you to have a Twitter developer account and Spotify developer account. However you can choose to only have a spotify developer account and run this for yourself without the `twitter.py`. Lastly all the access tokens given by the developer accounts will need to be added to your `.bash_profile` or `.zshrc` file. Make sure to name them as they are in the `twitter.py` and `createSpotifyPlaylist.py` files for easy use. Also don't  forget to source the files. 


## Setup: Twitter

To get your twitter developer account you can go [here](https://developer.twitter.com/en/apply-for-access). Once you apply you might have to wait to get access. Once you have access you will need to create an app on your dashboard. Now that you have your app you can save your access tokens that you were given so you can use those later. One thing to keep in mind is to enable `read and write` permissions. If you have set `read only` you can just change the settings on your app dashboard but you will need to reset your access tokens as well and use the new ones.


## Setup: Spotify

To get your spotify developer account you can go [here](https://developer.spotify.com/dashboard/). You will need to connect your spotify account with your developer account to be able to use the api. Once you've done that it will give you your access tokens.


## Run 

Install the requirements:

- `pip install -r requirements.txt`

Run Pytest
This module uses a modified version of the original functions. The reason for this is because the original module uses the spotify API. What I did was supply the data in a seperate file and take out the API calls so anyone can test the code without yet having the proper credentials. `functionstotest.py` contains the modifed functions without API calls. Now you can test the functions without using the API.

- `pytest test_create_spotify_playlist.py`

- `pytest test_twitter.py`


Test it out with Twitter:

- `python twitter.py`

Test it out with Spotify Only:

- `python3 createSpotifyPlaylist.py`


