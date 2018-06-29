import csv
import glob
import os
import urllib.request

from bs4 import BeautifulSoup

FileName = "MusicData.csv"
Path = 'C:/Users/mjgro/Documents/GitHub/YT-Music-AI/Music/'
NewMusicPath = 'C:/Users/mjgro/Documents/GitHub/YT-Music-AI/Music/New/'
CurrentMusicPath = 'C:/Users/mjgro/Documents/GitHub/YT-Music-AI/Music/Current/'
OldMusicPath = 'C:/Users/mjgro/Documents/GitHub/YT-Music-AI/Music/Old/'
DEVELOPER_KEY = "AIzaSyDsEUDbBKzBE6HS96PJ7FQpS5a8qfEV3Sk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
Fnames = []

#A class used to create music file objects
class Data:
    #Constructer
    def __init__(self, Title="", Url="", Artist="", Hash=0, likes=0, dislikes=0, views=0,
                 used=False):  # used, artist, tempo, ect
        self.Title = Title
        self.Url = Url
        self.Artist = Artist
        self.Hash = Hash
        self.likes = likes
        self.dislikes = dislikes
        self.views = views
        self.used = used
    #toString()
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

    # Reads through data and outputs it as array eg out[row]
    def readData(self):
        with open(FileName, "r", newline='\n') as csvfile:
            DataReader = csv.reader(csvfile, delimiter="\n", quotechar=" ",
                                    quoting=csv.QUOTE_NONNUMERIC)
            out = []
            for Item in DataReader:
                out.append(Item[0])
            csvfile.close()
            return out

    # Saves Header dataList into csv file
    def saveHeader(self, dataList=[[]]):
        with open(FileName, 'w', newline='\n') as csvfile:
            DataWriter = csv.writer(csvfile, delimiter="\n", quotechar=" ",
                                    quoting=csv.QUOTE_NONNUMERIC)
            DataWriter.writerow(dataList)
            csvfile.close()

    # Saves dataList into csv file
    def saveData(self, dataList={}):
        with open(FileName, 'w', newline='\n') as csvfile:
            fnames = ["Title", "Url", "Artist", "Hash",
                      "views", "dislikes", "likes"]
            DataWriter = csv.DictWriter(csvfile, delimiter="\n", quotechar=" ",
                                        quoting=csv.QUOTE_NONNUMERIC, fieldnames=Fnames)
            DataWriter.writerow(dataList)
            csvfile.close()

    # appends dataList into csv file
    def appendData(self, dataList={}):
        with open(FileName, 'a', newline='\n') as csvfile:
            fnames = ["Title", "Url", "Artist", "Hash",
                      "views", "dislikes", "likes"]
            DataWriter = csv.DictWriter(csvfile, delimiter="\n", quotechar=" ",
                                        quoting=csv.QUOTE_NONNUMERIC, fieldnames=Fnames)
            DataWriter.writerow(dataList)
            csvfile.close()

    # deletes data entry by it's row number shifts others up one
    #TODO
    def deleteEntry(self, rowNum):
        data = Data.readData(self)
        a = data[:rowNum]
        b = data[rowNum + 1:]
        self.saveData(a + b)
    #TODO
    def addEntry(self, rowNum, entry):
        data = Data.readData(self)
        data.insert(rowNum, entry)

    def clear(self):
        with open(FileName, 'w', newline='\n') as csvfile:
            csvfile.close()

    def toCurrent(self, musicFile):
        os.rename(NewMusicPath + musicFile, CurrentMusicPath + musicFile)

    def toOld(self, musicFile):
        os.rename(CurrentMusicPath + musicFile, OldMusicPath + musicFile)


#  def cleanCSV(self):

def force_to_unicode(text):
    test = str(text)
    "If text is unicode, it is returned as is. If it's str, convert it to Unicode using UTF-8 encoding"
    return text if isinstance(text, bytes) else text.encode('utf8')


# gets views, likes and dislikes
def getStats(url):
    soup = BeautifulSoup(urllib.request.urlopen(url).read().decode('utf-8', 'ignore'), 'html.parser')
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

#TODO
def search(term=''):
    with open(FileName, "r", newline='\n') as csvfile:
        DataReader = csv.DictReader(csvfile, delimiter="\n", quotechar=" ",
                                    quoting=csv.QUOTE_NONNUMERIC)
        out = {}
        for Item in DataReader:
            print(Item.keys())
        csvfile.close()
        return out

#TODO
#slim down and/or user control
if __name__ == "__main__":
    ytPath = 'https://www.youtube.com/watch?v='
    if not os.path.isfile(FileName):
        print("ERROR: 'MusicData.csv' could not be found")
        quit()

    numOfEntrys = Data.readData(Data).__len__() - 1  # -1 because headers at the top of the csv
    arr = glob.glob(NewMusicPath + '*.mp3')
    numOfEntrys += arr.__len__()
    # Data.saveHeader(Data, dataList=[["ARTIST", 'Title', "URL", "HASH", "LIKES","DISLIKES", "VIEWS", "USED?"]])
    Data.clear(Data)
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

        hs = hash(artist) % numOfEntrys  # hash by artist
        dict = {artist: [artist, title, url, hs, likes, dislikes, views, used]}
        # NewData = ([force_to_unicode(dict)])
        print("New Entry: " + artist + title + ' ' + url)
        Data.appendData(Data, dataList=dict)
    printRows(Data.readData(Data))
    search(Fnames[3])
