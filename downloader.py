import api
import yt_dlp
import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

CONFIG = {
    "artist_seperator": ", ",
    "generic_tags": "offical audio topic"
}


def attach_metadata(filename, metadata):
    def apply_basic_metadata():
        # Attach basic metadata
        audio = EasyID3(filename)
        audio["title"] = metadata.get("title")
        audio["album"] = metadata.get("album")
        audio["artist"] = metadata.get("artist")
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

def download_track(url):
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

    album_api = api.get_album(track_api["album"]["id"])

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

    search_string = f"ytsearch1:{metadata.get('title')} - {metadata.get('artist')} {CONFIG.get('generic_tags')}"

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
        "outtmpl": f"{filename}.%(ext)s",
        "noplaylist": True,  # Ensure only one video is downloaded
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # extract_info performs the search and download (download=True by default)
            ydl.extract_info(search_string, download=True)
            print(f"Successfully downloaded: {metadata.get('title')}")
        except Exception as e:
            print(f"An error occurred: {e}")

    attach_metadata(f"{filename}.mp3", metadata)


download_track(
    "https://open.spotify.com/track/6MDxjEmwVBrZM1UH9FpYP4?si=afe70faa8f4e44f7"
)
