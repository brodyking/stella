import api
import yt_dlp
from mutagen.easyid3 import EasyID3

CONFIG = {
    "artist_seperator": ", ",
    "generic_tags": "offical audio topic"}

def attach_metadata(filename,metadata):
    audio = EasyID3(filename)
    audio['title'] = metadata.get("title")
    audio['artist'] = metadata.get("artist")
    audio.save()

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
        "album_art": track_api["album"]["images"][0],
        "release_date": track_api["album"]["release_date"],
        "album_name": album_name
    }

    search_string = f"ytsearch1:{metadata.get('title')} - {metadata.get('artist')} {CONFIG.get('generic_tags')}"

    filename = f"{metadata.get('title')} - {metadata.get('artist')}"
    
    ydl_opts = {
        'format': 'bestaudio/best',  # Download best quality audio/video
        'postprocessors': [{ # Force mp3 output
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f"{filename}.%(ext)s",
        'noplaylist': True,           # Ensure only one video is downloaded
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # extract_info performs the search and download (download=True by default)
            ydl.extract_info(search_string, download=True)
            print(f"Successfully downloaded: {metadata.get('title')}")
        except Exception as e:
            print(f"An error occurred: {e}")

    attach_metadata(f"{filename}.mp3",metadata)

download_track(
    "https://open.spotify.com/track/1vxu8vMNshg5J8z3oA7QJZ?si=a4b3da3a11764b20"
)
