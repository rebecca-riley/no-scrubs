#!/usr/bin/env python3 -Xutf8

# No Scrubs: a command-line interface to scrub Spotify metadata from user libraries
#            and consolidate it into tsv format
# author: Rebecca Riley
# contact: rebecca.riley@uci.edu
# date: October 19 2022

import sys
import os
import datetime
import re
import spotipy
import spotipy.util
import platform

LOCAL_ZULU_OFFSET = -8  # represents PST (Los Angeles, CA time)
GREEN   = 32            # terminal color codes
LTRED   = 91
LTYLLW  = 93
BLUE    = 94
LTPINK  = 95
LTCYAN  = 96


#### HELPER FUNCTIONS ####

# formats date string (from Spotify metadata) as datetime object
def add_date(add_date_str):
    date = ((add_date_str.split('T'))[0]).split('-')
    time = ((add_date_str.split('T'))[1]).split(':')
    add_date = datetime.date(int(date[0]),int(date[1]),int(date[2]))
    if (int(time[0]) + LOCAL_ZULU_OFFSET) < 0:   # added on previous day in local time
        return add_date - datetime.timedelta(1)
    else:
        return add_date


# formats date string (from user input) as datetime object
def parse_date_entry(cutoff_date):
    long_ago = datetime.date(1900,1,1) # arbitrary date from long ago

    if cutoff_date:
        try:
            cutoff = cutoff_date.split('-')
            cutoff_datetime = datetime.date(int(cutoff[2]),int(cutoff[0]),int(cutoff[1]))
        except: # any entry outside of the date format should default to long_ago
            cutoff_datetime = long_ago
    else: # no cutoff date provided
        cutoff_datetime = long_ago

    return cutoff_datetime


# takes string and returns system-acceptable filename
# > replaces white space with '_'
# > replaces illegal characters with '-'
def formatted_filename(unformatted_filename):
    return re.sub(' ','_',(re.sub(r'[<>*."/\\[\]:;|,?]','-',unformatted_filename)))


# returns strings that will print to terminal in specified color
def color(string,colour):
    return '\033[' + str(colour) + 'm' + string + '\033[0m'


# prints songs for which data will be output in a consistent format
def print_processing(song_number,total_songs,artist,title):
    print('{:<20s}{:<28.26}{:<41.41s}'
          .format(color(('['+str(song_number)+'/'+str(total_songs)+']'),GREEN),
                  ((artist[0:23] + '...') if len(artist) > 26 else artist),
                  ((title[0:38] + '...') if len(title) > 41 else title)
                 )
         )


# prints songs which will be skipped in a consistent format
def print_skipping(song_number,total_songs,title,message):
    # 2nd, 3rd columns are wider to accomodate additional coloring characters
    print('{:<20s}{:<37.35}{:<50.50s}'
          .format(color(('['+str(song_number)+'/'+str(total_songs)+']'),BLUE),
                  color(('...Skipping (' + message + ')'),BLUE),
                  color(((title[0:38] + '...') if len(title) > 41 else title),BLUE)
                 )
         )


# makes a composite string for fields that may contain more than one item (e.g. artists)
def chain_multiple(list_of_objects):
    chain = ''
    chain += list_of_objects[0]['name']
    for i in range(1,len(list_of_objects)):
        chain += ', ' + list_of_objects[i]['name']
    return chain

# @todo: combine with chain_multiple
def chain_multiple_plain(list_of_objects):
    chain = ''
    chain += list_of_objects[0] if len(list_of_objects) != 0 else ''
    for i in range(1,len(list_of_objects)):
        chain += ', ' + list_of_objects[i]
    return chain


# recommends A-play, B-play, or grey status for songs based on popularity
# @todo: reassess popularity benchmarks
def KUCI_recommendation(track_popularity,artist_popularity):
    if artist_popularity > 68 or track_popularity > 60:
        return 'B'
    elif artist_popularity > 50 or track_popularity > 50:
        return 'G'
    else: # artist_popularity < 50 and track_popularity < 50
        return 'A'


#### PROCESSING FUNCTIONS ####

