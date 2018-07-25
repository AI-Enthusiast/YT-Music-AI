# MusicHashTable.py started on 6/25/2018
# Authors: Cormac Dacker, Marilyn Groppe
# Version # 0.0.9

import csv
import glob
import os
import sys
import urllib.error
import urllib.request

from bs4 import BeautifulSoup

from Music import HashTable as ht

IDEAL_SIZE = 3000


# noinspection PyUnresolvedReferences
def force_to_unicode(text):
    '''
    if isinstance(text, str) or isinstance(text, bytes):
        try:
            return text if isinstance(text, bytes) else text.encode('utf-8', 'strict').decode('utf-8', 'strict')
        except UnicodeEncodeError as e:
            error(e)
    else:
        return text
'''
    if isinstance(text, str):
        new = ""
        for char in text:
            if char.isprintable():
                new += char
            else:
                new += " "
        return new
    else:
        return text


def printability(text):
    if isinstance(text, str):
        new = ""
        for char in text:
            if char.isprintable():
                new += char
            else:
                new += " "
        return new
    else:
        return text


def invert(byte):
    if isinstance(byte, bytes):
        return byte.decode('utf-8', 'strict').encode('utf-8', 'strict')
    else:
        return byte


class User:
    def __init__(self, BASEPATH, code):
        self.BASEPATH = BASEPATH
        self.code = code

        self.MusicPath = self.BASEPATH + 'Music\\'
        self.NewPath = self.MusicPath + 'New\\'
        self.OldPath = self.MusicPath + 'Old\\'
        self.CurrentPath = self.MusicPath + 'Current\\'
        self.TestPath = self.BASEPATH + 'Test\\'


cormac = User('C:\\Users\\corma\\Documents\\GitHub\\YT-Music-AI\\', 'cd')
marilyn = User('C:\\Users\\mjgro\\Documents\\GitHub\\YT-Music-AI\\', 'mg')


def setUser():
    if sys.path.__contains__(marilyn.BASEPATH[:-1]):
        user = marilyn
        print("Hello, Marilyn!")

    elif sys.path.__contains__(cormac.BASEPATH[:-1]):
        user = cormac
        print("Hello, Cormac!")

    else:
        user = User(sys.path[0] + '\\', 'nu')
        print("Welcome, New User!")
    return user


user = setUser()
FileName = "MusicData.csv"
NewMusicPath = user.NewPath
CurrentMusicPath = user.CurrentPath
OldMusicPath = user.OldPath
TestMusicPath = user.TestPath
DEVELOPER_KEY = "AIzaSyDsEUDbBKzBE6HS96PJ7FQpS5a8qfEV3Sk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

music = ht.HashTable()


# A class used to create music file objects
class Data:
    # Constructor
    def __init__(self, Title="", Artist="", Url="6cwBLBCehGg", likes=0, dislikes=0, views=0,
                 used=False, likesToTotalRatio=0.0, likeToDislikeRatio=0.0,
                 likeToViewRatio=0.0):  # used, artist, tempo, etc
        self.Title = force_to_unicode(Title)
        self.Url = Url
        self.Artist = force_to_unicode(Artist)
        self.likes = likes
        self.dislikes = dislikes
        self.views = views
        self.used = used
        self.likesToTotalRatio = likesToTotalRatio
        self.likeToDislikeRatio = likeToDislikeRatio
        self.likeToViewRatio = likeToViewRatio

    # toString()
    def __str__(self):
        out = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}".format(
            self.Artist,
            self.Title,
            self.Url,
            self.likes,
            self.dislikes,
            self.views,
            self.used,
            self.likesToTotalRatio,
            self.likeToDislikeRatio,
            self.likeToViewRatio
        )
        return out

    def __eq__(self, other):
        if isinstance(other, Data):
            if other.Url == self.Url and other.Artist == self.Artist and other.Title == self.Title:
                return True
            else:
                return False
        else:
            return False


