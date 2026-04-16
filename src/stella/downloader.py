from stella.api import Api
import yt_dlp
import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

CONFIG = {
    "version": "1.0.0",
    "artist_seperator": ", ",
    "logs_enabled": True,
    "logs_logo": 'Stella',
    "ytdlp_show_console": False
}

class Download:

    def __init__(self,client_id,client_secret,redirect_uri):
        self.api = Api(client_id,client_secret,redirect_uri)

    def print(self,type,content):
        if CONFIG.get("logs_enabled"):

            RED = '\033[31m'
            GREEN = '\033[32m'
            RESET = '\033[0m'
            
            output = f"[{CONFIG.get('logs_logo')}] [{type}] {content}"
            if (type == "OK"):
                output = f"{GREEN}{output}{RESET}"
            if (type == "ERROR"):
                output = f"{RED}{output}{RESET}"
            print(output)

    def attach_metadata(self,filename, metadata):
        def apply_basic_metadata():
            # Attach basic metadata
            audio = EasyID3(filename)
            audio["title"] = [metadata.get("title")]
            audio["album"] = [metadata.get("album")]
            audio["artist"] = [metadata.get("artist")]
            audio["albumartist"] = [metadata.get("album_artist")]
            audio["date"] = [metadata.get("release_date")]
            audio["tracknumber"] = [metadata.get("track_number")]
            audio.save()
        def apply_album_art():
            # Attach album art
            response = requests.get(metadata.get("album_art"))
            img_data = response.content

            try:
                audio = ID3(filename)
            except Exception:
                # Create a new tag if one doesn't exist
                audio = ID3()
                audio.save(filename)
                audio = ID3(filename)
            audio.add(
                APIC(
                    encoding=3,  # 3 is for UTF-8
                    mime="image/jpeg",  # Change to image/png if applicable
                    type=3,  # 3 is for the front cover
                    desc="Cover",
                    data=img_data,
                )
            )
            audio.save(v2_version=3)
        apply_basic_metadata()
        apply_album_art()

    def download_file(self,youtube_url,filename,metadata):

        self.print("OK",f"Starting download for {metadata.get('title')}")

        ydl_opts = {
            "format": "bestaudio/best",  # Download best quality audio/video
            "postprocessors": [
                {  # Force mp3 output
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "match_filter": yt_dlp.utils.match_filter_func("!is_live & !is_upcoming"),
            "outtmpl": f"{filename}.%(ext)s",
            "default_search": "ytmsearch",
            "extractor_args": {
                "youtube": {
                    "search_source": ["ytm"]
                }
            },
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,  # Ensure only one video is downloaded
        }
    
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # extract_info performs the search and download (download=True by default)
                ydl.extract_info(youtube_url, download=True)
                self.print("OK",f"Finished downloading {metadata.get('title')}")

                # Attach metadata if downloaded
                self.attach_metadata(f"{filename}.mp3", metadata)
            except Exception as e:
                self.print("ERROR",f"Download could not be completed for {metadata.get('title')}")

    def download_track(self,spotify_url,youtube_url=None):

        self.print("OK",f"Gathering metadata for {spotify_url}")

        # Raw api data from spotiy
        track = self.api.get_track(spotify_url)

        # Gets artist, if multiple combines them
        artist = ""
        artist_id = ""
        i = 0
        for artist_data in track["album"]["artists"]:
            if i > 0:
                # Adds seperator if more than 1 artist
                artist += CONFIG.get("artist_seperator")
            else:
                # Uses the first artist as the artist ID
                artist_id = artist_data["id"]
            artist += artist_data["name"]
            i += 1
        del i

        # Metadata dict
        metadata = {
            "title": track["name"],
            "artist": artist,
            "arist_id": artist_id,
            "album_art": track["album"]["images"][0]["url"],
            "release_date": track["album"]["release_date"][0:4],
            "track_number": track["track_number"],
            "album_artist": track["album"]["artists"][0]["name"],
            "album": track["album"]["name"]
        }

        # The filename
        filename = f"{metadata.get('track_number')} {metadata.get('title')} - {metadata.get('artist')}"

        # If no URL provided, yt-dlp uses a search term instead.
        if (youtube_url is None):
            youtube_url = f"ytsearch1:{metadata.get('title')} - {metadata.get('artist')}"

        self.download_file(youtube_url,filename,metadata)


    def download_playlist(self,spotify_url):

        self.print("OK",f"Gathering metadata for {spotify_url}")

        playlist = self.api.get_playlist_items(spotify_url)

        tracks = []
        for track in playlist["items"]:
            tracks.append(track["item"])

        for track in tracks:
            self.download_track(track["id"])

    def download_album(self,spotify_url):

        self.print("OK",f"Gathering metadata for {spotify_url}")

        album = self.api.get_album(spotify_url)

        for track in album["tracks"]["items"]:         

            # Gets artist, if multiple combines them
            artist = ""
            artist_id = ""
            i = 0
            for artist_data in track["artists"]:
                if i > 0:
                    # Adds seperator if more than 1 artist
                    artist += CONFIG.get("artist_seperator")
                else:
                    # Uses the first artist as the artist ID
                    artist_id = artist_data["id"]
                artist += artist_data["name"]
                i += 1
            del i

            # Metadata dict
            metadata = {
                "title": track["name"],
                "artist": artist,
                "arist_id": artist_id,
                "album_art": album["images"][0]["url"],
                "release_date": album["release_date"][0:4],
                "track_number": track["track_number"],
                "album_artist": album["artists"][0]["name"],
                "album": album["name"]
            }

            # The filename
            filename = f"{metadata.get('track_number')} {metadata.get('title')} - {metadata.get('artist')}"

            youtube_url = f"ytsearch1:{metadata.get('title')} - {metadata.get('artist')}"

            self.download_file(youtube_url,filename,metadata)
