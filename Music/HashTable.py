# HashTable.py started on 7/9/2018
# Authors: Marilyn Groppe, Cormac Dacker
# Version # 0.0.1

from Music import MusicHashTable as mh
class HashTable:

    def __init__(self):
        self.size = 0
        self.capacity = 1000
        self.table = []
        self.seed = 37
        for i in range(self.capacity):
            self.table.append([])
        self.resize = 2
        self.values = []
        self.keys = []

    def __str__(self):
        for i in range(self.capacity):
            if self.table[i]:
                print("ARTIST: " + self.table[i][0].Artist)
                for j in self.table[i]:
                    print(j.__str__())
        print(self.capacity)
        print(self.size)

    def error(errorMessage):
        print(">ERROR:\t" + str(errorMessage))

    def h1(self, key):
        return hash(key) % self.capacity

    def h2(self, key):
        return hash(key) % self.seed

    def cutoff(self):
        if (self.capacity - self.size) < self.capacity // 2:
            return True
        else:
            return False

    # method to resolve collision by quadratic probing method
    def doubleHashing(self, key, value):
        posFound = False
        limit = self.capacity * .8
        i = 2
        newPosition = 0
        while i <= limit:
            newPosition = (i * self.h1(key) + self.h2(key)) % self.size
            if self.table[newPosition] == 0:
                posFound = True
                break
            else:
                # as the position is not empty increase i
                i += 1

        if posFound:
            value.isDoubleHashed = True
        return posFound, newPosition

    def get(self, key):
        return self.table[self.h1(key)]

    def rehash(self):
        self.capacity *= self.resize
        print("Rehashing... capacity is now " + str(self.capacity))
        self.table = [[] for i in range(0, self.capacity)]
        self.size = 0
        for value in self.values:
            self.put(value.Artist, value)

    def put(self, key, value):
        if self.cutoff():  # if table is full rehash
            self.rehash()
            self.put(key, value)
        elif self.table[self.h1(key)] == []:  # if position empty
            self.table[self.h1(key)].append(value)
            value.pos = self.h1(key)
            self.size += 1
            self.values.append(value)
            self.keys.append(key)
        elif self.table[self.h1(key)][0].Artist == key:  # if entry existing under artist already
            self.table[self.h1(key)].append(value)
            value.pos = self.h1(key)
            self.size += 1
            self.values.append(value)
            self.keys.append(key)

        else:  # Collision time to double hash
            poss = self.doubleHashing(key, value)
            newPos = poss[1]
            value.pos = newPos
            self.table[newPos] = [value]


    def remove(self, item):
        try:
            self.table[item.pos].remove(item)
            print(">ITEM REMOVED:\t" + str(item))
        except ValueError:
            self.error("[ITEM]" + str(item) + " doesn't exist")

    def has(self, item):
        return self.table[item.pos].__len__() > 0


if __name__ == '__main__':
    table = HashTable()
    songs = [
        mh.Data('A Real Life Happily Ever After', 'bCgjhkl08', 'Cast of Galavant', 34, 5, 45),
        mh.Data('Whatever Happened to My Part', 'hgIG1Jlk0', 'Quinn Thomashow', 356, 1, 145),
        mh.Data('Skinny Love', 'ghk1245UP', 'Quinn Thomashow', 1466, 224, 1352),
        mh.Data('Jackass in a Can', '45TYGkjkk', 'Cast of Galavant', 5354, 132, 15316)
    ]
    for song in songs:
        table.put(song.Artist, song)

    table.remove(mh.Data('Jackass in a Can', '45TYGkjkk', 'Cast of Galavant', 5354, 132, 15316))

    print(table.__str__())
