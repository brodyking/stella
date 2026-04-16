import spotipy
from spotipy.oauth2 import SpotifyOAuth
from mutagen.easyid3 import EasyID3

class Api:
    def __init__(self,client_id,client_secret,redirect_uri):
      
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope="user-library-read",
            )
        )

    def parse(self,url):
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
         

    def get_playlist(self,url):
        url = self.parse(url)
        return self.sp.playlist(url)

    def get_album(self, url):
        url = self.parse(url)
        return self.sp.album(url)

    def get_playlist_items(self, url):
        url = self.parse(url)
        return self.sp.playlist_items(url)

    def get_track(self, url):
        url = self.parse(url)
        return self.sp.track(url)   

    def get_artist(self, url):
        url = self.parse(url)
        return self.sp.artist(url)


