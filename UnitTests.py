import glob
import os
import unittest as ut
from Music import YT_Bot as yt
from Music import MusicHashTable as mht
from Music import HashTable as ht
from Music import MusicAI as ai


TEST_VIDEO = '6cwBLBCehGg'

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
            results = mht.getStats(ytPath + TEST_VIDEO)
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


class TestHashTable(ut.TestCase):
    def testH1(self):
        desiredResult = 205
        Table = ht.HashTable()
        result = Table.h1(key="test")
        self.assertEqual(result, desiredResult)

    def testH2(self):
        desiredResult = 23
        Table = ht.HashTable()
        result = Table.h2(key="test")
        self.assertEqual(result, desiredResult)

    def testCutOff(self):
        desiredResult = True
        Table = ht.HashTable()
        Table.capacity = 10
        Table.size = 4
        result = Table.cutoff()
        self.assertEqual(result, desiredResult)
        desiredResult = False
        Table.capacity = 10
        Table.size = 5
        result = Table.cutoff()
        self.assertEqual(result, desiredResult)

    def testDoubleHashing(self):
        desiredResult = True
        Table = ht.HashTable()
        Table.capacity = 10
        result = Table.doubleHashing('testKey0', "[test0, test1, test2]")
        self.assertEqual(result, desiredResult)

        desiredResult = False
        result = Table.doubleHashing('testKey1', "[test0, test1, test2]")
        self.assertEqual(result, desiredResult)

        desiredResult = True
        result = Table.doubleHashing('testKey2', "[test0, test1, test2]")
        print(result)
        Table.__str__()
        self.assertEqual(result, desiredResult)

    def testGet(self):
        desiredResult = '' #key exist
        Table = ht.HashTable()
        Table.put('testKey0', "[test0, test1, test2]")
        result = Table.get('testKey0')
        print(result)
        self.assertEqual(result, desiredResult)

        desiredResult = '' #key but different title
        Table.put('testKey0', "[test3, test4, test5]")
        result = Table.get('testKey0')
        self.assertEqual(result, desiredResult)

        desiredResult = None # key does not exist
        Table.put('testKey1', "[test0, test1, test2]")
        result = Table.get('testKey2')# key does not exist
        self.assertEqual(result, desiredResult)

    def testSearch(self):
        Table = ht.HashTable()

        desiredResult = ''
        result = Table.put('testKey0', "[test0, test1, test2]")
        self.assertEqual(result, desiredResult)

        desiredResult = ''
        result = Table.put('testKey1', "[test0, test1, test2]")
        self.assertEqual(result, desiredResult)

        desiredResult = ''
        result = Table.put('testKey2', "[test0, test1, test2]")
        self.assertEqual(result, desiredResult)

    def testRehash(self):
        desiredResult1 = 10
        desiredResult2 = 37
        desiredResult3 = ['BROCKHAMPTON', 'Milo', 'gnash']
        desiredResult4 = [mht.Data('SWEET', TEST_VIDEO, 'BROCKHAMPTON', 0, 0, 0),
                          mht.Data('Almost Cut My Hair (For Crosby)', TEST_VIDEO, 'Milo', 0, 0, 0),
                          mht.Data('i hate u, i love u', TEST_VIDEO, 'gnash', 0, 0, 0),
                          mht.Data('CINEMA 1', TEST_VIDEO, 'BROCKHAMPTON', 0, 0, 0)]
        desiredResult5 = 4
        desiredResult6 = 1
        Table = ht.HashTable(5)
        Table.put('BROCKHAMPTON', mht.Data('SWEET', TEST_VIDEO, 'BROCKHAMPTON', 0, 0, 0))
        Table.put('Milo', mht.Data('Almost Cut My Hair (For Crosby)', TEST_VIDEO, 'Milo', 0, 0, 0))
        Table.put('gnash', mht.Data('i hate u, i love u', TEST_VIDEO, 'gnash', 0, 0, 0))
        Table.put('BROCKHAMPTON', mht.Data('CINEMA 1', TEST_VIDEO, 'BROCKHAMPTON', 0, 0, 0))

        Table.rehash()
        self.assertEqual(desiredResult6, Table.rehashed)

        self.assertEqual(desiredResult1, Table.capacity)
        self.assertNotEqual(desiredResult2, Table.seed)
        Table.keys.sort()
        self.assertEqual(desiredResult3, Table.keys)
        self.assertEqual(desiredResult4, Table.values)
        self.assertEqual(desiredResult5, Table.size)

    def testPut(self):
        Table = ht.HashTable(5)
        Table.put('Gregory Alan Isakov', mht.Data('Black Car', TEST_VIDEO, 'Gregory Alan Isakov', 0, 0, 0))
        self.assertEqual(1, Table.size)
        self.assertEqual(['Gregory Alan Isakov'], Table.keys)
        self.assertEqual([ mht.Data('Black Car', TEST_VIDEO, 'Gregory Alan Isakov', 0, 0, 0)], Table.values)
        self.assertEqual([ mht.Data('Black Car', TEST_VIDEO, 'Gregory Alan Isakov', 0, 0, 0)],
                         Table.table[Table.h1('Gregory Alan Isakov')])

    def testRemove(self):
        Table = ht.HashTable(10)
        Table.put('One Direction', mht.Data('What Makes You Beautiful', TEST_VIDEO, 'One Direction', 0, 0, 0))
        desiredResult1 = 1
        desiredResult2 = 0
        desiredResult3 = []
        desiredResult4 = [mht.Data('What Makes You Beautiful', TEST_VIDEO, 'One Direction', 0, 0, 0)]
        desiredResult5 = [[], [], [], [], [], [], [], [], [], []]
        desiredResult6 = ['One Direction']
        self.assertEqual(desiredResult1, Table.size)
        self.assertEqual(desiredResult4, Table.values)
        self.assertEqual(desiredResult6, Table.keys)
        Table.remove('One Direction')
        self.assertEqual(desiredResult2, Table.size)
        self.assertEqual(desiredResult3, Table.keys)
        self.assertEqual(desiredResult3, Table.values)
        self.assertEqual(desiredResult5, Table.table)


    def testHas(self):
        desiredResult = ''
        Table = ht.HashTable(10)
        result = Table.doubleHashing('testKey0', "[test0, test1, test2]")
        self.assertEqual(result, desiredResult)

        desiredResult = ''
        result = Table.doubleHashing('testKey1', "[test0, test1, test2]")
        self.assertEqual(result, desiredResult)

        desiredResult = ''
        result = Table.doubleHashing('testKey2', "[test0, test1, test2]")
        self.assertEqual(result, desiredResult)
        self.assertEqual(result, desiredResult)


if __name__ == '__main__':
    ut.main()