# Reads through data and outputs it as array eg out[row]
def readData():
    with open(FileName, "r", newline='', encoding='utf8') as csvfile:
        DataReader = csv.reader(csvfile, delimiter="\n", quotechar=" ",
                                quoting=csv.QUOTE_NONNUMERIC)
        out = []
        for Item in DataReader:
            try:
                out.append(invert(Item))
            except UnicodeDecodeError as e:
                error(e)
                pass

        csvfile.close()
        return out


# Saves Header dataList into csv file
# DataList is a LIST object
def saveHeader(dataList):
    with open(FileName, 'w', newline='\n', encoding='utf8') as csvfile:
        DataWriter = csv.writer(csvfile, delimiter="\n", quotechar=" ",
                                quoting=csv.QUOTE_NONNUMERIC)
        DataWriter.writerow([dataList])
        csvfile.close()


# Saves dataList into csv file
# DataList is a HashTable
def saveData(dataList):
    with open(FileName, 'a', newline='', encoding='utf8') as csvfile:
        DataWriter = csv.writer(csvfile, delimiter="\n", quotechar=" ",
                                quoting=csv.QUOTE_NONNUMERIC)
        for val in dataList.values:
            appendData(val)
        csvfile.close()


# appends dataList into csv file
def appendData(song):
    with open(FileName, 'a', newline='', encoding='utf8') as csvfile:
        DataWriter = csv.writer(csvfile, delimiter="\n", quotechar=" ",
                                quoting=csv.QUOTE_NONNUMERIC)
        try:
            song.Artist = force_to_unicode(song.Artist)
            song.Title = force_to_unicode(song.Title)
            DataWriter.writerow([song.__str__()])
        except TypeError and AttributeError and UnicodeEncodeError as e:
            error(e)
        csvfile.close()


def clear():
    with open(FileName, 'w', newline='\n', encoding='utf8') as csvfile:
        csvfile.close()


def toCurrent(musicFile, setting):
    musicFile = str(str(musicFile).split('/')[-1:]).replace('\'', '').split("\\")[-1:]
    n = 2
    if setting == -1:  # if in testing mode
        path = TestMusicPath
        if user.code == 'mg':
            n += 1
        elif user.code == 'cd':
            n += 2
        else:
            n += 0
    else:
        path = NewMusicPath
    musicFile = str(musicFile)[n:-3]
    musicFile.replace('\\', '')
    try:
        os.rename(path + musicFile, CurrentMusicPath + musicFile)
        print(">FILE MOVED:\t" + str(musicFile) + " to /Music/Current/")
    except FileNotFoundError as e:
        error(e)
    except OSError as e:
        error(e)


# gets (likes, dislikes, and views)
def getStats(url):
    try:
        soup = BeautifulSoup(urllib.request.urlopen(url).read().decode
                             ('utf-8', 'strict'), 'html.parser')
    except urllib.error.HTTPError as e:
        error(e)
        return [-1, -1, -1]  # if bad url
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
    elif likes == "Transcript":  # if there is an additional button present
        likes = ratings[26]
        dislikes = ratings[28]
        likes = str(likes).split('>')
        likes = likes[likes.__len__() - 3]
        likes = likes[:likes.__len__() - 6]
        dislikes = str(dislikes).split('>')
        dislikes = dislikes[dislikes.__len__() - 3]
        dislikes = dislikes[:dislikes.__len__() - 6]
    else:  # if normal
        dislikes = str(dislikes).split('>')
        dislikes = dislikes[dislikes.__len__() - 3]
        dislikes = dislikes[:dislikes.__len__() - 6]
    Views = soup.find_all('div', class_="watch-view-count")
    views = Views[0]
    views = (str(views).split('>'))[1]
    views = views[:views.__len__() - 11]
    if str(views) == "No":  # if no views
        views = '0'
    try:
        l = int(removeCommas(likes))
    except ValueError and AttributeError:
        l = 0
        pass
    try:
        d = int(removeCommas(dislikes))
    except ValueError and AttributeError:
        d = 0
        pass
    try:
        v = int(removeCommas(views))
    except ValueError and AttributeError:
        v = 0
        pass
    return [l, d, v]


