# MusicHashTable.py started on 6/25/2018
# Authors: Cormac Dacker, Marilyn Groppe
# Version # 0.0.8

import csv
import glob
import os
import urllib.request

from bs4 import BeautifulSoup


def force_to_unicode(text):
    return text if isinstance(text, bytes) else text.encode('utf8')


class User:
    def __init__(self, BASEPATH, code):
        self.BASEPATH = BASEPATH
        self.code = code

        self.MusicPath = self.BASEPATH + 'Music/'
        self.NewPath = self.MusicPath + 'New/'
        self.OldPath = self.MusicPath + 'Old/'
        self.CurrentPath = self.MusicPath + 'Current/'
        self.TestPath = self.BASEPATH + 'Test/'


user = User('', '')
Path = user.BASEPATH
FileName = "MusicData.csv"
NewMusicPath = user.NewPath
CurrentMusicPath = user.CurrentPath
OldMusicPath = user.OldPath
TestMusicPath = user.TestPath
DEVELOPER_KEY = "AIzaSyDsEUDbBKzBE6HS96PJ7FQpS5a8qfEV3Sk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
Fnames = []

music = {}


# A class used to create music file objects
class Data:
    # Constructer
    def __init__(self, Title="", Url="", Artist="", likes=0, dislikes=0, views=0,
                 used=False):  # used, artist, tempo, etc
        self.Title = force_to_unicode(Title).decode('utf8')
        self.Url = Url
        self.Artist = force_to_unicode(Artist).decode('utf8')
        self.likes = likes
        self.dislikes = dislikes
        self.views = views
        self.used = used
        try:
            self.pos = hash(Artist)%(1000)
        except ZeroDivisionError:
            self.pos = 0

    # toString()
    def __str__(self):
        out = "{0},{1},{2},{3},{4},{5},{6},{7}".format(
            self.Artist,
            self.Title,
            self.Url,
            self.likes,
            self.dislikes,
            self.views,
            self.used,
            self.pos
        )
        return out

    def __eq__(self, other):
        if isinstance(other, Data):
            if other.Url == self.Url:
                return True
            else:
                return False
        else:
            return False

music['Khalid'] = Data("Location", "by3yRdlQvzs", "Khalid", 1900000, 80000, 297339999)
music['Flight of the Conchords'] = Data("Robots", "BNC61-OOPdA", "Flight of the Conchords", 4100, 59, 559964)
music['Tessa Violet'] = Data("Crush", "SiAuAJBZuGs", "Tessa Violet", 111000, 4300, 1969889)
music['gnash'] = Data("home", "bYBLt_1HcQE", "gnash", 120000, 20000, 20243102)


# Reads through data and outputs it as array eg out[row]
def readData():
    with open(FileName, "r", newline='') as csvfile:
        DataReader = csv.reader(csvfile, delimiter="\n", quotechar=" ",
                                quoting=csv.QUOTE_NONNUMERIC)
        out = []
        for Item in DataReader:
            out.append(Item)
        csvfile.close()
        return out


# Saves Header dataList into csv file
# TO TEST
# DataList is a LIST object
def saveHeader(dataList):
    with open(FileName, 'w', newline='\n') as csvfile:
        DataWriter = csv.writer(csvfile, delimiter="\n", quotechar=" ",
                                quoting=csv.QUOTE_NONNUMERIC)
        DataWriter.writerow([dataList])
        csvfile.close()


# Saves dataList into csv file
# TO TEST
# DataList is a dictionary
def saveData(dataList):
    with open(FileName, 'a', newline='') as csvfile:
        DataWriter = csv.writer(csvfile, delimiter="\n", quotechar=" ",
                                quoting=csv.QUOTE_NONNUMERIC)
        dd = []
        for key in dataList.keys():
            val = dataList.get(key)
            string = val.__str__()
            el = [string]
            dd.append(el)
        try:
            DataWriter.writerows(dd)
        except UnicodeEncodeError as e:
            error(e)
            pass
        csvfile.close()


# appends dataList into csv file
def appendData(song):
    with open(FileName, 'a', newline='') as csvfile:
        DataWriter = csv.writer(csvfile, delimiter="\n", quotechar=" ",
                                quoting=csv.QUOTE_NONNUMERIC)
        try:
            music[song.Artist] = song
            DataWriter.writerow([song.__str__()])
        except TypeError and AttributeError as e:
            error(e)
        csvfile.close()


# TO TEST
def clear():
    with open(FileName, 'w', newline='\n') as csvfile:
        csvfile.close()


# TO TEST
def toCurrent(musicFile, setting):
    if str(setting) == '-1':  # if in testing mode
        path = TestMusicPath
    else:
        path = Path

    os.rename(path + musicFile, CurrentMusicPath + musicFile)


# def cleanCSV(self):


