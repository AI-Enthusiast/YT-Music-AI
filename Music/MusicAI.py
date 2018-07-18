# Convolutional DNN
from Music import MusicHashTable as mht

user = mht.User('', '')
Path = user.BASEPATH
FileName = "MusicData.csv"
NewMusicPath = user.NewPath
CurrentMusicPath = user.CurrentPath
OldMusicPath = user.OldPath
TestMusicPath = user.TestPath


def label(data):
    lables = []
    for i in range(1, data.__len__()):
        entry = (str(data[i]).split(','))
        mht.printRows(entry)


data = mht.readData()
lables = label()
