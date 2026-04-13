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
            audio["title"] = metadata.get("title")
            audio["album"] = metadata.get("album")
            audio["artist"] = metadata.get("artist")
            audio["date"] = metadata.get("release_date")
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
        apply_basic_metadata();
        apply_album_art();

    def download_track_manual(self,spotify_url,youtube_url):
        # Raw api data from spotiy
        track_api = api.get_track(spotify_url)

        # Gets artist, if multiple combines them
        artist = ""
        artist_id = ""
        i = 0
        for artist_api in track_api["album"]["artists"]:
            if i > 0:
                # Adds seperator if more than 1 artist
                artist += CONFIG.get("artist_seperator")
            else:
                # Uses the first artist as the artist ID
                artist_id = artist_api["id"]
            artist += artist_api["name"]
            i += 1
        del i

        album_api = api.track_api["album"]

        album_name = album_api["name"]

        # Metadata dict
        metadata = {
            "title": track_api["name"],
            "artist": artist,
            "arist_id": artist_id,
            "album_art": track_api["album"]["images"][0]["url"],
            "release_date": track_api["album"]["release_date"],
            "album": album_name,
        }

        filename = f"{metadata.get('title')} - {metadata.get('artist')}"

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
           
                self.attach_metadata(f"{filename}.mp3", metadata)
            except Exception as e:
                print(f"An error occurred: {e}")

    def download_track_auto(self,url):
        # Raw api data from spotiy
        track_api = api.get_track(url)

        # Gets artist, if multiple combines them
        artist = ""
        artist_id = ""
        i = 0
        for artist_api in track_api["album"]["artists"]:
            if i > 0:
                # Adds seperator if more than 1 artist
                artist += CONFIG.get("artist_seperator")
            else:
                # Uses the first artist as the artist ID
                artist_id = artist_api["id"]
            artist += artist_api["name"]
            i += 1
        del i

        album_api = track_api["album"]

        album_name = album_api["name"]

        # Metadata dict
        metadata = {
            "title": track_api["name"],
            "artist": artist,
            "arist_id": artist_id,
            "album_art": track_api["album"]["images"][0]["url"],
            "release_date": track_api["album"]["release_date"][0:4],
            "album": album_name,
        }

        search_string = f"ytsearch1:{metadata.get('title')} - {metadata.get('artist')}"

        filename = f"{metadata.get('title')} - {metadata.get('artist')}"

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
                ydl.extract_info(search_string, download=True)
                print(f"Successfully downloaded: {metadata.get('title')}")
           
                self.attach_metadata(f"{filename}.mp3", metadata)
            except Exception as e:
                print(f"An error occurred: {e}")

    def download_playlist(self,url):

        playlist_api = api.get_playlist_items(url)

        tracks = []
        for track in playlist_api["items"]:
            tracks.append(track["item"])

        for track in tracks:
        
            # Raw api data from spotiy
            track_api = track

            # Gets artist, if multiple combines them
            artist = ""
            artist_id = ""
            i = 0
            for artist_api in track_api["album"]["artists"]:
                if i > 0:
                    # Adds seperator if more than 1 artist
                    artist += CONFIG.get("artist_seperator")
                else:
                    # Uses the first artist as the artist ID
                    artist_id = artist_api["id"]
                artist += artist_api["name"]
                i += 1
            del i

            album_api = track["album"]

            album_name = album_api["name"]

            # Metadata dict
            metadata = {
                "title": track_api["name"],
                "artist": artist,
                "arist_id": artist_id,
                "album_art": track_api["album"]["images"][0]["url"],
                "release_date": track_api["album"]["release_date"][0:4],
                "album": album_name,
            }

            search_string = f"ytsearch1:{metadata.get('title')} - {metadata.get('artist')}"

            filename = f"{metadata.get('title')} - {metadata.get('artist')}"

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
                    ydl.extract_info(search_string, download=True)
                    print(f"Successfully downloaded: {metadata.get('title')}")
           
                    self.attach_metadata(f"{filename}.mp3", metadata)
                except Exception as e:
                    print(f"An error occurred: {e}")
