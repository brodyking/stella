import os
from dotenv import load_dotenv
import spotipy
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

def parse(url):
    if ("playlist/" in url):
        url = url.split("playlist/")[1]
    elif ("album/" in url):
        url = url.split("album/")[1]
    elif ("track/" in url):
        url = url.split("track/")[1]
    elif ("playlist/" in url):
        url = url.split("playlist/")[1]

    if ("?" in url):
        url = url.split("?")[0]

    return url
         

def get_playlist(url):
    url = parse(url)
    return sp.playlist(url)

def get_album(url):
    url = parse(url)
    return sp.album(url)

def get_playlist_items(url):
    url = parse(url)
    return sp.playlist_items(url)

def get_track(url):
    url = parse(url)
    return sp.track(url)   

def get_artist(url):
    url = parse(url)
    return sp.artist(url)


