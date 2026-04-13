import argparse
import sys
from downloader import Download


def main():
    parser = argparse.ArgumentParser(prog="Stella",description="A Spotify Downloader")
    parser.add_argument('spotify_url')           # positional argument
    parser.add_argument("-m", "--manual", type=str, help="Manually input the youtube source video")

    args = parser.parse_args()

    Downloader = Download()

    if args.manual:
        Downloader.download_track_manual(args.spotify_url,args.manual)
    else:
        Downloader.download_track_auto(args.spotify_url)


if __name__ == "__main__":
    sys.exit(main())