# TO TEST
# gets views, likes and dislikes
def getStats(url):
    soup = BeautifulSoup(urllib.request.urlopen(url).read().decode
                         ('utf-8', 'ignore'), 'html.parser')
    ratings = soup.find_all('button')
    likes = ratings[24]
    dislikes = ratings[26]
    likes = str(likes).split('>')
    likes = likes[likes.__len__() - 3]
    likes = likes[:likes.__len__() - 6]
    if likes == "Statistics":  # if there is an additional button present
        likes = ratings[25]
        dislikes = ratings[27]
        likes = str(likes).split('>')
        likes = likes[likes.__len__() - 3]
        likes = likes[:likes.__len__() - 6]
        dislikes = str(dislikes).split('>')
        dislikes = dislikes[dislikes.__len__() - 3]
        dislikes = dislikes[:dislikes.__len__() - 6]
    elif likes == "Transcript":
        likes = ratings[26]
        dislikes = ratings[28]
        likes = str(likes).split('>')
        likes = likes[likes.__len__() - 3]
        likes = likes[:likes.__len__() - 6]
        dislikes = str(dislikes).split('>')
        dislikes = dislikes[dislikes.__len__() - 3]
        dislikes = dislikes[:dislikes.__len__() - 6]
    else:
        dislikes = str(dislikes).split('>')
        dislikes = dislikes[dislikes.__len__() - 3]
        dislikes = dislikes[:dislikes.__len__() - 6]
    Views = soup.find_all('div', class_="watch-view-count")
    views = Views[0]
    views = (str(views).split('>'))[1]
    views = views[:views.__len__() - 11]
    if (str(views) == "No"):  # if no views
        views = '0'
    try:
        return [int(removeCommas(likes)), int(removeCommas(dislikes)), int(removeCommas(views))]
    except ValueError and AttributeError as e:
        error(e)


def printRows(arr):
    count = 0
    while count < arr.__len__():
        try:
            print("[" + str(count) + "]" + str(arr[count]))
        except KeyError as e:
            error(e)
            break
        count += 1


def removeCommas(string):
    out = ''.join(string.split(","))
    return out


# prints error message
def error(errorMessage):
    print(">ERROR:\t" + str(errorMessage))


# get's the info of the track (url, artist, title)
def getTrackInfo(file):
    url = file[file.__len__() - 15:file.__len__() - 4]
    fx = file.split('-')
    artist = removeCommas(fx[0])
    title = removeCommas(fx[1])
    return [artist, title, url]


# TODO convert CSV to Dict
def convertCSVtoDict():
    dataList = readData()
    dic = {}
    index = 1
    while index < dataList.__len__():  # dataList to dict
        artist = (str(dataList[index]).split(',')[0])
        artist = artist[2:]
        dic[artist] = dataList[index]
        index += 1
    return dic


# control center for MusicHashTable.py
def updateCSV(setting):
    if setting == -1:  # if testing mode
        path = TestMusicPath
    else:
        path = NewMusicPath

    ytPath = 'https://www.youtube.com/watch?v='
    # grabbing all the files in the set path
    musicFileList = glob.glob(path + '*.mp3')
    # creating a dictionary and shoving those in there
    music = convertCSVtoDict()
    clear()
    # Setting up the basic CSV
    saveHeader(dataList="'ARTIST', 'TITLE', 'URL', 'LIKES', 'DISLIKES', 'VIEWS', 'USED?'")
    for musicFile in musicFileList:
        file = musicFile[path.__len__():]
        try:
            info = getTrackInfo(file)  # (artist, title, url)
            data = getStats(ytPath + info[2])  # (likes, dislikes, views)
        except urllib.error.HTTPError and ValueError as e:
            error(str(e) + ' ' + file)
            continue
        entry = Data(force_to_unicode(info[1]).decode('utf8'),
                     force_to_unicode(info[2]).decode('utf8'),
                     force_to_unicode(info[0]).decode('utf8'), data[0], data[1], data[2], False)
        if music.get(info[0]) != None:  # if there is an existing entry under the same artist
            song = str(music.get(info[0])).split(',')[1]  # get the song from the entry
            if (song == info[1]):  # if the song names match
                if setting != -1:  # if not a test
                    print(">FILE DUPLICATE FOUND:\t" + str(musicFile)[10:])
                    os.remove(musicFile)
                continue  # determine tracks to be the same, add no entry
            # TODO iterate through songs by artist (key) to ensure track does not already exist
            else:  # if new track under existing artist
                print(">NEW ENTRY UNDER:\t" + info[0])
                # TODO double hash the data
        music[info[0]] = entry
        if setting != -1:  # if not a test
            toCurrent(musicFile, 0)  # send track to /Current/
            print(">NEW ENTRY:\t\t" + info[0] + ' - ' + info[1] + ' ' + info[2])
    saveData(dataList=music)
    if setting != -1:  # if not a test
        print(">FILE UPDATED:\t" + str(FileName) + " in /Music/")


def checkResults(test, desiredResults, results):
    test += ":"
    if test.__len__() <= 9:
        test += '\t'
    if test.__len__() <= 13:
        test += '\t'
    if test.__len__() <= 16:
        test += '\t'
    if test.__len__() < 19:
        test += '\t'
    if str(results) == str(desiredResults):
        print(">TEST " + test + "\tPASS")
    else:
        print(">TEST " + test + "\tFAIL")
        print("\tExpected Output: " + str(desiredResults))
        print("\tOutput Received: " + str(results))