# outputs data in tsv format for a playlist or list of liked songs
def process_list(playlist_or_liked_songs,list_name,spotify,cutoff_date,new_songs_only):
    # start tsv
    if platform.system() == 'Windows': # see spotipy issue #870 on github
        outfile = open(str(os.path.dirname(os.path.abspath(__file__))) + '\\' +
                           formatted_filename(list_name) + '.tsv','w',
                           encoding='utf-8')
    else:
        outfile = open(formatted_filename(list_name) + '.tsv','w')
    write_out_header(outfile)

    total_songs = playlist_or_liked_songs['total']
    current_song = 0

    # loop through playlist or liked songs while there are still unprocessed tracks
    tracks_remaining = True
    while tracks_remaining:

        # cycle through batch of songs (max batch size = 50)
        for saved_track in playlist_or_liked_songs['items']:
            current_song += 1

            # skip item if added after cutoff date
            if new_songs_only and add_date(saved_track['added_at']) < cutoff_date:
                print_skipping(current_song,total_songs,saved_track['track']['name'],
                               ('++' + (saved_track['added_at'].split('T'))[0]))
                continue

            # if track is local, print only track name and write out modified row
            if saved_track['track']['is_local']:
                print_processing(current_song,total_songs,'(local)',
                                 saved_track['track']['name'])
                outfile.write('(local)' + '\t')
                outfile.write(saved_track['track']['name'])
                outfile.write('\n')
                continue

            # otherwise, process song
            track = saved_track['track']
            album = spotify.album(track['album']['id'])
            artist = spotify.artist(track['artists'][0]['id'])

            # output processing message to terminal
            print_processing(current_song,total_songs,
                             chain_multiple(track['artists']),track['name'])

            # write Spotify metadata to outfile
            write_out_KUCI_info(outfile,track,album,artist)
            write_out_popularity_info(outfile,track,
                                spotify.artist(track['artists'][0]['id'])['popularity'])
            write_out_other_info(outfile,track,album,saved_track)
            write_out_audio_features(outfile,spotify.audio_features(track['id'])[0])
            outfile.write('\n')

        # check and see if there are more songs remaining.  if so, loop continues.
        tracks_remaining = playlist_or_liked_songs['next'] # gives link or 'None'
        if tracks_remaining: # update playlist_or_liked_songs with new batch
            playlist_or_liked_songs = spotify.next(playlist_or_liked_songs)

    outfile.close()
    print('Song info successfully written to ' + formatted_filename(list_name) + '.tsv.')
    print()


#### WRITEOUT FUNCTIONS ####

# write column labels to outfile
def write_out_header(outfile):
    outfile.write('Artist\tTrack\tAlbum\tLabel\tGenre\tSuggested KUCI status\t'\
                  'Track Popularity\tArtist Popularity\tOPI?\tRelease date\t'\
                  'Add date\t30s preview\t'\
                  'Danceability\tEnergy\tTempo\tValence\tAcousticness\t'\
                  'Instrumentalness\tSpeechiness\tLoudness\tLiveness\n')


# write artist, track, album, label, and genre to outfile
def write_out_KUCI_info(outfile,track,album,artist):
    # track
    outfile.write(chain_multiple(track['artists']) + '\t' + track['name'] + '\t')

    # album -- distinguish between singles, EPs, and full albums
    if album['album_type'] != 'single':
        outfile.write(album['name'] + '\t')
    elif album['tracks']['total'] > 1: # 'single' with more than one track = EP
        outfile.write(album['name'] +  # don't add 'EP' if album already has it
                     (' EP' if album['name'][-2:] != 'EP' else '') + '\t')
    else:
        outfile.write('Single' + '\t')

    # label
    outfile.write(((album['label'] or "") if album['label'] != track['artists'][0]['name']
                                  else 'Self-released') + '\t')
    # genre
    outfile.write(chain_multiple_plain(artist['genres']) + '\t')


# write KUCI recommended status, track popularity, and artist popularity to outfile
def write_out_popularity_info(outfile,track,artist_popularity):
    # KUCI recommended status
    outfile.write(KUCI_recommendation(track['popularity'],artist_popularity) + '\t')

    # track popularity
    outfile.write(str(track['popularity']) + '\t')

    # artist popularity
    outfile.write(str(artist_popularity) + '\t')


# write OPI, release date, add date, and preview to outfile
def write_out_other_info(outfile,track,album,metatrack):
    # OPI
    outfile.write(('Yes' if track['explicit'] else 'No') + '\t')

    # release date
    outfile.write(album['release_date'] + '\t')

    # add date
    outfile.write(f"{(add_date(metatrack['added_at'])):%Y-%m-%d}" + '\t')

    # preview url
    # 'or' leaves column blank if no preview url
    outfile.write(str(track['preview_url'] or '') + '\t')


