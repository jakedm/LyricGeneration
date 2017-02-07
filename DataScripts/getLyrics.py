#!/usr/bin/python3

import os
import sys
#import numpy
import csv
import requests
import argparse

URL="http://api.musixmatch.com/ws/1.1/"
KEY="5415dac2a9443eb880e54cbaf3d3f1e4"

def getArtist(artist):
    artistSearch_str = URL + "artist.search?q_artist={}&apikey=" + KEY
    artistID = ''

    r = requests.get(artistSearch_str.format('"' + artist + '"'))    
    print(r.status_code)
    rJson = r.json()

    artistList = rJson['message']['body']['artist_list']
    
    if len(artistList) == 0:
        print("Artist {} not found.".format(artist))
        exit(0)

    elif len(artistList) > 1:
        print("Multiple artists found:")
        for i in artistList:
            print("  Name : " + i["artist"]["artist_name"])
            print("    ID : " + str(i["artist"]["artist_id"]))
            print()
        exit(0)

            
    elif len(artistList) == 1:
        i = artistList[0]
        print("Artist " + i["artist"]["artist_name"] + " found.")
        print("  Artist id: " + str(i["artist"]["artist_id"]))
        artistID = str(i["artist"]["artist_id"])

    return artistID
        
def getSong(song, artistID=None, page_size=5):
    trackSearch_str = URL + "track.search?q_track={}&f_lyrics_language=en&format=json&page_size={}&apikey=" + KEY

    if artistID is not None:
        trackSearch_str += "&f_artist_id=" + str(artistID)
    
    r = requests.get(trackSearch_str.format('"' + song + '"', page_size))
    rJson = r.json()
    trackList = rJson['message']['body']['track_list']
    
    if len(trackList) == 0:
        print("Song {} not found.".format(song))
        exit(0)
        
    elif len(trackList) > 1:
        print("Multiple tracks found:")
        for i in trackList:
            print("  Name : " + i['track']["track_name"])
            print("    Artist : " + i['track']["artist_name"])
            print("    ID     : " + str(i['track']["track_id"]))
        exit(0)

    elif len(trackList) == 1:
        i = trackList[0]
        print("  Name : " + i['track']["track_name"])
        print("    Artist : " + i['track']["artist_name"])
        print("    ID     : " + str(i['track']["track_id"]))
        
            
    elif len(artistList) == 1:
        i = artistList[0]
        print("Artist " + i['track']["artist_name"] + " found.")
        print("  Track id: " + i['track']["track_id"])
        trackID = str(i['track']["track_id"])
        lyricsID = str(i['track']["lyrics_id"])
        albumID = str(i['track']["album_id"])

        return trackID, lyricsID, albumID


def getLyrics(songs, songNames, outDir):
    lyricSearch_str = URL + "track.lyrics.get?track_id={}&format=json&apikey=" + KEY
    for s, sname in zip(songs, songNames):
        r = requests.get(lyricSearch.str.format(s))
        rJson = r.json()
        print(rJson)
        lyrics = rJson['body']['lyrics']['lyrics_body']
        if len(lyrics) == 0:
            print("Error: Could not get lyrics for song {} with song id {}.".format(sname, s))
            exit(-1)
        f = open(outDir + '/' + sname + '.txt', 'w')
        f.write(lyrics)
        f.close()
        
    
def getAlbum(artistID, album=None):
    return 1, 2


    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--artist", type=str, help="Artist to search for.")
    parser.add_argument("--artist_id", type=int, help="Specific artist ID.")
    parser.add_argument("-s", "--song", type=str, help="Song name to search for.")
    parser.add_argument("--song_id", type=int, help="Specific song ID.")
    parser.add_argument("-r", "--record", type=str, help="Album/record to search for (Artist must be provided).")
    parser.add_argument("-o", "--output", type=str, required=True, help="Directory to print lyrics to.")
    args = parser.parse_args()

    artist = ''
    album = ''
    song = ''
    artistID = -1
    trackID = -1
    albumID = -1


    print(args.artist)
    print(args.song)

    if args.artist_id:
        artistID = args.artist_id
        
        
    if args.song_id:
        trackID = args.song_id
    
    if not args.artist and not args.song and not args.record:
        if not args.artist_id and not args.song_id:
            print("Error: No search terms given.")
            exit(-1)


            
    if args.artist and artistID == -1:
        artist = args.artist
        artistID = getArtist(artist)
        albumList = getAlbum(artistID)

    
        
    if args.song:
        song = args.song
        if args.artist or (artistID != -1):
            trackID, lyricsID, albumID = getSong(song, artistID)
        else:
            trackID , lyricsID, albumID = getSong(song)

        getLyrics([trackID], [song], args.output)

        
    if args.record:
        if not args.artist:
            print("Error: Artist must be provided.")
            exit(-1)
        
        album = args.record
        albumID, songNames, songIDs = getAlbum(album, artistID)
        getLyrics(songIDs, songNames, args.output)
    

