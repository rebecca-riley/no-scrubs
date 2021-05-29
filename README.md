# no-scrubs
no-scrubs is an application which scrubs track metadata from Spotify playlists and liked songs and outputs it in csv format.

## Introduction
Welcome to **No Scrubs**!  As a DJ for [KUCI Irvine](kuci.org), spend a lot of time with my music collection.  I keep all my tracks in a spreadsheet so I can sort by genre, artist, release date, popularity, and label to streamline bringing you "the best mix of mellow, upbeat, and underground music on public radio."™  Manually inputting information for each track was incredibly tedious, so I decided to automate the process with a script to "scrub" my Spotify music library for metadata.  Thus, **No Scrubs** was born.

I hope other DJs and music lovers alike will benefit from the ability to compile information and metrics from their music libraries, whether to share their music with the world, work with and see trends in large collections, or simply to better understand their own tastes.  I am happy to receive comments, feedback, and requests for future features.  Please shoot me an email at rebecca.riley@uci.edu to get in touch.

Long live independent music!  
_**Rebecca Riley**_  
Host of [_The Rebelution_](facebook.com/rebelutionradio) at [WRVU Nashville](https://wrvu.org/) and [_Violet Freedom_](violetfreedom.kuci.org/) at [KUCI Irvine](kuci.org)  
[facebook.com/rebelutionradio](facebook.com/rebelutionradio)

## Installation
To install **No Scrubs**, you will need:
1.  no-scrubs.py
2.  a Python installation
3.  a Spotipy installation
4.  the passphrase

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

#### 4. the passphrase
In order for Spotify to authorize you to use **No Scrubs**, you need a passphrase which I must generate.  To get the passphrase, please send me (rebecca.riley@uci.edu) an email with the subject line 'passphrase' and I'll send it to you.
