# About the project 
In this project I craeted a python module that creates spotify playlists from the most popular songs in other spotify playlists. It uses a query to search the spotify api for playlists with same words in them. From those spotify playlists that we searched we go through each and find its most popular songs. Those most popular songs get added to the playlist we are trying to craete. 


## Setup Info

This whole project requires you to have Spotify developer account. To get your spotify developer account you can go [here](https://developer.spotify.com/dashboard/). You will need to connect your spotify account with your developer account to be able to use the api. Once you've done that it will give you your access tokens. All the access tokens given by the Spotify developer accounts will need to be added to your `.bash_profile` or `.zshrc` file. For example this is what my `.zshrc` file looks like 
~~~
export SPOTIPY_CLIENT_ID=your_client_id
export SPOTIPY_CLIENT_SECRET=your_client_secret
export SPOTIPY_REDIRECT_URI=your_redirect_uri
export spotifyUserID=your_username
~~~

Now I just run `source ~/.zsrhc`. One thing to mention is that spotifyUserID is simply just your spotify username which you can find in your account settings. The SPOTIPY_REDIRECT_URI will be in your `Dashboard` in your spotify app under `Redirect URIS`. Most often people set it to localhost:800. Once you run the spotify module you will be asked to paste the link it took you to. That should cover most of the setup.




## Running the Project
This project uses a good amount of libraries so first you will need to install them with this command `pip install -r requirements.txt`. Now you can test it out. I have a function with some preset values that uses the `CreateSpotifyPlaylist` class but that can be removed/edited etc for whatever reason. To try it out with the preset values you can use the following command



Test it out with Spotify Only:

- `python3 createSpotifyPlaylist.py`


