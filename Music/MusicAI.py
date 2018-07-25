# MusicAI.py started on 7/17/2018
# Authors: Cormac Dacker, Marilyn Groppe
# Version # 0.0.3
import sys
from glob import glob
from subprocess import Popen, PIPE

import numpy as np
from sklearn import tree

from Music import MusicHashTable as mht


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
    elif sys.path.__contains__(cormac.BASEPATH[:-1]):
        user = cormac
    else:
        user = User(sys.path[0] + '\\', 'nu')
    return user


user = setUser()
FileName = "MusicData.csv"
NewMusicPath = user.NewPath
CurrentMusicPath = user.CurrentPath
OldMusicPath = user.OldPath
TestMusicPath = user.TestPath


def error(errorMessage):
    print(">ERROR:\t" + str(errorMessage))


def label(data, test):  # likes, dislikes, views, ratios
    labels = []
    if test == -1:
        data = data[:10]
    for i in range(1, data.__len__()):
        entry = (str(data[i]).split(','))
        info = [float("{0:.6f}".format(float(entry[3]))), float("{0:.6f}".format(float(entry[4]))),
                float("{0:.6f}".format(float(entry[5]))), float("{0:.6f}".format(float(entry[7]))),
                float("{0:.6f}".format(float(entry[8]))), float("{0:.6f}".format(float(entry[9]
                                                                                       [:entry[9].__len__() - 2])))]
        labels.append(info)
    return labels


def feature(path, test=0):  # MP3 to array
    musicFileList = glob(path + '*.mp3')
    if test == -1:
        musicFileList = musicFileList[:10]
    features = []
    for track in musicFileList:
        # If you are on Windows use full path to ffmpeg.exe
        cmd = ["C:/Users/corma/Documents/GitHub/YT-Music-AI/Music/ffmpeg.exe", "-i", track, "-f", "mp3", "-"]
        # If you are on W add argument creationflags=0x8000000 to prevent another console window jumping out
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, creationflags=0x8000000)
        data = p.communicate()[0]
        a = data[data.find(data) + 4:]
        b = np.int16
        print(a)
        print(b)
        print(np.fromstring(a, b))
        features.append(np.fromstring(data[data.find(data) + 4:], np.int16))
    print(features)  # debuging
    return features


def train():
    data = mht.readData()[1:]
    if not data:
        error("MusicData.csv has no data to train decision tree")
        mht.isEnoughData()  # TODO add jobs top queue to gather and index data
        quit()
    labels = label(data, 0)
    features = feature(CurrentMusicPath)
    clf = tree.DecisionTreeRegressor(random_state=0)
    clf = clf.fit(features, labels)  # analize the music in context of it's ratios and other stats
    test(clf)


def test(clf):
    testingMusic = feature(CurrentMusicPath, -1)
    prediction = clf.predict([testingMusic])
    actual = label(mht.readData()[1:], -1)
    print(prediction)
    print(clf.score(prediction, actual))
    print(clf.__str__())  # debuging


# TODO pic a song from /current/
# then select similar sounding music that will have high performing ratios
if __name__ == "__main__":
    print("Please run from main.py")
    train()
