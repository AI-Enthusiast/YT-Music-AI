import glob
import os
import unittest as ut
from Music import YT_Bot as yt
from Music import MusicHashTable as mht
from Music import HashTable as ht
from Music import MusicAI as ai


# prints error message
def error(errorMessage):
    print(">ERROR:\t" + str(errorMessage))


class TestYT_Bot(ut.TestCase):

    def testIsLive(self):
        self.assertTrue(yt.isLive(['live', 'test', 'test', 'test']))
        self.assertTrue(yt.isLive(['test', 'test', 'live', 'test']))
        self.assertTrue(yt.isLive(['test', 'test', 'test', 'live']))
        self.assertFalse(yt.isLive(['test', 'test', 'test', 'test']))


class TestMusicHashTable(ut.TestCase):
    mht.FileName = 'Test.csv'

    def testMode(self):
        self.assertEqual(mht.FileName, 'Test.csv'
                         )

    def testReadData(self):
        desiredResult = []
        mht.clear()
        try:
            data = mht.readData()
            self.assertEqual(data, desiredResult, 'Failed to read from file' + mht.FileName)
        except TypeError and ValueError and FileNotFoundError as e:
            error(str(e))
            pass

    def testSaveHeader(self):
        desiredResult = "[\"['ARTIST', 'TITLE', 'URL', 'HASH', 'LIKES', 'DISLIKES', 'VIEWS', 'USED?']\"]"
        try:
            mht.saveHeader(dataList=['ARTIST', 'TITLE', 'URL', 'HASH', 'LIKES', 'DISLIKES', 'VIEWS', 'USED?'])  # Test
            results = str(mht.readData()[0])  # gather results
            self.assertEqual(results, desiredResult)
        except TypeError and ValueError as e:
            error(str(e))
            pass

    def testSaveData(self):
        desiredResult = "[['Flight of the Conchords,Robots,BNC61-OOPdA,4100,59,559964,False']," \
                        " ['Tessa Violet,Crush,SiAuAJBZuGs,111000,4300,1969889,False'], " \
                        "['gnash,home,bYBLt_1HcQE,120000,20000,20243102,False'], " \
                        "['alt-j,in cold blood,rP0uuI80wuY,74000,2000,9059467,False']]"
        try:
            mht.saveData(mht.music)
            results = str(mht.readData()[1:])  # gather results
            self.assertEqual(results, desiredResult)
        except ValueError and AttributeError as e:
            error(str(e))
            pass

    def testAppendData(self):
        desiredResult = "[['alt-j,in cold blood,rP0uuI80wuY,74000,2000,9059467,False']]"
        try:
            mht.clear()
            mht.appendData(mht.Data("in cold blood", "rP0uuI80wuY", "alt-j", 74000, 2000, 9059467, False))
            results = str(mht.readData()[mht.readData().__len__() - 1:])
            self.assertEqual(desiredResult, results)
        except TypeError and ValueError as e:
            error(str(e))
            pass

    def testGetStats(self):
        desiredResult = [0, 0, 0]
        ytPath = 'https://www.youtube.com/watch?v='
        try:
            results = mht.getStats(ytPath + "6cwBLBCehGg")
            self.assertEqual(results, desiredResult)
        except TypeError as e:
            error(str(e))
            pass

    def testClear(self):
        desiredResult = 0
        try:
            mht.clear()
            results = mht.readData().__len__()
            self.assertEqual(results, desiredResult)
        except ValueError as e:
            error(str(e))
            pass

    def testToCurrent(self):
        desiredResult = ['Music/Current\Test 0-title-6cwBLBCehGg.mp3',
                         'Music/Current\Test 1-title-6cwBLBCehGg.mp3',
                         'Music/Current\Test 2-title-6cwBLBCehGg.mp3',
                         'Music/Current\Test 3-title-6cwBLBCehGg.mp3',
                         'Music/Current\Test 4-title-6cwBLBCehGg.mp3']
        try:
            musicList = glob.glob(mht.TestMusicPath + '*.mp3')  # gather a list of tracks in /Test/
            for track in musicList:
                if str(track.split(' ')[0])[-4:] == "Test":
                    track = track[mht.TestMusicPath.__len__():]
                    mht.toCurrent(track, '-1')

            results = glob.glob(mht.CurrentMusicPath + '*.mp3')  # gather a list of tracks in /Music/Current/
            for track in results:  # return Test*.mp3 to /Test/
                track = track[mht.CurrentMusicPath.__len__():]
                if track.split(' ')[0] == "Test":
                    os.rename(mht.CurrentMusicPath + track, mht.TestMusicPath + track)
            self.assertEqual(results, desiredResult)
        except TypeError and FileNotFoundError and AttributeError and OSError as e:
            error(str(e))
            pass

    def testUpdateCSV(self):
        desiredResult = [["'ARTIST', 'TITLE', 'URL', 'LIKES', 'DISLIKES', 'VIEWS', 'USED?'"],
                         ['Test 0,title,6cwBLBCehGg,0,0,0,False'],
                         ['Test 1,title,6cwBLBCehGg,0,0,0,False'],
                         ['Test 2,title,6cwBLBCehGg,0,0,0,False'],
                         ['Test 3,title,6cwBLBCehGg,0,0,0,False'],
                         ['Test 4,title,6cwBLBCehGg,0,0,0,False']]
        try:
            mht.clear()
            mht.updateCSV(-1)
            results = mht.readData()
            mht.clear()
            self.assertEqual(results, desiredResult)
        except TypeError as e:
            error(str(e))
            pass


if __name__ == '__main__':
    ut.main()