def runTests():
    print(">COMMENCE TESTING...")
    results = None  # stores result of each test
    dic = convertCSVtoDict()  # stored so that info is not lost
    # TEST readData()
    desiredResult = []  # stores desired result of each test
    clear()
    try:
        results = readData()
    except TypeError and ValueError and FileNotFoundError as e:
        error(str(e))
        pass
    checkResults("readData()", desiredResult, results)

    # TEST saveHeader()
    desiredResult = "[\"['ARTIST', 'TITLE', 'URL', 'HASH', 'LIKES', 'DISLIKES', 'VIEWS', 'USED?']\"]"
    try:
        saveHeader(dataList=['ARTIST', 'TITLE', 'URL', 'HASH', 'LIKES', 'DISLIKES', 'VIEWS', 'USED?'])  # Test
        results = str(readData()[0])  # gather results
    except TypeError and ValueError as e:
        error(str(e))
        pass
    checkResults('saveHeader()', desiredResult, results)

    # TEST saveData()
    desiredResult = "[['Khalid,Location,by3yRdlQvzs,1900000,80000,297339999,False'], " \
                    "['Flight of the Conchords,Robots,BNC61-OOPdA,4100,59,559964,False']," \
                    " ['Tessa Violet,Crush,SiAuAJBZuGs,111000,4300,1969889,False'], " \
                    "['gnash,home,bYBLt_1HcQE,120000,20000,20243102,False']]"
    try:
        saveData(music)
        results = str(readData()[1:])  # gather results
    except ValueError and AttributeError as e:
        error(str(e))
        pass
    checkResults("saveData()", desiredResult, results)

    # TEST appendData()
    desiredResult = "[['alt-j,in cold blood,rP0uuI80wuY,74000,2000,9059467,False']]"
    try:
        clear()
        appendData(Data("in cold blood", "rP0uuI80wuY", "alt-j", 74000, 2000, 9059467, False))
        results = str(readData()[readData().__len__() - 1:])
    except TypeError and ValueError as e:
        error(str(e))
        pass
    checkResults("appendData()", desiredResult, results)

    # TEST getStats()
    desiredResult = [0, 0, 0]
    ytPath = 'https://www.youtube.com/watch?v='
    try:
        results = getStats(ytPath + "6cwBLBCehGg")
    except TypeError as e:
        error(str(e))
        pass
    checkResults("getStats()", desiredResult, results)

    # TEST clear()
    desiredResult = 0
    try:
        clear()
        results = readData().__len__()
    except ValueError as e:
        error(str(e))
        pass
    checkResults("clear()", desiredResult, results)

    # TEST toCurrent()
    desiredResult = "['Music/Current\\\\Test 0-title-6cwBLBCehGg.mp3', " \
                    "'Music/Current\\\\Test 1-title-6cwBLBCehGg.mp3', " \
                    "'Music/Current\\\\Test 2-title-6cwBLBCehGg.mp3', " \
                    "'Music/Current\\\\Test 3-title-6cwBLBCehGg.mp3', " \
                    "'Music/Current\\\\Test 4-title-6cwBLBCehGg.mp3']"
    try:
        musicList = glob.glob(TestMusicPath + '*.mp3')  # gather a list of tracks in /Test/
        for track in musicList:
            if str(track.split(' ')[0])[-4:] == "Test":
                track = track[TestMusicPath.__len__():]
                toCurrent(track, '-1')

        results = glob.glob(CurrentMusicPath + '*.mp3')  # gather a list of tracks in /Music/Current/
        for track in results:  # return Test*.mp3 to /Test/
            track = track[CurrentMusicPath.__len__():]
            if track.split(' ')[0] == "Test":

                os.rename(CurrentMusicPath + track, TestMusicPath + track)
    except TypeError and FileNotFoundError and AttributeError and OSError as e:
        error(str(e))
        pass
    checkResults("toCurrent()", desiredResult, results)

    # TEST updateCSV()
    desiredResult = str([["'ARTIST', 'TITLE', 'URL', 'LIKES', 'DISLIKES', 'VIEWS', 'USED?'"],
                         ['Test 0,title,6cwBLBCehGg,0,0,0,False'],
                         ['Test 1,title,6cwBLBCehGg,0,0,0,False'],
                         ['Test 2,title,6cwBLBCehGg,0,0,0,False'],
                         ['Test 3,title,6cwBLBCehGg,0,0,0,False'],
                         ['Test 4,title,6cwBLBCehGg,0,0,0,False']])
    try:
        clear()
        updateCSV(-1)
        results = readData()
        clear()
    except TypeError as e:
        error(str(e))
        pass
    checkResults("updateCSV()", desiredResult, results)

    saveData(dic)  # return original data to csv


if __name__ == "__main__":
    print(error("Please run from main.py"))
