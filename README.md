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
    - [Step 2: Register an app](#step-2-register-an-app)
    - [Step 3: Spotify Auth](#step-3-spotify-auth)
  - [Usage](#usage)
    - [Manual Download Option](#manual-download-option)

<!--toc:end-->

## Requirements

The dependencies for stella are usually installed by default, but they are
listed here aswell:

- requests
- yt-dlp
- mutagen
- dotenv
- spotipy

You will also need a Spotify Premium account to use this app. This is due to
Spotify's new API restrictions.

## Install

### Step 1: Download

First clone this repo (or download and unzip):

```
git clone https://github.com/brodyking/stella.git
```

### Step 2: Spotify Auth

Spotify requires you to have a developer account/app for stella to utilize
Spotify's API. Goto the
[Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and
register a new app.

Then, head back into the root project. Paste the credentials into the
`.env.example` file, and rename it to `.env`.

### Step 3: Installation

Install the application with pip:

```
pip install -e .
```

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
