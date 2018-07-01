# main.py started on 6/30/2018
# Authors: Marilyn Groppe, Cormac Dacker
# Vertion# 0.0.5
from __future__ import unicode_literals

from Music import MusicHashTable

import youtube_dl
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import csv
import glob
import os
import urllib.request
from Music import YT_Bot
from bs4 import BeautifulSoup

codes = {'mg': 'C:/Users/mjgro/Documents/GitHub/YT-Music-AI', 'cd': 'C:/Users/corma/Documents/GitHub/YT-Music-AI'}
user = MusicHashTable.User('', '')
if __name__ == "__main__":
    print('Insert the path to the directory on your computer that '
          'leads to the directory that contains your \'New\' \n\tand \'Current\' folders, or your initials\n')
    path = input('>>')
    argparser.add_argument("--q", help="Search term", default=path[1])
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()
    while True:
        if user.BASEPATH == '':
            if codes.keys().__contains__(path):
                user = MusicHashTable.User(codes.get(path), path)
                YT_Bot.user = user
                MusicHashTable.user = user
            elif (len(path) < 1):
                l = input('That didn\'t work... Insert the path to the directory on your computer that '
                          'leads to the directory that contains your \'New\' and \'Current\' folders, in one string.\n')
                if (len(l) < 1):
                    YT_Bot.doneConvertion()
                    quit()
                else:
                    print('Saving your path...\n')
                    user = MusicHashTable.User(l, 'nu')
                    YT_Bot.user = user
                    MusicHashTable.user = user
            else:
                print('Saving your path...\n')
                user = MusicHashTable.User(path, 'nu')
                YT_Bot.user = user
                MusicHashTable.user = user
        else:
            com = input('>>').split()
            if len(com) == 0:  # if there is not input end program
                print("\n YT_Bot.py has been Terminated...")
                YT_Bot.doneConvertion()
                break
            elif len(com) < 2 and str(com[0]) != "help":  # if there is not enough input
                print("ERROR: Insufficient arguments. For help type 'help'")
            elif com[0] == "v":  # if video
                # try:
                YT_Bot.doneConvertion()
                YT_Bot.convertVid(com[1])
            elif com[0] == "p":  # if playlist p
                # try:
                YT_Bot.convertPlaylist(com[1])
                YT_Bot.downloading()
                # except Error as e:
                # print("ERROR: " + e)
            elif com[0] == "c":  # if channel c
                # try:
                YT_Bot.convertChannel(com[1])
                YT_Bot.downloading()
                # except Error as e:
                # print("ERROR: " + e)
            elif com[0] == "s":  # if search s
                argparser.set_defaults(q=com[1])
                args = argparser.parse_args()
                try:
                    YT_Bot.youtube_search(args)
                except HttpError as e:
                    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            elif com[0] == "updateCSV":
                MusicHashTable.updateCSV()
            elif com[0] == "runTests":
                MusicHashTable.runTests()
            # elif com[0] == "auto":
            # enter automatic stage
            else:
                print("Please type 's'(for search), 'v'(for video), 'p'(for playlist), "
                      "or 'c'(for channel) followed by the end url or the search term. "
                      "\n\tE.G: 'v LGeaZwunIFk' or 's lofi'")
