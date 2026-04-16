# Stella 🏴‍☠️

Stella is a python script that converts a spotify link to an mp3 file. Using
[yt-dlp](https://github.com/yt-dlp/yt-dlp) and
[spotipy](https://github.com/spotipy-dev/spotipy), it uses the Spotify API to
gather the metadata, while using yt-dlp to download the track from youtube. The
metadata is then combined and a final mp3 is given. Stella's main purpose is as
a [spotdl](https://github.com/spotDL/spotify-downloader) replacement, which
seems to have fallen out of development.

## Table of contents

<!--toc:start-->

- [Stella 🏴‍☠️](#stella-🏴‍️)
  - [Table of contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Install](#install)
    - [Step 1: Download](#step-1-download)
    - [Step 2: Installation](#step-2-installation)
    - [Step 3: Spotify Auth](#step-3-spotify-auth)
  - [Usage](#usage)
    - [Manual Download Option](#manual-download-option)

<!--toc:end-->

## Requirements

The python dependencies for stella are usually already installed by other
packages, but they are listed here aswell:

- requests
- yt-dlp
- mutagen
- dotenv
- spotipy

You will also need [FFmpeg](https://ffmpeg.org/), which can be installed from
[Winget](https://github.com/microsoft/winget-cli) or
[Homebrew](https://brew.sh/) on Windows and macOS respectively.

You will also need a Spotify Premium account to use this app. This is due to
Spotify's new API restrictions.

## Install

### Step 1: Download

First clone this repo (or download and unzip):

```
git clone https://github.com/brodyking/stella.git
```

### Step 2: Build and Installation

To install the application with pip, run this command while in the root
directory of the repository (folder with `pyproject.toml`):

```
pip install .
```

### Step 3: Spotify Auth

Spotify requires you to have a developer account/app for stella to utilize
Spotify's API. Goto the
[Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and
register a new app.

When you first run `stella` in the terminal, it should create the configuration
file. It can be found at `~/.config/stella/config.json`. If it was not already
created, you can create it manually. It should look like this by default:

```json
{
  "CLIENT_ID": "",
  "CLIENT_SECRET": "",
  "REDIRECT_URI": "http://127.0.0.1:8080"
}
```

Fill it in with your API keys here. On the first run after, it will ask you to
paste a URL into your browser. Paste it, then copy the URL you were redirected
to in the terminal. Then stella should work without issue.

## Usage

On the first use of the app, it will open a browser window for authentication.

Open the directory where you want to download the mp3's to, and run the script
with the spotify URL.

```
stella https://open.spotify.com/track/5DnT9a5IM3eMjKgXTWVJvi
```

### Manual Download Option

If you include `-m` or `--manual` followed by a youtube link, it will merge the
Spotify metadata with the Youtube audio. **This only works when downloading a
track.**

```
stella https://open.spotify.com/track/5DnT9a5IM3eMjKgXTWVJvi?si=5bb3015e563d4434 -m https://www.youtube.com/watch?v=iyf0ZIh3SVo
```
