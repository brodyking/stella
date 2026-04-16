import argparse
import sys
import json
from pathlib import Path
from stella.downloader import Download

def load_config():
    # Config path
    config_path = Path.home() / ".config" / "stella" / "config.json"
    # Creates directory if it dosen't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    # Create file with defaults if it dosent exist
    if not config_path.exists():
        default_config = {
            "CLIENT_ID": "",
            "CLIENT_SECRET": "",
            "REDIRECT_URI": "http://127.0.0.1:8080",
        }
        config = default_config or {}
        config_path.write_text(json.dumps(config, indent=2))
        return config
    with config_path.open() as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(prog="Stella",description="A Spotify Downloader")
    parser.add_argument('spotify_url')           # positional argument
    parser.add_argument("-m", "--manual", type=str, help="Manually input the youtube source video")

    args = parser.parse_args()

    config = load_config();

    if (config["CLIENT_ID"] is None or config["CLIENT_SECRET"] is None or config["REDIRECT_URI"] is None or config["CLIENT_ID"] == ""):
        Download.print(None,"ERROR","You must specify your CLIENT_ID, CLIENT_SECRET, and REDIRECT_URI in the config. (~/.config/stella/config.json)")
        exit()
    else:
        Downloader = Download(config["CLIENT_ID"],config["CLIENT_SECRET"],config["REDIRECT_URI"])

    if ("track/" in args.spotify_url):
        if args.manual:
            Downloader.download_track(args.spotify_url,args.manual)
        else:
            Downloader.download_track(args.spotify_url)
    elif("playlist/" in args.spotify_url):
        Downloader.download_playlist(args.spotify_url)
    elif("album/" in args.spotify_url):
        Downloader.download_album(args.spotify_url)
    else:
        Downloader.print("ERROR","You must paste in the full Spotify URL. You can only download using track, album, or playlist links.")
        raise ValueError("You must paste in the full Spotify URL. You can only download using track, album, or playlist links.")

if __name__ == "__main__":
    sys.exit(main())
