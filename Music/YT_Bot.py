# YT_Bot.py started on 6/25/2018
# Authors: Cormac Dacker, Marilyn Groppe
# Vertion# 0.0.6

from __future__ import unicode_literals

import glob
import os

import youtube_dl
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from Music import MusicHashTable

#different words to identify mixes and livestreams
liveVidKeyWords = ["24/7", "radio", "mix", "live", "2018", "lofi", "lo-fi", "songs", "#"]
user = MusicHashTable.User('', '')
BASEPATH = user.BASEPATH
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyDsEUDbBKzBE6HS96PJ7FQpS5a8qfEV3Sk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


#A function to check the list to predict if its a live vide
#params: list of title words
#returns a Boolean depicting whether it is assumed to be live or not

def isLive(title=[]):
    for i in liveVidKeyWords:
        for word in title:
            if i == word:
                return True
    return False

#A function to search videos, channels, and playlists from the console
#params: options for the search itself
#returns: N/A
def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results
    ).execute()

    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        title = search_result["snippet"]["title"]
        title.lower()
        if isLive(title.split(" " or "　" or "/" or "[" or "]" or "\u3000")):  # filters out live streams
            pass
        elif search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                       search_result["id"]["videoId"]))
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                         search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                          search_result["id"]["playlistId"]))

    print("Videos:\n", "\n".join(videos), "\n")
    print("Channels:\n", "\n".join(channels), "\n")
    print("Playlists:\n", "\n".join(playlists), "\n")

#A class to aide in importing -- logs errors
class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

#A function to show progress in downloads
def my_hook(d):
    if d['status'] == 'finished':
        print('>CONVERTING...')

#A function to move files from general folder to New folder
def toNew(filename):
    os.rename(user.MusicPath + filename, user.NewPath + filename)
    print("Moved File: " + filename)

#Moves all files done converting to New
def doneConvertion():
    arr = glob.glob(user.MusicPath + '*.mp3')
    for i in arr:
        file = i[50:]
        print('Moving ' + file + '...')
        toNew(file)
        print(file)


def convertVid(url):
    videoURL = "https://www.youtube.com/watch?v=" + url
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videoURL])
    doneConvertion()

#Converts playlists using youtube-dl library
def convertPlaylist(url):
    playlistURL = "https://www.youtube.com/playlist?list=" + url
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlistURL])
    doneConvertion()

#Converts channels using youtube-dl library
def convertChannel(url):
    channelURL = "https://www.youtube.com/channel/" + url
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([channelURL])
    doneConvertion()


# prints downloading. Purely OCD aesthetic
def downloading():
    print(">DOWNLOADING...")


# prints error message
def error(errorMessage):
    print("ERROR: " + errorMessage)

#options needed for youtube-dl library
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(), 'progress_hooks': [my_hook]
}

if __name__ == "__main__":
    #needed to set up the search opts
    print('Insert the path to the directory on your computer that '
          'leads to the directory that contains your \'New\' \n\tand \'Current\' folders, or your initials\n')
    path = input('>>')
    argparser.add_argument("--q", help="Search term", default=path[1])
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()
    while True:
        if(BASEPATH == ''):
            if (path == 'mg'):
                BASEPATH = 'C:/Users/mjgro/Documents/GitHub/YT-Music-AI'
            elif (path == 'cd'):
                BASEPATH = 'C:/Users/corma/Documents/GitHub/YT-Music-AI'
            elif (len(path) < 1):
                l = input('That didn\'t work... Insert the path to the directory on your computer that '
                          'leads to the directory that contains your \'New\' and \'Current\' folders, in one string.\n')
                if(len(l) < 1):
                    doneConvertion()
                    quit()
                else:
                    print('Saving your path...\n')
                    BASEPATH = l
            else:
                print('Saving your path...\n')
                BASEPATH = path
        else:
            com = input('>>').split()
            if len(com) == 0:  # if there is not input end program
                print("\n YT_Bot.py has been Terminated...")
                doneConvertion()
                break
            elif len(com) < 2 and str(com[0]) != "help":  # if there is not enough input
                print("ERROR: Insufficient arguments. For help type 'help'")
            elif com[0] == "v":  # if video v
                # try:
                downloading()
                convertVid(com[1])
                #    except Error as e:
                #    print("ERROR: " + e)
            elif com[0] == "p":  # if playlist p
                #try:
                downloading()
                convertPlaylist(com[1])
                # except Error as e:
                # print("ERROR: " + e)
            elif com[0] == "c":  # if channel c
                # try:
                downloading()
                convertChannel(com[1])
                # except Error as e:
                # print("ERROR: " + e)
            elif com[0] == "s":  # if search s
                argparser.set_defaults(q=com[1])
                args = argparser.parse_args()
                try:
                    youtube_search(args)
                except HttpError as e:
                    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

            # elif com[0] == "auto":
            # enter automatic stage
            else:
                print("Please type 's'(for search), '>'(for next page), 'v'(for video), 'p'(for playlist), "
                  "or 'c'(for channel) followed by the end url or the search term. "
                  "\n\tE.G: 'v LGeaZwunIFk' or 's lofi'")
