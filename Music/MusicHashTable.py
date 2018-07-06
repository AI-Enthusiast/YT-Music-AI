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

    # toString()
    def __str__(self):
        out = "{0},{1},{2},{3},{4},{5},{6}".format(
            self.Artist,
            self.Title,
            self.Url,
            self.likes,
            self.dislikes,
            self.views,
            self.used
        )
        return out

music['Khalid'] = Data("Location", "by3yRdlQvzs", "Khalid",1900000, 80000,297339999)
music['Flight of the Conchords'] = Data("Robots", "BNC61-OOPdA", "Flight of the Conchords", 4100, 59, 559964)
music['Tessa Violet'] = Data("Crush", "SiAuAJBZuGs", "Tessa Violet", 111000, 4300, 1969889)
music['gnash'] = Data("home", "bYBLt_1HcQE", "gnash", 120000, 20000, 20243102)
# partially deletes data entry by it's row and col number shifts others up one
# TO TEST
def deleteEntry_Partial(rowNum, colNum):
    data = readData()
    with open(FileName, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter="\n", quotechar=" ",
                                quoting=csv.QUOTE_NONNUMERIC)
        row = 0
        while row < data.__len__():
            if row != rowNum:
                writer.writerow(data[row])
            else:
                song = data[row].split(',')
                if colNum < song.__len__():
                    song[colNum] = ""
                    str = ""
                    for el in song:
                        str += el
                    writer.writerow(str.encode('utf8', 'ignore'))
                else:
                    print("That is out of range for this row. Try again.")
                    pass



# deletes data entry by it's row number shifts others up one
# TO TEST
def deleteEntry_Row(rowNum):
    data = readData()
    with open(FileName, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter="\n", quotechar=" ",
                                quoting=csv.QUOTE_NONNUMERIC)
        row = 0
        while row < data.__len__():
            if row != rowNum:
                writer.writerow(data[row])


# adds data entry by desired row num
# TO TEST
# TODO
def addEntry(rowNum, entry):
    # reads data
    # must probe data row to check there are no conflicts
    # copy data before and after row num with entry occupying the new row
    data = readData()
    data.insert(rowNum, entry)


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
        DataWriter.writerows(dd)
        csvfile.close()


# appends dataList into csv file
def appendData(song):
    with open(FileName, 'a', newline='') as csvfile:
        DataWriter = csv.writer(csvfile, delimiter="\n", quotechar=" ",
                                    quoting=csv.QUOTE_NONNUMERIC)
        music[song.Artist] = song
        try:
            DataWriter.writerow([song.__str__()])
        except TypeError as e:
            error(e)
        csvfile.close()



# TO TEST
def clear():
    with open(FileName, 'w', newline='\n') as csvfile:
        csvfile.close()


# TO TEST
def toCurrent(musicFile):
    os.rename(Path + musicFile, CurrentMusicPath + musicFile)


# TO TEST
def toOld(musicFile):
    os.rename(CurrentMusicPath + musicFile, OldMusicPath + musicFile)


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
    return [int(removeCommas(likes)), int(removeCommas(dislikes)), int(removeCommas(views))]


def printRows(arr):
    count = 0
    while count < arr.__len__():
        print("[" + str(count) + "]" + str(arr[count]))
        count += 1


def removeCommas(string):
    out = ''.join(string.split(","))
    return out


# TO TEST
# TODO
def search():
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
    print(">ERROR: " + str(errorMessage))

def getTrackInfo(file):
    url = file[file.__len__() - 15:file.__len__() - 4]
    fx = file.split('-')
    artist = removeCommas(fx[0])
    title = removeCommas(fx[1])
    return [artist, title, url]
# TO TEST
# control center for MusicHashTable.py
def updateCSV():
    ytPath = 'https://www.youtube.com/watch?v='
    arr = glob.glob(NewMusicPath + '*.mp3')
    # TODO integrate new data with previous data
    clear()  # erases all previous data
    saveHeader(dataList=["ARTIST", 'TITLE', "URL", "LIKES", "DISLIKES", "VIEWS", "USED?"])
    for i in arr:
        file = i[NewMusicPath.__len__():]
        info = getTrackInfo(file)
        data = getStats(ytPath + info[2])  # gets views, likes and dislikes
        entry = Data(info[1], info[2], info[0], data[0], data[1], data[2], False)

        if not music.get(info[0]).__contains__(entry):
            music[info[0]] = entry
            print("New Entry: " + info[0] + info[1] + ' ' + info[2])
    saveData(dataList=music)
    printRows(">FILE Updated: " + str(FileName) + "in /Music/")


