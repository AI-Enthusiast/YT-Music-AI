import random

from Music import MusicHashTable as mh


class HashTable:

    # Constructor
    def __init__(self, CAP=1000):
        self.size = 0
        self.capacity = CAP
        self.table = []
        self.seed = 37
        for i in range(self.capacity):
            self.table.append([])
        self.resize = 2
        self.values = []
        self.keys = []
        self.rehashed = 0

    # TODO return string instead of printing
    # toString()
    def __str__(self):
        for i in range(self.capacity):
            if self.table[i]:
                print("ARTIST: " + self.table[i][0].Artist)
                for j in self.table[i]:
                    print(j.__str__())
        print(self.capacity)
        print(self.size)

    # a hashing functionality
    def h1(self, key):
        return hash(key) % self.capacity

    # needed for doubleHashing algorithm
    def h2(self, key):
        return hash(key) % self.seed

    # tells the program when to double hash and when to rehash
    def cutoff(self):
        if self.keys.__len__() >= self.capacity * .8:
            print(self.keys.__len__())
            return True
        else:
            return False

    # method to resolve collision by quadratic probing method
    def doubleHashing(self, key):
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
        return posFound, newPosition

    def get(self, key):
        if self.table[self.h1(key)] == []:  # if the fist location of hash is blank
            return None
        elif self.table[self.h1(key)][0].Artist == key:  # if the first location is the entry is the same
            return self.table[self.h1(key)]
        else:  # else cycle to next artist place
            pos = self.search(key)
            return self.table[pos]

    # method that searches for an element in the table
    # returns position of element if found
    # else returns False
    def search(self, key):
        found = False
        position = self.h1(key)
        if self.table[position][0].Artist == key:
            return position
        # if element is not found at position returned hash function
        # then we search element using double hashing
        else:
            limit = 50
            i = 2
            newPosition = position
            # start a loop to find the position
            while i <= limit:
                # calculate new position by double Hashing
                position = (i * self.h1(key) + self.h2(key)) % self.size
                # if element at newPosition is equal to the required element
                if self.table[position][0].Artist == key:
                    found = True
                    break
                elif self.table[position] == []:
                    found = False
                    break
                else:
                    # as the position is not empty increase i
                    i += 1
            if found:
                return position
            else:
                print("Element not Found")
                return found

    def rehash(self):
        # increases the number of artists
        self.capacity *= self.resize
        self.rehashed += 1
        print("Rehashing... capacity is now " + str(self.capacity))
        # resets all other vars
        self.table = [[] for i in range(0, self.capacity)]
        vals = self.values
        self.values = []
        self.keys = []
        self.size = 0
        self.seed = random.randint(7, 41)
        for value in vals:
            self.put(value.Artist, value)

    def put(self, key, value):
        location = self.h1(key)
        if self.table[location] == []:  # if the desired location in the hashtable is empty
            self.table[location].append(value)  # add the Data object to the list
            # upkeep
            self.size += 1
            self.values.append(value)
            self.keys.append(key)
        elif self.table[location][0].Artist == key:  # that artist already exists in the table
            self.table[location].append(value)
            value.pos = location
            # upkeep
            self.size += 1
            self.values.append(value)
        elif self.keys.__len__() >= self.capacity * 0.8:
            print(self.capacity * 0.8)  # if the table is too full and needs to be rehashed
            self.rehash()
            self.put(key, value)
        else:  # there needs to be a second try (aka double hash it, baby!)
            poss = self.doubleHashing(key)
            newPos = poss[1]
            value.pos = newPos
            self.table[newPos] = [value]
            # upkeep
            self.size += 1
            self.values.append(value)
            self.keys.append(key)

    def remove(self, key, value=None):
        pos = self.search(key)
        if value:
            value = self.get(key)
            idx = self.table[pos].index(value)
            removed = self.table[pos].pop(idx)
            self.values.remove(value)
        else:
            for i in self.table[pos]:
                self.values.remove(i)
            self.table[pos] = []
            removed = True
        self.keys.remove(key)
        self.size -= 1
        if self.size != 0:
            self.rehash()
        return removed

    def has(self, key):
        if self.search(key) is not False:
            return True
        else:
            return False


if __name__ == '__main__':
    table = HashTable(1000)
    songs = [
        mh.Data('A Real Life Happily Ever After', 'bCgjhkl08', 'Cast of Galavant', 34, 5, 45),
        mh.Data('Whatever Happened to My Part', 'hgIG1Jlk0', 'Quinn Thomashow', 356, 1, 145),
        mh.Data('Skinny Love', 'ghk1245UP', 'Quinn Thomashow', 1466, 224, 1352),
        mh.Data('Jackass in a Can', '45TYGkjkk', 'Cast of Galavant', 5354, 132, 15316)
    ]
    for song in songs:
        table.put(song.Artist, song)
    table.remove('Cast of Galavant',
                 value=mh.Data('Jackass in a Can', '45TYGkjkk', 'Cast of Galavant', 5354, 132, 15316))
    print(table.__str__())
