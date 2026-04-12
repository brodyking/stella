import api
import yt_dlp

CONFIG = {
    "artist_seperator": ", ",
    "generic_tags": "offical audio topic"}

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

    # Get the artist genre
    
    # Metadata dict
    metadata = {
        "name": track_api["album"]["name"],
        "artist": artist,
        "arist_id": artist_id
    }

    search_string = f"ytsearch1:{metadata.get('name')} - {metadata.get('artist')} {CONFIG.get('generic_tags')}"
    
    ydl_opts = {
        'format': 'bestaudio/best',  # Download best quality audio/video
        'postprocessors': [{ # Force mp3 output
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f"{metadata.get('name')} - {metadata.get('artist')}.%(ext)s",
        'noplaylist': True,           # Ensure only one video is downloaded
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # extract_info performs the search and download (download=True by default)
            ydl.extract_info(search_string, download=True)
            print(f"Successfully downloaded: {metadata.get('name')}")
        except Exception as e:
            print(f"An error occurred: {e}")

download_track(
    "https://open.spotify.com/track/6mFkJmJqdDVQ1REhVfGgd1?si=e7dd9da2076b433b"
)