def checkResults(test, desiredResults, results):
    test = test + ':'
    if str(test).__len__() < 9:
        test = test + '\t'
    if results.__eq__(desiredResults) :
        print(">TEST " + test + "\tPASS")
    else:
        print(">TEST " + test + "\tFAIL")
        print("\tExpected Output:\t" + str(desiredResults))
        print("\tOutput Received:\t" + str(results))


def runTests():
    print(">COMMENCE TESTING...")
    results = None  # stores result of each test

    clear()
    # TEST readData()
    desiredResult = []  # stores desired result of each test
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
        appendData(music)
        results = str(readData())
        appendData(Data("in cold blood","rP0uuI80wuY" , "alt-j", 74000, 2000, 9059467, False))
        result = str(readData()[readData().__len__()-1:])
    except TypeError and ValueError as e:
        error(str(e))
        pass
    checkResults("appendData()", desiredResult, results)
    printRows(readData())
    checkResults("appendData()", desiredResult, result)

    # TEST getStats()

    desiredResult = [0, 0, 0]
    ytPath = 'https://www.youtube.com/watch?v='
    try:
        results = getStats(ytPath + "6cwBLBCehGg")
    except TypeError as e:
        error(str(e))
        pass
    checkResults("getStats()", desiredResult, results)

    checkResults("getStats()", desiredResult, result)
    printRows(readData())
    # TEST clear()
    desiredResult = 0
    try:
        clear()
        results = readData().__len__()
    except ValueError as e:
        error(str(e))
        pass
    checkResults("clear()", desiredResult, result)
    '''
    checkResults("clear()", desiredResult, results)

    # TEST toCurrent()
    desiredResult = "['Music/Current/Test 1-zGDzdps75ns.mp3', 'Music/Current/Test 0-zGDzdps75ns.mp3', " \
                    "'Music/Current/Test 4-zGDzdps75ns.mp3', 'Music/Current/Test 2-zGDzdps75ns.mp3', " \
                    "'Music/Current/Test 3-zGDzdps75ns.mp3']"
    try:
        musicList = glob.glob(user.TestPath + '*.mp3')
        for track in musicList:
            if track.split(' ')[0] == "Test":
                toCurrent(track)
        results = glob.glob(CurrentMusicPath + '*.mp3')
        for track in musicList:
            os.rename(CurrentMusicPath + track, user.TestPath + track)

    except TypeError and FileNotFoundError and AttributeError as e:
        error(str(e))
        pass
    checkResults("toCurrent()", desiredResult, results)

'''
    # TEST addEntry()
    desiredResult = "['Test4', 'Test5', 'Test6', 'Test7']"
    try:
        addEntry(2, ['Test4', 'Test5', 'Test6', 'Test7'])  # Test
        result = str(readData())  # gather results
    except TypeError and IndexError and AttributeError as e:
        error(str(e))
        pass
    checkResults("addEntry()", desiredResult, result)
    
    # TEST deleteEntry_Partial()
    desiredResult = None
    try:
        deleteEntry_Partial(0, 0)
        result = str(readData())
    except ValueError and TypeError and AttributeError as e:
        error(str(e))
        pass
    checkResults("deleteEntry_Partial()", desiredResult, result)

    # TEST deleteEntry_Row()
    desiredResult = None
    try:
        deleteEntry_Row(0)
        result = str(readData())
    except IndexError and AttributeError as e:
        error(str(e))
        pass
    checkResults("deleteEntry_Row()", desiredResult, result)

    # TEST updateCSV()
    # desiredResult = None
    # try:
    #     #test
    #     #results = bla
    # except Error as e:
    #     error(str(e))
    #     pass

    # TEST search()
    # desiredResult = None
    # try:
    #     #test
    #     #results = bla
    # except Error as e:
    #     error(str(e))
    #     pass
    '''



# TODO
# slim down and/or user control
if __name__ == "__main__":
    if not os.path.isfile(FileName):
        error("'MusicData.csv' could not be found")
        clear()
        quit()
    print("Commands are: updateCSV(), runTests()")
    while True:
        com = input('>>').split()
        if len(com) != 1:
            error("Just one command please")
            pass
        elif com[0] == '':
            quit()
        elif com[0] == "updateCSV()":
            updateCSV()
        elif com[0] == "runTests()":
            runTests()
        elif com[0] == "clear":
            clear()
        elif com[0] == "read":
            printRows(readData())
