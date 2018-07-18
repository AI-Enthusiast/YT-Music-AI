import random
import _md5

def error(errorMessage):
    print(">ERROR:\t" + str(errorMessage))

def force_to_unicode(text):
    return text if isinstance(text, bytes) else text.encode('utf8')
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
        self.doubleHashed = 0

    # toString()
    def __str__(self):
        tab = ""
        for i in range(self.capacity):
            if self.table[i]: #if not an empty list
                tab += '[' + str(i) + '] '
                tab += "ARTIST: " + self.table[i][0].Artist + ' \n'
                for j in self.table[i]:
                    tab += '\t'
                    tab += j.__str__() + '\n'
        return tab

    # a hashing functionality
    def h1(self, key):
        return int(_md5.md5(force_to_unicode(key)).hexdigest(), 16) % self.capacity

    # needed for doubleHashing algorithm
    def h2(self, key):
        return int(_md5.md5(force_to_unicode(key)).hexdigest(), 16) % self.seed

    # tells the program when to double hash and when to rehash
    def cutoff(self):
        return(self.keys.__len__() > int(self.capacity*0.8))


    # method to resolve collision by quadratic probing method
    def doubleHashing(self, key):
        posFound = False
        limit = self.capacity * 0.8
        i = 2
        newPosition = 0
        while i <= limit:
            newPosition = (i * self.h1(key) + self.h2(key)) % self.capacity
            if self.table[newPosition] == []:
                posFound = True
                break
            else:
                i += 1
        self.doubleHashed += 1
        return posFound, newPosition

    def get(self, key):
        if self.table[self.h1(key)] == []:  # if the fist location of hash is blank
            return None
        elif self.table[self.h1(key)][0].Artist == key:  # if the first location is the entry is the same
            return self.table[self.h1(key)]
        else:  # else cycle to next artist place
            pos = self.search(key)
            return self.table[pos]

    # method that searches for an entry in the table
    # returns position of entry if found
    # else returns False
    def search(self, key):
        position = self.h1(key)
        if self.table[position][0].Artist == key:
            return position
        else:
            i = 0
            while i < self.table.__len__():
                position = (i * self.h1(key) + self.h2(key)) % self.capacity
                if not self.table[position]:
                    i += 1
                elif self.table[position][0].Artist == key:
                    return position
                else:
                    i += 1
            return False


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

    #TODO make tests more thorough
    def put(self, key, value):
        location = self.h1(key)
        if self.cutoff(): #if max size reached
            self.rehash()
            self.put(key, value)
        elif self.table[location] == []:  # if the desired location in the hashtable is empty
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
            if poss[0] is True: # if double hashing works
                newPos = poss[1]+1
                self.table[newPos] = [value]
                #   upkeep
                self.size += 1
                self.values.append(value)
                self.keys.append(key)
            else: #fail safe
                self.rehash()
                self.put(key, value)

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
    print(error("Please run from main.py"))