# write audio features (e.g. tempo, danceability) to outfile
def write_out_audio_features(outfile,audio_feature):
    outfile.write(str(audio_feature['danceability']) + '\t' +
                  str(audio_feature['energy']) + '\t' +
                  str(audio_feature['tempo']) + '\t' +
                  str(audio_feature['valence']) + '\t' +
                  str(audio_feature['acousticness']) + '\t' +
                  str(audio_feature['instrumentalness']) + '\t' +
                  str(audio_feature['speechiness']) + '\t' +
                  str(audio_feature['loudness']) + '\t' +
                  str(audio_feature['liveness']) + '\t')


#### MAIN EXECUTION ####

def main():
    # introductory info: purpose of program and contact info
    print('Welcome to No Scrubs!  This program will output a tsv file containing all the ')
    print('info we\'re required to submit in our playlists (artist - track - album - label')
    print('- genre), plus some other metadata to help you keep your library organized')
    print('(e.g. add date, OPI info, a preview link, track and artist popularity, and')
    print('more).')
    print()
    print('I made this primarily for myself, but I hope you can find it useful as well. ')
    print('Long live KUCI and independent music!')
    print()
    print('-----------------------------------------------------------------------------')
    print('If you\'re using this program and you haven\'t obtained the passphrase from me,')
    print('STOP.  Email rebecca.riley@uci.edu with the subject line \'passphrase\' and')
    print('I\'ll send it to you.')
    print('(n.b. Enter the passphrase *carefully*! If you don\'t, you\'ll get a nasty')
    print('      error. Be aware that most terminals don\'t support Ctrl+V for paste -- ')
    print('      you\'ll need to right-click paste instead!!)')
    print('-----------------------------------------------------------------------------')
    print()

    # activate color for Windows systems
    if platform.system() == 'Windows':
        os.system('color')

    # prompt for client secret and spotify username
    secret = input('What\'s the ' + color('passphrase',LTYLLW) + '? ')
    print()

    username = input('What\'s your ' + color('Spotify username',LTRED) + '? ')
    print()

    # liked songs, playlists, or both?
    print('>> Output options >>')
    print('By default, this program will output song info for your ' +
          color('liked songs',LTCYAN) + ' and for ')
    print(color('playlists',LTPINK) + ' you\'ve created.')
    print()
    print('To output info for ' + color('liked songs',LTCYAN) + ' only, type ' +
          color('\'liked\'',LTCYAN) + '.  To output info for ' + color('playlists',LTPINK))
    which_songs = input('only, type ' + color('\'playlists\'',LTPINK) +
                        '.  Any other input will default to outputting both: ')
    print()

    # default behavior -- both liked & playlists
    LIKED = True
    PLAYLISTS = True
    scope = 'user-library-read,user-top-read,playlist-read-private,playlist-read-collaborative'

    # if just liked or just playlists, reset the defaults
    if which_songs == ('liked' or 'like'):
        PLAYLISTS = False
        scope = 'user-library-read,user-top-read'
    elif which_songs == ('playlists' or 'playlist'):
        LIKED = False
        scope = 'playlist-read-private,playlist-read-collaborative,user-top-read'

    # contact spotify, verify user permissions
    print('>> Contacting Spotify >>')

    try:
        # specify cache_path for Windows -- see spotipy issue #870 on github
        if platform.system() == 'Windows':
            cache = (str(os.path.dirname(os.path.abspath(__file__))) + '\\' +
                         '.cache-' + username)
        else:
            cache = '.cache-' + username

        token = spotipy.util.prompt_for_user_token(username,scope,
        client_id='b7fc438dd1494d998c4eacfc3a78e0c4',
        client_secret=secret,
        redirect_uri='http://localhost:8888/callback',
        cache_path=cache)
    except: # catches all 'bad request' errors from spotify
        print(color('Incorrect username or passphrase.  Please check your spelling ' +
                    'and try again.',LTRED))
        sys.exit()

    # it would be unusual to fail here, but it's theoretically possible
    if not token:
        print(color('Spotify connection failed. Please contact the administrator at ' +
                    'rebecca.riley@uci.edu with a screenshot of the error.',LTRED))
        sys.exit()

    # token is good and spotify contact was successful
    spotify = spotipy.Spotify(auth=token)
    print(color('Contact successful.',GREEN))
    print()

    if PLAYLISTS: # user wants only playlists or both playlists & liked songs
        # prompt for cutoff date, if desired
        print('>> Playlist options >>')
        print('If you only want data for playlists updated ' +
              color('after a certain date',BLUE) + ', enter that')
        print('here.  Please type the date after which you want updated playlists in ' +
              color('mm-dd-yyyy',BLUE))
        print('format (e.g. 01-01-2020).  If you want data for ' +
              color('all your playlists',GREEN) + ', just press')
        cutoff_date = parse_date_entry(input(color('enter',GREEN) + ': '))
        print()

        # prompt for cutoff date within playlists
        print('By default, No Scrubs will output the ' + color('full playlist ',GREEN) +
              'if at least one song has ')
        print('been added since the cutoff date.  If you only want data for songs added '
              + color('after ',LTYLLW))
        new_songs_only = (input(color('the cutoff date',LTYLLW) + ', type ' +
                          color('\'new\'',LTYLLW) +'.  Otherwise, press ' +
                          color('enter',GREEN) + ': ') == 'new')
        print()

        # prompt for which playlists to process -- created by just you or anyone?
        print('By default, No Scrubs will only output data for ' +
              color('playlists created by you',GREEN) + '.  If')
        print('you want data for ' + color('all your playlists',LTRED) +
              ', including those that you follow but did')
        created_by_others = (input('not create, type '+ color('\'yes\'',LTRED) +
                        '.  Otherwise, press ' + color('enter',GREEN) + ': ') == 'yes')
        print()

        # grab first batch of playlists (max batch size = 50)
        playlists = spotify.current_user_playlists()

        # loop through playlists while there are still playlists to be processed
        playlists_remaining = True
        while playlists_remaining:

            # cycle through batch of playlists
            for playlist in playlists['items']:

                # skip playlists owned/created by others unless requested otherwise
                if (not created_by_others) and (playlist['owner']['id'] != username):
                    print(color(('...Skipping ' + playlist['name'] +
                          ' (owned by ' + playlist['owner']['id'] + ')'), BLUE))
                    print()
                    continue

                # skip playlists that have no songs added after cutoff date
                pylst = spotify.user_playlist(username,playlist['id'],'tracks')
                no_songs_after_cutoff_date = True

                # search playlist for track added since cutoff date
                for track in pylst['tracks']['items']:
                    if add_date(track['added_at']) > cutoff_date:
                        no_songs_after_cutoff_date = False

                if no_songs_after_cutoff_date:
                    print(color(('...Skipping ' + playlist['name'] +
                          ' (no songs added after ' + str(cutoff_date) + ')'),BLUE))
                    print()
                    continue

                # otherwise, playlist is eligible to be processed
                print('...Processing ' + playlist['name'])
                process_list(pylst['tracks'],playlist['name'],spotify,cutoff_date,
                             new_songs_only)

            # check if there are more playlists remaining.  if so, loop continues.
            playlists_remaining = playlists['next'] # gives link or 'None'
            if playlists_remaining: # update playlists with new batch
                playlists = spotify.next(playlists)

    if LIKED: # user wants only liked songs or both liked songs & playlists
        # prompt for cutoff date, if desired
        print('>> Liked songs options >>')
        print('If you only want data for liked songs added ' +
              color('after a certain date',BLUE) + ', enter that')
        print('here.  Please type the date after which you want added songs in ' +
              color('mm-dd-yyyy',BLUE))
        print('format (e.g. 01-01-2020).  If you want data for ' +
              color('all your liked songs',GREEN) + ', just press')
        cutoff_date = parse_date_entry(input(color('enter',GREEN) + ': '))
        print()

        # process list of liked songs
        print('...Processing Liked Songs')
        process_list(spotify.current_user_saved_tracks(),'Liked Songs',spotify,
                     cutoff_date,True)
        print()


    # all processing successfully completed
    print(color('Done!',GREEN))

    # fun stuff :)
    print('Thanks for using this script to build your music library!  If you have any ')
    print('further questions, comments, or concerns, you can email me at ')
    print('rebecca.riley@uci.edu.')
    print()

    # short term top artists
    print('As a parting gift, check out your top artists this month:')
    for artist in spotify.current_user_top_artists(time_range='short_term')['items']:
        print(artist['name'])
    print()

    # long term top artists
    print('...and of all time!')
    for artist in spotify.current_user_top_artists(time_range='long_term')['items']:
        print(artist['name'])
    print()

    print('Hope to see you back soon!  Remember, you can use the cutoff date feature')
    print('to aggregate only recently added tracks to continue growing your collection')
    print('in the future.  Ciao!  -RR')

    # keep windows terminal alive while running
    if platform.system() == 'Windows':
        print()
        input('Press any key to exit.')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('An unexpected error has occured.  Please contact me at rebecca.riley@uci.edu')
        print('and include the following error message:')
        print(e)
