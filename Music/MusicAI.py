# MusicAI.py started on 7/17/2018
# Authors: Cormac Dacker, Marilyn Groppe
# Version # 0.0.1

from sklearn import tree

from Music import MusicHashTable as mht

user = mht.User('', '')
Path = user.BASEPATH
FileName = "MusicData.csv"
NewMusicPath = user.NewPath
CurrentMusicPath = user.CurrentPath
OldMusicPath = user.OldPath
TestMusicPath = user.TestPath


def label(data):  # ratios
    labels = []
    for i in range(1, data.__len__()):
        entry = (str(data[i]).split(','))
        info = []
        info.append(float("{0:.6f}".format(float(entry[7]))))
        info.append(float("{0:.6f}".format(float(entry[8]))))
        info.append(float("{0:.6f}".format(float(entry[9][:entry[9].__len__() - 2]))))
        labels.append(info)
    return labels


def feature(data):  # likes, dislikes, views
    labels = []
    for i in range(1, data.__len__()):
        entry = (str(data[i]).split(','))
        info = []
        info.append(float("{0:.6f}".format(float(entry[3]))))
        info.append(float("{0:.6f}".format(float(entry[4]))))
        info.append(float("{0:.6f}".format(float(entry[5]))))
        labels.append(info)
    return labels


def temp():
    features = mht.readData()[1:]
    labels = label(features)
    features = feature(features)

    # we are going to train a simple decision tree based on the statistics rather than the music itself as an alpha ai
    clf = tree.DecisionTreeRegressor()
    clf = clf.fit(features, labels)
    print(clf.predict([[4100, 59, 559964]]))
    clf.__str__()


temp()

# TODO pic a song from /current/
# TODO the next step will be to analize the music and understand that in the context of the ratios
# then select similar sounding music that will have high performing ratios
if __name__ == "__main__":
    print("Please run from main.py")

