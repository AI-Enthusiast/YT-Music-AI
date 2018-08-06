# main.py started on 6/30/2018
# Authors: Marilyn Groppe, Cormac Dacker
# Version # 0.0.9
from __future__ import unicode_literals

import os
import unittest
from io import StringIO
from pprint import pprint

from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

from AfterEffects.SourceFiles import AE_Bot as ae
from Music import MusicAI as mai
from Music import MusicHashTable as mh
from Music import YT_Bot as yt
from Test import UnitTests as ut

codes = {'mg': 'C:/Users/mjgro/Documents/GitHub/YT-Music-AI/', 'cd': 'C:/Users/corma/Documents/GitHub/YT-Music-AI/'}


# user = mh.User('', '')


def error(errorMessage):
    print(">ERROR:\t" + str(errorMessage))


if __name__ == "__main__":
    if not os.path.isfile(mh.FileName):
        mh.error("'MusicData.csv' could not be found")
        mh.clear()
        print(">FILE CREATED: 'MusicData.csv' in /Music/")

    argparser.add_argument("--q", help="Search term", default="")
    argparser.add_argument("--max-results", help="Max results", default=25)
    first = True
    while True:
        try:
            if mh.user.BASEPATH == '':
                print('Insert the path to the directory on your computer that '
                      'leads to the directory that contains your \'New\' \n\tand \'Current\' folders, or your initials\n')
                path = input('>>')
                if codes.keys().__contains__(path):
                    user = mh.User(codes.get(path), path)
                    yt.user = user
                    mh.user = user
                    if path == "cd":
                        print("Welcome Cormac :)")
                    elif path == "mg":
                        print("Welcome Marilyn :)")
                    elif len(path) < 1:
                        path = str(input("TERMINATE PROGRAM (Y/N)?: ")).lower()
                        if path == 'y' or path == 'yes':
                            yt.doneConversion()
                            print(">PROGRAM TERMINATED: By user command")
                            quit()
                        else:
                            pass
                    else:
                        print('>SAVING PATH...\n')
                        user = mh.User(path, 'nu')
                        yt.user = user
                        mh.user = user
                else:
                    print('>SAVING PATH...\n')
                    user = mh.User(path, 'nu')
                    yt.user = user
                    mh.user = user
            else:
                user = mh.user
                ut.user = mh.user
                userIN = input('>>').split()
                if first:
                    mh.convertCSVtoDict()
                    first = False
                if len(userIN) == 0:  # if there is not input end program
                    print("\n yt.py has been Terminated...")
                    yt.doneConversion()
                    break
                elif userIN[0] == "test":  # if wanting to run tests
                    print(">COMMENCE TESTING...")
                    dic = mh.convertCSVtoDict()  # stored so that info is not lost
                    stream = StringIO()
                    runner = unittest.TextTestRunner(stream=stream)
                    result = runner.run(unittest.makeSuite(ut.TestHashTable))
                    print('Tests run ', result.testsRun)
                    print('Errors ', result.errors)
                    pprint(result.failures)
                    stream.seek(0)
                    print('Test output\n', stream.read())
                    result = runner.run(unittest.makeSuite(ut.TestMusicHashTable))
                    print('Tests run ', result.testsRun)
                    print('Errors ', result.errors)
                    pprint(result.failures)
                    stream.seek(0)
                    print('Test output\n', stream.read())
                    result = runner.run(unittest.makeSuite(ut.TestYT_Bot))
                    print('Tests run ', result.testsRun)
                    print('Errors ', result.errors)
                    pprint(result.failures)
                    stream.seek(0)
                    print('Test output\n', stream.read())
                    mh.saveData(dic)  # return original data to csv
                elif userIN[0] == "read":  # if wanting to read MusicData.csv
                    mh.printRows(mh.readData())
                elif userIN[0] == "clear":  # if wishing to clear of create a new instance of MusicData.csv
                    mh.clear()
                elif userIN[0] == "done":  # if wishing to clear BASEPATH of *.mp3 files
                    yt.doneConversion()
                elif userIN[0] == "update":  # if wishing to update csv with new music info
                    mh.updateCSV(0)
                elif userIN[0] == "mai":  # if wanting to initiate MusicAI.py
                    mai.train()
                elif userIN[0] == 'ae':
                    ae.setTrack(userIN[1])
                elif userIN[0] == "v":  # if video v
                    try:
                        yt.downloading()
                        yt.convertVid(userIN[1])
                    except yt.youtube_dl.utils.PostProcessingError and yt.youtube_dl.utils.DownloadError as e:
                        yt.error(e)
                elif userIN[0] == "p":  # if playlist p
                    try:
                        yt.downloading()
                        yt.convertPlaylist(userIN[1])
                    except yt.youtube_dl.utils.PostProcessingError and yt.youtube_dl.utils.DownloadError as e:
                        yt.error(e)
                elif userIN[0] == "c":  # if channel c
                    try:
                        yt.downloading()
                        yt.convertChannel(userIN[1])
                    except yt.youtube_dl.utils.PostProcessingError and yt.youtube_dl.utils.DownloadError as e:
                        yt.error(e)
                elif userIN[0] == "s":  # if search s
                    try:
                        argparser.set_defaults(q=userIN[1:])
                        args = argparser.parse_args()
                        yt.youtube_search(args)
                    except HttpError and AttributeError as e:
                        error(e)
                elif userIN[0] == "auto":  # if wanting to enter automatic stage
                    yt.doneConversion()
                    if not mh.isEnoughData():
                        pass
                        # TODO automate music gathering
                    mh.updateCSV(0)
                    mai.train()  # tigger mai
                    # TODO check copyright
                    # TODO trigger wallpaper bot (Waide) to select a background
                    ae.trgr()  # writes info about mp3 so ae has access to the title
                    # TODO trigger AEbot to make video with music and background
                    # TODO compress vid
                    # TODO upload video to youtube
                    # TODO automate acquisition of new data and deletion of old
                    # TODO possibly create a director or a job queue for this so that it never stops
                else:
                    print("Please type 's'(for search), 'v'(for video), 'p'(for playlist), or 'c'(for channel)"
                          "\nfollowed by the end url or the search term."
                          "\n\tE.G: 'v LGeaZwunIFk' or 's lofi'"
                          "\nOr: 'done'(transfers *.mp3 to /New/ for processing), 'read'(reads MusicData.csv),"
                          "\n'clear'(clears MusicData.csv), or 'test'(run tests)")
        except AttributeError as e:
            error(e)
