# main.py started on 6/30/2018
# Authors: Marilyn Groppe, Cormac Dacker
# Version # 0.0.8
from __future__ import unicode_literals

import os

from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

from Music import MusicHashTable
from Music import YT_Bot

codes = {'mg': 'C:/Users/mjgro/Documents/GitHub/YT-Music-AI', 'cd': 'C:/Users/corma/Documents/GitHub/YT-Music-AI'}
user = MusicHashTable.User('', '')
if __name__ == "__main__":
    if not os.path.isfile(MusicHashTable.FileName):
        MusicHashTable.error("'MusicData.csv' could not be found")
        MusicHashTable.clear()
        print(">FILE CREATED: MusicData.csv")

    print('Insert the path to the directory on your computer that '
          'leads to the directory that contains your \'New\' \n\tand \'Current\' folders, or your initials\n')
    path = input('>>')

    while True:
        if user.BASEPATH == '':
            if codes.keys().__contains__(path):
                user = MusicHashTable.User(codes.get(path), path)
                YT_Bot.user = user
                MusicHashTable.user = user
                if path == "cd":
                    print("Welcome Cormac :)")
                elif path == "cd":
                    print("Welcome Marilyn :)")
            elif (len(path) < 1):
                l = input('That didn\'t work... Insert the path to the directory on your computer that '
                          'leads to the directory that contains your \'New\' and \'Current\' folders, in one string.\n')
                if (len(l) < 1):
                    YT_Bot.doneConvertion()
                    quit()
                else:
                    print('>SAVING PATH...\n')
                    user = MusicHashTable.User(l, 'nu')
                    YT_Bot.user = user
                    MusicHashTable.user = user
            else:
                print('>SAVING PATH...\n')
                user = MusicHashTable.User(path, 'nu')
                YT_Bot.user = user
                MusicHashTable.user = user
        else:
            com = input('>>').split()
            if len(com) == 0:  # if there is not input end program
                print("\n YT_Bot.py has been Terminated...")
                YT_Bot.doneConvertion()
                break
            elif com[0] == "test":  # if wanting to run test for MusicHashTable.py
                MusicHashTable.runTests()
            elif com[0] == "read":  # if wanting to read MusicData.csv
                MusicHashTable.printRows(MusicHashTable.readData())
            elif com[0] == "clear":  # if wishing to clear of create a new instance of MusicData.csv
                MusicHashTable.clear()
            elif com[0] == "done":  # if wishing to clear BASEPATH of *.mp3 files
                YT_Bot.doneConvertion()
            elif com[0] == "v":  # if video v
                try:
                    YT_Bot.downloading()
                    YT_Bot.convertVid(com[1])
                except YT_Bot.youtube_dl.utils.PostProcessingError and YT_Bot.youtube_dl.utils.DownloadError as e:
                    YT_Bot.error(e)
            elif com[0] == "p":  # if playlist p
                try:
                    YT_Bot.downloading()
                    YT_Bot.convertPlaylist(com[1])
                except YT_Bot.youtube_dl.utils.PostProcessingError and YT_Bot.youtube_dl.utils.DownloadError as e:
                    YT_Bot.error(e)
            elif com[0] == "c":  # if channel c
                try:
                    YT_Bot.downloading()
                    YT_Bot.convertChannel(com[1])
                except YT_Bot.youtube_dl.utils.PostProcessingError and YT_Bot.youtube_dl.utils.DownloadError as e:
                    YT_Bot.error(e)
            elif com[0] == "s":  # if search s
                argparser.add_argument("--q", help="Search term", default=path[1])
                argparser.add_argument("--max-results", help="Max results", default=25)
                argparser.set_defaults(q=com[1])
                args = argparser.parse_args()
                try:
                    YT_Bot.youtube_search(args)
                except HttpError as e:
                    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            # elif com[0] == "auto":
            # enter automatic stage
            else:
                print("Please type 's'(for search), 'v'(for video), 'p'(for playlist), or 'c'(for channel)"
                      "\nfollowed by the end url or the search term."
                      "\n\tE.G: 'v LGeaZwunIFk' or 's lofi'"
                      "\nOr: 'done'(transfers *.mp3 to /New/ for processing), 'read'(reads MusicData.csv),"
                      "\n'clear'(clears MusicData.csv), or 'test'(run tests)")