# gets the info of the track (url, artist, title)
def getTrackInfo(file):
    url = file[file.__len__() - 15:file.__len__() - 4]
    fx = (str(file.split('/')[-1:])[2:-6]).split('-')  # file string manipulation
    artist = removeCommas(fx[0])
    title = removeCommas(fx[1])
    return [str(artist).title(), str(title).title(), url]


# gets the ratios of the track (likesToTotalRatio, likeToDislikeRatio, likeToViewRatio)
def getRatios(data):
    if data.__len__() < 3:
        error("Insufficient args given to getRatios()")
        quit()
    else:
        likes = int(data[0])
        dislikes = int(data[1])
        views = int(data[2])
        if dislikes != 0:
            likeToDislikeRatio = likes / dislikes
        else:
            likeToDislikeRatio = 0
        if views != 0:
            likeToViewRatio = likes / views
        else:
            likeToViewRatio = 0
        if (likes + dislikes) != 0:
            likesToTotalRatio = likes / (likes + dislikes)
        else:
            likesToTotalRatio = 0
        return [float(likesToTotalRatio), float(likeToDislikeRatio), float(likeToViewRatio)]


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


def convertCSVtoDict():
    dataList = readData()
    index = 1
    while index < dataList.__len__():  # dataList to dict
        artist = (str(dataList[index]).split(',')[0])
        artist = artist[2:]
        entry = dataList[index][0].split(",")
        entry = Data(entry[1], entry[0], entry[2], entry[3], entry[4],
                     entry[5], entry[6], entry[7], entry[8], entry[9])
        music.put(artist, entry)
        index += 1


def onlyKeepOne(a, b):
    a.likesToTotalRatio = float(a.likesToTotalRatio)
    b.likesToTotalRatio = float(b.likesToTotalRatio)
    a.likeToViewRatio = float(a.likeToViewRatio)
    b.likeToViewRatio = float(b.likeToViewRatio)
    a.likeToDislikeRatio = float(a.likeToDislikeRatio)
    b.likeToDislikeRatio = float(b.likeToDislikeRatio)
    if a.likesToTotalRatio > b.likesToTotalRatio:
        if a.likeToViewRatio > b.likeToViewRatio:
            if a.likeToDislikeRatio > b.likeToDislikeRatio:
                return a  # a a a
            elif b.likeToDislikeRatio > a.likeToDislikeRatio:
                return a  # a a b
            else:
                return a  # a a =
        elif b.likeToViewRatio > a.likeToViewRatio:
            if a.likeToDislikeRatio > b.likeToDislikeRatio:
                return a  # a b a
            elif b.likeToDislikeRatio > a.likeToDislikeRatio:
                return b  # a b b
            else:
                return a  # a b =
        else:
            if a.likeToDislikeRatio > b.likeToDislikeRatio:
                return a  # a = a
            elif b.likeToDislikeRatio > a.likeToDislikeRatio:
                return a  # a = b
            else:
                return a  # a = =
    elif b.likesToTotalRatio > a.likesToTotalRatio:
        if a.likeToViewRatio > b.likeToViewRatio:
            if a.likeToDislikeRatio > b.likeToDislikeRatio:
                return a  # b a a
            elif b.likeToDislikeRatio > a.likeToDislikeRatio:
                return b  # b a b
            else:
                return a  # b a =
        elif b.likeToViewRatio > a.likeToViewRatio:
            if a.likeToDislikeRatio > b.likeToDislikeRatio:
                return b  # b b a
            elif b.likeToDislikeRatio > a.likeToDislikeRatio:
                return b  # b b b
            else:
                return b  # b b =
        else:
            if a.likeToDislikeRatio > b.likeToDislikeRatio:
                return a  # b = a
            elif b.likeToDislikeRatio > a.likeToDislikeRatio:
                return b  # b = b
            else:
                return a  # b = =
    else:
        if a.likeToViewRatio > b.likeToViewRatio:
            if a.likeToDislikeRatio > b.likeToDislikeRatio:
                return a  # = a a
            elif b.likeToDislikeRatio > a.likeToDislikeRatio:
                return a  # = a b
            else:
                return a  # = a =
        elif b.likeToViewRatio > a.likeToViewRatio:
            if a.likeToDislikeRatio > b.likeToDislikeRatio:
                return a  # = b a
            elif b.likeToDislikeRatio > a.likeToDislikeRatio:
                return b  # = b b
            else:
                return b  # = b =
        else:
            if a.likeToDislikeRatio > b.likeToDislikeRatio:
                return a  # = = a
            elif b.likeToDislikeRatio > a.likeToDislikeRatio:
                return b  # = = b
            else:
                return a  # = = =


