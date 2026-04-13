# Stella 🐕

Stella is a python script that converts a spotify link to an mp3 file. Using
[yt-dlp](https://github.com/yt-dlp/yt-dlp) and
[spotipy](https://github.com/spotipy-dev/spotipy), it uses the Spotify API to
gather the metadata, while using yt-dlp to download the track from youtube. The
metadata is then combined and a final mp3 is given. Stella's main purpose is as
a [spotdl](https://github.com/spotDL/spotify-downloader) replacement, which
seems to have fallen out of development.

## Table of contents

<!--toc:start-->

- [Stella 🐕](#stella-🐕)
  - [Table of contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Install](#install)
    - [Step 1: Download](#step-1-download)
    - [Step 2: Spotify Auth](#step-2-spotify-auth)
  - [Usage](#usage)

<!--toc:end-->

## Requirements

Make sure to have the following packages installed, alongside their
dependencies.

- yt-dlp
- requests
- mutagen
- dotenv
- spotipy

You will also need a spotify premium account to use this app. This is due to
Spotify's new API restrictions.

## Install

### Step 1: Download

First clone this repo (or download and unzip):

```
git clone https://github.com/brodyking/stella.git
```

### Step 2: Register an app

Spotify requires you to have a developer account/app for stella to utilize
Spotify's API.

### Step 3: Spotify Auth

Create a `.env` file in the folder where the repo is downloaded. Then, fill it
out with the information from your app's dashboard. It should look like this but
with the information filled in:

```
CLIENT_ID=
CLIENT_SECRET=
REDIRECT_URI="http://127.0.0.1:8080"
```

## Usage
