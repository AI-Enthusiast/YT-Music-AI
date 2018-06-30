# MusicHashTable.py started on 6/25/2018
# Authors: Cormac Dacker, Marilyn Groppe
# Vertion# 0.0.4


import csv
import glob
import os
import urllib.request
from Music import YT_Bot
from bs4 import BeautifulSoup
from Music import main

FileName = "MusicData.csv"
user = main.User('', '')
Path = user.BASEPATH
NewMusicPath = user.NewPath
CurrentMusicPath = user.CurrentPath
OldMusicPath = user.OldPath
DEVELOPER_KEY = "AIzaSyDsEUDbBKzBE6HS96PJ7FQpS5a8qfEV3Sk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
Fnames = []


# A class used to create music file objects
class Data:
    # Constructer
    def __init__(self, Title="", Url="", Artist="", Hash=0, likes=0, dislikes=0, views=0,
                 used=False):  # used, artist, tempo, etc
        self.Title = Title
        self.Url = Url
        self.Artist = Artist
        self.Hash = Hash
        self.likes = likes
        self.dislikes = dislikes
        self.views = views
        self.used = used

    # toString()
    def __str__(self):
        out = "{0},{1},{2},{3},{4},{5},{6}, {7}".format(
            self.Artist,
            self.Title,
            self.Url,
            self.Hash,
            self.likes,
            self.dislikes,
            self.views,
            self.used
        )
        return out

    # partially deletes data entry by it's row and col number shifts others up one
    # TO TEST
    def deleteEntry_Partial(self, rowNum, colNum):
        data = readData()
        with open(FileName, 'wb'):
            writer = csv.writer(FileName)
            row = 0
            while row < data.__len__():
                if row != rowNum:
                    writer.writerow(data[row])
                else:
                    writer.writerow("")

    # deletes data entry by it's row number shifts others up one
    # TO TEST
    def deleteEntry_Row(self, rowNum):
        data = readData()
        with open(FileName, 'wb'):
            writer = csv.writer(FileName)
            row = 0
            while row < data.__len__():
                if row != rowNum:
                    writer.writerow(data[row])

    # adds data entry by desired row num
    # TO TEST
    # TODO
    def addEntry(self, rowNum, entry):
        # reads data
        # must probe data row to check there are no conflicts
        # copy data before and after row num with entry occupying the new row
        data = readData()
        data.insert(rowNum, entry)


# Reads through data and outputs it as array eg out[row]
def readData():
    with open(FileName, "r", newline='\n') as csvfile:
        DataReader = csv.reader(csvfile, delimiter="\n", quotechar=" ",
                                quoting=csv.QUOTE_NONNUMERIC)
        out = []
        print(DataReader)
        for Item in DataReader:
            out.append(Item[0])
            csvfile.close()
        return out


# Saves Header dataList into csv file
# TO TEST
def saveHeader(dataList=[]):
    with open(FileName, 'w', newline='\n') as csvfile:
        DataWriter = csv.writer(csvfile, delimiter="\n", quotechar=" ",
                                quoting=csv.QUOTE_NONNUMERIC)
        DataWriter.writeheader(dataList)
        csvfile.close()


# Saves dataList into csv file
# TO TEST
def saveData(dataList={}):
    with open(FileName, 'w', newline='\n') as csvfile:
        DataWriter = csv.DictWriter(csvfile, delimiter="\n", quotechar=" ",
                                    quoting=csv.QUOTE_NONNUMERIC, fieldnames=Fnames)
        DataWriter.writerow(dataList)
        csvfile.close()


# appends dataList into csv file
def appendData(dataList={}):
    with open(FileName, 'a', newline='\n') as csvfile:
        DataWriter = csv.DictWriter(csvfile, delimiter="\n", quotechar=" ",
                                    quoting=csv.QUOTE_NONNUMERIC, fieldnames=Fnames)
        DataWriter.writerow(dataList)
        csvfile.close()


# TO TEST
def clear():
    with open(FileName, 'w', newline='\n') as csvfile:
        csvfile.close()


# TO TEST
def toCurrent(musicFile):
    os.rename(NewMusicPath + musicFile, CurrentMusicPath + musicFile)


# TO TEST
def toOld(musicFile):
    os.rename(CurrentMusicPath + musicFile, OldMusicPath + musicFile)


