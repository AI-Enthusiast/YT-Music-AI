# YT_Bot.py started on 6/25/2018
# Authors: Cormac Dacker, Marilyn Groppe
# Version # 0.0.8

from __future__ import unicode_literals

import glob
import os

import youtube_dl
from googleapiclient.discovery import build

from Music import MusicHashTable

# different words to identify mixes and livestreams
liveVidKeyWords = ["24/7", "radio", "mix", "live", "2018", "lofi", "lo-fi", "songs", "#", 'compilation', 'hour']
user = MusicHashTable.User('', '')
BASEPATH = user.BASEPATH
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyDsEUDbBKzBE6HS96PJ7FQpS5a8qfEV3Sk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


# A function to check the list to predict if its a live video
# params: list of title words
# returns a Boolean depicting whether it is assumed to be live or not

def isLive(title):
    for i in liveVidKeyWords:
        for word in title:
            if i == word:
                return True
    return False


# A function to search videos, channels, and playlists from the console
# params: options for the search itself
# returns: N/A
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


# A class to aide in importing -- logs errors
class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, errorMessage):
        print(str(errorMessage))


def printRows(arr):
    count = 0
    while count < arr.__len__():
        print("[" + str(count) + "]" + str(arr[count]))
        count += 1


# A function to show progress in downloads
def my_hook(d):
    if d['status'] == 'finished':
        print('>CONVERTING...')


# A function to move files from general folder to New folder
def toNew(filename):
    try:
        os.rename(user.BASEPATH + filename, str(user.NewPath + filename).replace('\'', ''))
        print(">FILE MOVED:\t" + str(filename) + " to /Music/New/")
    except FileExistsError:  # if file already exists
        raise FileExistsError
    except FileNotFoundError as e:  # if the file cannot be found
        error(e)
    except PermissionError:  # if the file is currently being accessed
        pass


# Moves all files done converting to New
def doneConversion():
    musicList = glob.glob(user.BASEPATH + '*.mp3')
    deadList = glob.glob(user.BASEPATH + '*.part') # abandoned parts of yt videos
    deleted = 0
    for track in musicList:
        file = track[str(user.BASEPATH).__len__():]
        try:
            toNew(file)
        except FileExistsError:
            error(str(track) + ' already exists')
            os.remove(track)
            deleted +=1
    for track in deadList:
        try:
            os.remove(track)
        except PermissionError as e:
            error(e)
            continue
    print('>FILES MOVED:\t' + str((musicList.__len__() - deleted)))
    print('>FILES REMOVED:\t' + str(deleted + str(deadList).__len__()))


def convertVid(url):
    videoURL = "https://www.youtube.com/watch?v=" + url
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videoURL])
    doneConversion()


# Converts playlists using youtube-dl library
def convertPlaylist(url):
    playlistURL = "https://www.youtube.com/playlist?list=" + url
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlistURL])
    doneConversion()


# Converts channels using youtube-dl library
def convertChannel(url):
    channelURL = "https://www.youtube.com/channel/" + url
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([channelURL])
    doneConversion()


# prints downloading. Purely OCD aesthetic
def downloading():
    print(">DOWNLOADING...")


# prints error message
def error(errorMessage):
    print(">ERROR:\t" + str(errorMessage))


# options needed for youtube-dl library
ydl_opts = {
    'format': 'bestaudio/best', 'ignorerrors': True,
    'max_filesize': 10*2**20,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(), 'progress_hooks': [my_hook]
}

if __name__ == "__main__":
    error("Please run from main.py")
