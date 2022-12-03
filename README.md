# no-scrubs
no-scrubs is an application which scrapes track metadata from Spotify playlists and liked songs and outputs it in tsv format.

## Introduction
Welcome to **No Scrubs**!  As a DJ for [KUCI Irvine](https://kuci.org), I spend a lot of time with my music collection.  I keep all my tracks in a spreadsheet so I can sort by genre, artist, release date, popularity, and label to streamline bringing you "the best mix of mellow, upbeat, and underground music on public radio."™  Manually inputting information for each track was incredibly tedious, so I decided to automate the process with a script to "scrub" my Spotify music library for metadata.  Thus, **No Scrubs** was born.

I hope other DJs and music lovers alike will benefit from the ability to compile information and metrics from their music libraries, whether to share their music with the world, work with and see trends in large collections, or simply to better understand their own tastes.  I am happy to receive comments, feedback, and requests for future features.  Please shoot me an email at rebeccariley@kuci.org to get in touch.

Long live independent music!  
_**Rebecca Riley**_  
Host of [_The Rebelution_](https://facebook.com/rebelutionradio) at [WRVU Nashville](https://wrvu.org/) and [_Violet Freedom_](https://violetfreedom.kuci.org/) at [KUCI Irvine](https://kuci.org)  
[facebook.com/rebelutionradio](https://facebook.com/rebelutionradio)

## Installation
To run **No Scrubs**, you will need:
1.  no-scrubs.py
2.  a Python installation
3.  a Spotipy installation

#### 1. no-scrubs.py
You can obtain no-scrubs.py either by (a) cloning the [no-scrubs repository](https://github.com/rebecca-riley/no-scrubs) or (b) directly downloading it from GitHub.  I recommend the latter.

At the top of [this page](https://github.com/rebecca-riley/no-scrubs), you should see a green button that says "Code."  Choose to "Download Zip."  Once you extract the files, move no-scrubs.py to a convenient location on your machine.

#### 2. a Python installation
The [Python website](https://www.python.org/downloads/) is your source for Python installers and binaries.

**Mac/Linux:** Modern Macs and most popular Linux distributions come with Python preinstalled.  To see if Python is installed on your machine, open your terminal and type `python --version`.  If Python is installed, this will return the Python version you are running.  If you do not have Python natively, installers are available on [python.org](https://www.python.org/downloads/).

**Windows:** If you are on a new version of Windows (updated since May 2019), you can download Python directly from the Microsoft Store.  This is the best installation option as it simplifies the next step.  If you have an older version of Windows, download and run a Windows installer from [python.org](https://www.python.org/downloads/).

#### 3. a Spotipy installation
[Spotipy](https://spotipy.readthedocs.io/) is a Python library that allows **No Scrubs** to collect and sift through metadata from your Spotify library.

**Mac/Linux:** In your terminal, type `pip install spotipy`.

**Windows:** If you installed Python through the Microsoft Store, open a terminal window and type `pip install spotipy`.  If you installed Python with an installer from [python.org](https://www.python.org/downloads/), type `py -m pip install spotipy` instead.

## Usage
#### Running no-scrubs.py
To run the program, open a terminal in Mac/Linux or the Command Prompt in Windows.  Navigate to the folder in which you saved no-scrubs.py and run `python no-scrubs.py`.  If you are on Mac/Linux, your output files will be saved in your current directory (typically the same folder as no-scrubs.py; use `pwd` to check).  If you're on Windows, they will be saved in the same folder as no-scrubs.py.

A typical terminal input might look like:
```
$ cd Downloads/no-scrubs/
$ python no-scrubs.py
```
( Hint if you are new to terminals: You don't need to type the '$'. :] )

If you're on Windows, you can run no-scrubs.py by double-clicking it.  This can be buggy, though -- if it doesn't work for some reason, try using Command Prompt instead.

#### What's my username?
The first thing the program will prompt you for is your Spotify username.  Your username is *not* the same as your display name.  To find your username, go to [spotify.com](https://open.spotify.com/), log in, and go to 'Account' in the settings.

There is only an indirect way to determine your username on mobile.  In the Spotify app, go to Home > Settings (gear icon) > View Profile > three dots menu > Share.  Copy the link and paste it into a note.  The link will be in the format [https://open.spotify.com/user/[username]?...]()  Your username is everything after 'user/' and before '?'.

#### Data output options
1.  Liked songs and/or playlists
    You can have **No Scrubs** output info for your liked songs ('liked'), your playlists ('playlists'), or both (hit enter).
2.  Recently updated playlists
    You can limit output to only recently updated playlists.  Enter a cutoff date in mm-dd-yyyy format, or hit enter to output info for all your playlists.
3.  Recently updated songs in your playlists
    You can limit output to only the recently updated songs in your playlists.  Enter a cutoff date in mm-dd-yyyy format, or press enter to output info for all the songs     in your playlists.
4.  Playlists created by others
    You can download song info for playlists you follow but did not create ('yes'), or only output playlists created by you (hit enter).
5.  Recently added liked songs
    You can limit output to only recently liked songs.  Enter a cutoff date in mm-dd-yyyy format, or press enter to output info for all your liked songs.

#### Opening the output files
**No Scrubs** generates a .tsv (tab separated value) file for each playlist it processes, as well as one for your liked songs.  These .tsv files can be opened by Excel or LibreOffice Calc.  To open in Excel, open a blank workbook and go to File > Open > Browse.  You may need to select 'All Files' in the dropdown for .tsv files to appeaar in the dialog box.  When you select your .tsv file, a Text Import Wizard will open.  The data in your .tsv file is **delimited** with **tabs**, and it **has headers**; choose the corresponding options.  Once you do so, all your data will be imported into Excel.  You can save it as an Excel file for easier reopening in the future.  If some of the cells display '#####', increase the size of the column.

LibreOffice Calc has a similar import assistant; select tab delimited and your workbook will be correctly populated.

## Features
#### Playlist info
Data in the tsv output file is listed as artist - track - album - label - genre.  You can copy and paste right into your email for weekly playlist submissions!

#### A-play / B-play / grey area
**No Scrubs** suggests whether a song in your library is A-play, B-play, or grey area.  The program makes this determination based on a combination of track popularity and overall artist popularity.  I hand-calibrated the popularity bounds based on A-play, B-play, and grey area songs from my own music collection; you can see those results [here](https://violetfreedom.kuci.org/post/663523339838603264/no-scrubs-popularity-calibration-during-the).  Your mileage may vary, so always check and adjust these suggestions for your personal use.

#### OPI (Obscenity, Profanity, Indecency)
**No Scrubs** indicates whether or not songs contain profanity, _as determined by Spotify._  **This identification is not always accurate.  Always personally verify that songs do not contain profanity before airing.**  My testing of this feature suggests that Spotify uses AI to test for explicit lyrics, with human verification for more popular songs.[* ](#ftnt1)  In my experience, explicit tags are less accurate for less popular and foreign-language songs.  Proceed accordingly.

#### Other features
Exported data also includes a 30 second song preview (where available), metrics like danceability and acousticness, artist and track popularity, and release and add dates.

<a name="ftnt1">*</a> There seems to be some evidence of this in a patent Spotify filed in 2020 for a "spoken words analyzer": https://www.digitalmusicnews.com/2020/12/17/spotify-spoken-words-analyzer-patent/.

## Future additions
- [ ] Genre metadata  
The vast majority of songs on Spotify do not have a published genre.  It's obvious from their annual "Wrapped" feature that Spotify does collect this information, but for whatever reason they've decided to keep it inaccessible via their API.[* ](#ftnt2)  I have a fancy idea to someday incorporate the genre data from one of my favorite websites ever, [Every Noise at Once](https://everynoise.com/), but no immediate implementation plans.  If someone would like to fork and attempt this, feel free.

- [ ] Fixing color commands for Windows terminals  
no-scrubs.py contains commands to color some output text in Unix shells for readability.  This is output as gibberish in Windows terminals.  The program is still perfectly functional, but readability suffers.

<a name="ftnt2">*</a> Genre is an "available" piece of metadata for tracks, but it always comes back blank.  This is a known bug of the Spotify API which its developers have declined to fix.
