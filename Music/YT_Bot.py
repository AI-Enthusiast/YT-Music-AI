from __future__ import unicode_literals

import glob
import os

import youtube_dl
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

liveVidKeyWords = ["24/7", "radio", "mix", "live", "2018", "lofi", "lo-fi", "songs", "#"]
CurrentPath = 'C:/Users/corma/Summer2018/Project/Music/'

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyDsEUDbBKzBE6HS96PJ7FQpS5a8qfEV3Sk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def isLive(title=[]):
    for i in liveVidKeyWords:
        for word in title:
            if i == word:
                return True
    return False


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
    vids = {}
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        title = search_result["snippet"]["title"]
        title.lower()
        if isLive(title.split(" " or "　" or "/" or "[" or "]")):  # filters out live streams
            pass
        elif search_result["id"]["kind"] == "youtube#video":
            vidID = search_result["id"]["videoId"]
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                       search_result["id"]["videoId"]))
            vids.append("%s (%s)" % (search_result["snippet"]["title"]))
            vids[search_result["id"]["videoId"]] = search_result["snippet"]["title"]
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                         search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                          search_result["id"]["playlistId"]))

    print("Videos:\n", "\n".join(videos), "\n")
    print("Channels:\n", "\n".join(channels), "\n")
    print("Playlists:\n", "\n".join(playlists), "\n")
    s = ','.join(vids.keys())


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Downloading ...')


def toNew(filename):
    NewMusicPath = 'C:/Users/corma/Summer2018/Project/Music/New/'
    os.rename(CurrentPath + filename, NewMusicPath + filename)
    print("Moving File: " + filename)


def doneConvertion():
    arr = glob.glob(CurrentPath + '*.mp3')
    for i in arr:
        file = i[40:]
        toNew(file)


def convertVid(url):
    videoURL = "https://www.youtube.com/watch?v=" + url
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videoURL])
    doneConvertion()


def convertPlaylist(url):
    playlistURL = "https://www.youtube.com/playlist?list=" + url
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlistURL])

    doneConvertion()


def convertChannel(url):
    channelURL = "https://www.youtube.com/channel/" + url
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([channelURL])
    doneConvertion()


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
    temp = [None, None]
    argparser.add_argument("--q", help="Search term", default=temp[1])
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()
    while True:
        com = input('>>').split()
        if len(com) == 0:  # if there is not input end program
            print("\n YT_Bot.py has been Terminated...")
            doneConvertion()
            break
        elif len(com) < 2 and str(com[0]) != "help":  # if there is not enough input
            print("ERROR: Insufficient arguments. For help type 'help'")
        elif com[0] == "v":  # if video v
            # try:
            convertVid(com[1])
            # except Error as e:
            # print("ERROR: " + e)
        elif com[0] == "p":  # if playlist p
            # #try:
            convertPlaylist(com[1])
            # except Error as e:
            # print("ERROR: " + e)
        elif com[0] == "c":  # if channel c
            # try:
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
