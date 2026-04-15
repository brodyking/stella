import api
import yt_dlp
import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

CONFIG = {
    "artist_seperator": ", ",
}

class Download:

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
            "noplaylist": True,  # Ensure only one video is downloaded
        }
    
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # extract_info performs the search and download (download=True by default)
                ydl.extract_info(youtube_url, download=True)
                print(f"Successfully downloaded: {metadata.get('title')}")

                # Attach metadata if downloaded
                self.attach_metadata(f"{filename}.mp3", metadata)
            except Exception as e:
                print(f"An error occurred: {e}")

    def download_track(self,spotify_url,youtube_url=None):

        # Raw api data from spotiy
        track = api.get_track(spotify_url)

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


    def download_playlist(self,url):

        playlist = api.get_playlist_items(url)

        tracks = []
        for track in playlist["items"]:
            tracks.append(track["item"])

        for track in tracks:
            self.download_track(track["id"])

    def download_album(self,url):

        album = api.get_album(url)

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
