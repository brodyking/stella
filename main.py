import argparse
import sys
from downloader import Download


def main():
    parser = argparse.ArgumentParser(prog="Stella",description="A Spotify Downloader")
    parser.add_argument('spotify_url')           # positional argument
    parser.add_argument("-m", "--manual", type=str, help="Manually input the youtube source video")

    args = parser.parse_args()

    Downloader = Download()

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

if __name__ == "__main__":
    sys.exit(main())
