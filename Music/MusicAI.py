# Convolutional DNN
from sklearn import tree

from Music import MusicHashTable as mht

user = mht.User('', '')
Path = user.BASEPATH
FileName = "MusicData.csv"
NewMusicPath = user.NewPath
CurrentMusicPath = user.CurrentPath
OldMusicPath = user.OldPath
TestMusicPath = user.TestPath


def label(data):
    labels = []
    for i in range(1, data.__len__()):
        entry = (str(data[i]).split(','))
        mht.printRows(entry)  # we want the ratios to get an initial idea on the videos performance
        labels.append(entry[7:])
    return labels


features = mht.readData()
labels = label()

# we are going to train a simple decition tree baised on the statistics rather than the music itself as an alpha ai
clf = tree.DecisionTreeClassifir()
clf = clf.fit(features, labels)
print(clf.prdict['Flight of the Conchords', 'Robots', 'BNC61-OOPdA', 4100, 59, 559964, False, .9858, 69.49, .0073])

# the next step will be to analize the music and understand that in the context of the ratios
# then select similar sounding music that will have high performing ratios