# control center for MusicHashTable.py
# noinspection PyShadowingNames
def updateCSV(setting):
    if setting == -1:  # if testing mode
        path = TestMusicPath
        FileName = 'Test.csv'
    else:
        path = NewMusicPath
        FileName = 'MusicData.csv'

    ytPath = 'https://www.youtube.com/watch?v='
    # grabbing all the files in the set path
    musicFileList = glob.glob(path + '*.mp3')
    # creating a dictionary and shoving those in there
    convertCSVtoDict()
    saveData(music)
    # Setting up the basic CSV
    saveHeader(dataList="'ARTIST', 'TITLE', 'URL', 'LIKES', 'DISLIKES', 'VIEWS', 'USED?', 'LIKES to TOTAL RATIO', "
                        "'LIKES to DISLIKES RATIO', 'LIKES to VIEWS RATIO'")
    for musicFile in musicFileList:
        file = musicFile[path.__len__():]
        new = False  # bool to represent a new track under an existing artist
        try:
            info = getTrackInfo(file)  # (artist, title, url)
            data = getStats(ytPath + info[2])  # (likes, dislikes, views)
            ratios = getRatios(data)  # (likesToTotalRatio, likeToDislikeRatio, likeToViewRatio)

        except urllib.request.HTTPError and ValueError as e:
            error(str(e) + ' ' + file)
            continue
        if data[0] == -1 and data[1] == -1 and data[2] == -1:  # if bad url
            print('>BAD URL FOUND:\t ' + str(musicFile))
            os.remove(musicFile)
            continue
        entry = Data(force_to_unicode(info[1]), force_to_unicode(info[0]),
                     force_to_unicode(info[2]), force_to_unicode(data[0]),
                     force_to_unicode(data[1]), force_to_unicode(data[2]),
                     False, float(ratios[0]), float(ratios[1]), float(ratios[2]))
        if music.has(info[0]):  # if there is an existing entry under the same artist
            #  get the song from the entry
            lst = music.get(info[0])
            for el in lst:
                if entry.Title == el.Title:  # if the song names match
                    if setting != -1:  # if not a test
                        print(">FILE DUPLICATE FOUND:\t" + str(musicFile)[str(NewMusicPath).__len__():])
                        try:
                            keeper = onlyKeepOne(el, entry)
                            if keeper == el:
                                os.remove(musicFile)
                            else:
                                music.remove(info[0], el)
                                music.put(info[0], entry)
                                os.remove(musicFile)
                        except FileNotFoundError as e:
                            error(e)
                    continue  # determine tracks to be the same, add no entry
            if setting != -1:  # if new track under existing artist
                print(">NEW ENTRY UNDER:\t" + info[0] + '-' + info[1] + ' ' + info[2])
                new = True
        if setting != -1:  # if not a test
            toCurrent(musicFile, 0)  # send track to /Current/
            if not new:  # if there hasn't already been a print
                print(">NEW ENTRY:\t\t" + info[0] + '-' + info[1] + ' ' + info[2])
        music.put(entry.Artist, entry)
        appendData(entry)
    # TODO figure out why the data isn't all being written to the CSV
    if setting != -1:  # if not a test
        print(">FILE UPDATED:\t" + str(FileName) + " in /Music/ with " + str(musicFileList.__len__()) + ' tracks')
        # print(music.__str__())


def isEnoughData():
    currCount = glob.glob(CurrentMusicPath + '*.mp3').__len__()
    newCount = glob.glob(NewMusicPath + '*.mp3').__len__()
    if currCount + newCount >= IDEAL_SIZE:
        return True
    else:
        return False


if __name__ == "__main__":
    error("Please run from main.py")
