import os
from dotenv import load_dotenv
import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from mutagen.easyid3 import EasyID3

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

scope = "user-library-read"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=scope,
    )
)


def get_playlist(url):
    playlist_id = url.split("playlist/")[1].split("?")[0]
    return sp.playlist(playlist_id)

def get_playlist_items(url):
    playlist_id = url.split("playlist/")[1].split("?")[0]
    return sp.playlist_items(playlist_id)

def get_track(url):
    playlist_id = url.split("track/")[1].split("?")[0]
    return sp.track(playlist_id)   

def get_artist(url):
    artist_id= url.split("artist/")[1].split("?")[0]
    return sp.artist(artist_id)
