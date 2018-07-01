# MusicHashTable.py started on 6/25/2018
# Authors: Cormac Dacker, Marilyn Groppe
# Vertion# 0.0.6

import csv
import glob
import os
import urllib.request
from bs4 import BeautifulSoup


class User:
    def __init__(self, BASEPATH, code):
        self.BASEPATH = BASEPATH
        self.code = code

        self.MusicPath = self.BASEPATH + '/Music/'
        self.NewPath = self.MusicPath + '/New/'
        self.OldPath = self.MusicPath + '/Old/'
        self.CurrentPath = self.MusicPath + '/Current/'


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
        out = "{0},{1},{2},{3},{4},{5},{6},{7}".format(
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
    lst = [*dataList.keys()]
    with open(FileName, 'a', newline='') as csvfile:
        DataWriter = csv.writer(csvfile, delimiter="\n", quotechar=" ",
                                    quoting=csv.QUOTE_NONNUMERIC)
        for key in lst:
            val = dataList.get(key)
            data = []
            for el in val:
                data.append(force_to_unicode(el))
            DataWriter.writerow([i for i in data])
        csvfile.close()


# appends dataList into csv file
def appendData(dataList):
    with open(FileName, 'a', newline='') as csvfile:
        DataWriter = csv.writer(csvfile, delimiter="\n", quotechar=" ",
                                    quoting=csv.QUOTE_NONNUMERIC)

        DataWriter.writerows([[i for i in dataList.get(el)] for el in dataList.keys()])
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
    print(">ERROR: " + errorMessage)


# TO TEST
# control center for MusicHashTable.py
def updateCSV():
    ytPath = 'https://www.youtube.com/watch?v='
    print(readData())
    numOfEntrys = readData().__len__() - 1  # -1 because headers at the top of the csv
    arr = glob.glob(NewMusicPath + '*.mp3')
    numOfEntrys += arr.__len__()
    # TODO integrate new data with previous data
    clear()  # erases all previous data
    saveHeader(dataList=["ARTIST", 'Title', "URL", "HASH", "LIKES", "DISLIKES", "VIEWS", "USED?"])
    for i in arr:
        file = i[NewMusicPath.__len__():]
        url = file[file.__len__() - 15:file.__len__() - 4]
        fx = file.split('-')
        artist = removeCommas(fx[0])
        title = removeCommas(fx[1])
        used = False

        data = getStats(ytPath + url)  # gets views, likes and dislikes
        likes = removeCommas(data[0])
        dislikes = removeCommas(data[1])
        views = removeCommas(data[2])
        '''
        index = 0
        inlist = False
        while index < Fnames.__len__():  # check Fnames list to see if artist is already in it
            if Fnames[index] == artist:
                inlist = True
                break
            index += 1

        if not inlist:  # checks results from list check
            Fnames.append(artist)
        '''
        hs = hash(artist) % numOfEntrys  # hash by artist
        entry = Data(title, url, artist, hs, likes, dislikes, views, used)
        dict = {artist: [entry.__str__()]}
        print("New Entry: " + artist + title + ' ' + url)
        saveData(dataList=dict)


def checkResults(test, desiredResults, results):
    if results.__eq__(desiredResults) :
        print("TEST " + test + ":\tPASS")
    else:
        print("TEST " + test + ":\tFAIL")
        print("\tExpected Output: " + str(desiredResults))
        print("\tOutput Received: " + str(results))


def runTests():
    print(">COMMENCE TESTING...")
    result = None  # stores result of each test

    clear()
    # TEST readData()
    desiredResult = []  # stores desired result of each test
    try:
        result = readData()
    except TypeError and ValueError and FileNotFoundError as e:
        error(str(e))
        pass
    checkResults("readData()", desiredResult, result)

    # TEST saveHeader()
    desiredResult = "['Test0', 'Test1', 'Test2', 'Test3']"
    try:
        saveHeader(dataList=['Test0', 'Test1', 'Test2', 'Test3'])  # Test
        result = str(readData()[0])  # gather results
    except TypeError and ValueError as e:
        error(str(e))
        pass
    checkResults('saveHeader()', desiredResult, result)

    # TEST saveData()
    desiredResult = "['00', 'TestSong', 'test--notreal', '0', '45', '23', '123456', ' False']"
    try:
        testSong = Data("TestSong", "test--notreal", "00", 0, 45, 23, 123456)
        test = {"00" : testSong.__str__()}
        saveData(test)  # Test
        result = str(readData()[1])  # gather results
    except ValueError and AttributeError as e:
        error(str(e))
        pass
    checkResults("saveData()", desiredResult, result)

    # TEST appendData()
    desiredResult = "['Test4', 'Test5', 'Test6', 'Test7']"
    try:
        Fnames.append("key")
        appendData({"key": ['Test4', 'Test5', 'Test6', 'Test7']})
        result = str(readData()[2])  # probably not the right way to find the results
    except TypeError and ValueError as e:
        error(str(e))
        pass
    checkResults("appendData()", desiredResult, result)
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

    # TEST clear()
    desiredResult = 0
    try:
        clear()
        result = readData().__len__()
    except ValueError as e:
        error(str(e))
        pass
    checkResults("clear()", desiredResult, result)

    # TEST toCurrent()
    # desiredResult = None
    # try:
    #     #test
    #     #results = bla
    # except Error as e:
    #     error(str(e))
    #     pass

    # TEST getStats()
    # desiredResult = None
    # try:
    #     #test
    #     #results = bla
    # except Error as e:
    #     error(str(e))
    #     pass

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
        elif com[0] == "updateCSV()" or com[0] == "u":
            updateCSV()
        elif com[0] == "runTests()":
            runTests()
        elif com[0] == "clear":
            clear()
        elif com[0] == "read":
            printRows(readData())