# def cleanCSV(self):

def force_to_unicode(text):
    return text if isinstance(text, bytes) else text.encode('utf8')


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
    else:
        dislikes = str(dislikes).split('>')
        dislikes = dislikes[dislikes.__len__() - 3]
        dislikes = dislikes[:dislikes.__len__() - 6]
    Views = soup.find_all('div', class_="watch-view-count")
    views = Views[0]
    views = (str(views).split('>'))[1]
    views = views[:views.__len__() - 11]

    return [likes, dislikes, views]


def printRows(arr=[]):
    count = 0
    while count < arr.__len__():
        print("[" + str(count) + "]" + str(arr[count]))
        count += 1


def removeCommas(string):
    out = ''.join(string.split(","))
    return out


# TO TEST
# TODO
def search(term=''):
    with open(FileName, "r", newline='\n') as csvfile:
        DataReader = csv.DictReader(csvfile, delimiter="\n", quotechar=" ",
                                    quoting=csv.QUOTE_NONNUMERIC)
        out = {}
        for Item in DataReader:
            print(Item.keys())
        csvfile.close()
        return out


# prints error message
def error(errorMessage):
    print(">ERROR: " + errorMessage)


# TO TEST
# control center for MusicHashTable.py
def updateCSV():
    # numOfEntrys = readData().__len__() - 1  # -1 because headers at the top of the csv
    arr = glob.glob(NewMusicPath + '*.mp3')
    # numOfEntrys += arr.__len__()
    # Data.saveHeader(Data, dataList=[["ARTIST", 'Title', "URL", "HASH", "LIKES"
    # ,"DISLIKES", "VIEWS", "USED?"]])
    clear()
    for i in arr:
        file = i[44:]
        url = file[file.__len__() - 15:file.__len__() - 4]
        fx = file.split('-')
        artist = removeCommas(fx[0])
        title = removeCommas(fx[1])
        used = False

        data = getStats(ytPath + url)  # gets views, likes and dislikes
        likes = removeCommas(data[0])
        dislikes = removeCommas(data[1])
        views = removeCommas(data[2])

        index = 0
        inlist = False
        while index < Fnames.__len__():  # check Fnames list to see if artist is already in it
            if Fnames[index] == artist:
                inlist = True
                break
            index += 1

        if not inlist:  # checks results from list check
            Fnames.append(artist)

        # hs = hash(artist) % numOfEntrys  # hash by artist
        hs = 0  # temp
        dict = {artist: [artist, title, url, hs, likes, dislikes, views, used]}
        # NewData = ([force_to_unicode(dict)])
        print("New Entry: " + artist + title + ' ' + url)
        appendData(dataList=dict)


def runTests():
    print(">COMMENCE TESTING...")
    result = None  # stores result of each test
    desiredResult = None  # stores desired result of each test

    # TEST saveHeader()
    desiredResult = "['Test0', 'Test1', 'Test2', 'Test3']"
    try:
        saveHeader(Data, dataList=['Test0', 'Test1', 'Test2', 'Test3'])  # Test
        result = str(readData()[0])  # gather results
    except TypeError as e:
        error(str(e))
        pass
    if (result == desiredResult):  # check if results are correct
        print("TEST saveHeader(): PASS")
    else:
        print("TEST saveHeader(): FAIL")

    # TEST saveData()
    try:
        saveData({"key": ["Test0", 'Test1', "Test2", "Test3"]})
        result = str(readData())
    except ValueError as e:
        error(str(e))
        pass
    # TEST addEntry()
    # TEST appendData()
    # TEST deleteEntry_Partial()
    # TEST deleteENtry_Row()
    # TEST clear()
    # TEST toCurrent()
    # TEST getStats()
    # TEST updateCSV()
    # TEST search()


# TODO
# slim down and/or user control
if __name__ == "__main__":
    ytPath = 'https://www.youtube.com/watch?v='
    if not os.path.isfile(FileName):
        error("'MusicData.csv' could not be found")
        quit()
    print("Commands are: updateCSV(), runTests()")
    while True:
        com = input('>>').split()
        if len(com) > 1:
            error("Just one command please")
        elif com[0] == "updateCSV()":
            updateCSV()
            printRows(readData())
        elif com[0] == "runTests()":
            runTests()
        elif com[0] == '':
            quit()
