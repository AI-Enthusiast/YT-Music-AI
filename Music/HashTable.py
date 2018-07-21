import random

random.seed(37)

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
            if self.table[i]:  # if not an empty list
                tab += '[' + str(i) + '] '
                tab += "ARTIST: " + self.table[i][0].Artist + ' \n'
                for j in self.table[i]:
                    tab += '\t'
                    tab += j.__str__() + '\n'
        return tab

    '''
    Quick note: smaller sized tables will result in an oscillating double hash
    value because of the current hash functions. However, we need constant hash functions, 
    so I'm not too mad about this right now. Important note though.
    
    One thing we could do would be to use random generators with a constant seed value to keep
    the numbers constant for testing. 
    '''
    def h0(self, key):
        sum = 0
        for char in key:
            sum += ord(char)
        return sum

    # a hashing functionality
    def h1(self, key):
        return self.h0(key) % self.capacity

    # needed for doubleHashing algorithm
    def h2(self, key):
        return self.h0(key) % self.seed

    # tells the program when to double hash and when to rehash
    def cutoff(self):
        return (self.keys.__len__() > int(self.capacity * 0.8))

    def quadProbe(self, key, i):
        return (i * self.h1(key) + self.h2(key)) % self.capacity

    # method to resolve collision by quadratic probing method
    def doubleHashing(self, key):
        posFound = False
        limit = self.capacity * 0.8
        i = 2
        newPosition = 0
        if self.keys.__contains__(key):
            posFound = self.search(key)
        while i <= limit:
            newPosition = self.quadProbe(key, i)
            if self.table[newPosition] == []:
                posFound = True
                break
            else:
                i += 1
        if posFound:
            self.doubleHashed += 1
        return posFound, newPosition

    def get(self, key):
        pos = self.search(key)
        if pos:
            return self.table[pos]
        else:
            return None

    # method that searches for an entry in the table
    # returns position of entry if found
    # else returns False
    def search(self, key):
        # maybe a more clear way to search would be to first create
        # an array of indices to search and then check each one
        lst = []

        if not self.keys.__contains__(key):
            return False
        lst.append(self.h1(key))
        for i in range(2, (self.capacity*80)//100):
            idx = self.quadProbe(key, i)
            if not lst.__contains__(idx):
                lst.append(idx)
        for j in lst:
            item = self.table[j]
            if item:
                if item[0].Artist == key:
                    return j
        return False

    def rehash(self):
        # increases the number of artists
        self.capacity *= self.resize
        self.rehashed += 1
        print(">INCREASING TABLE SIZE:\tNow " + str(self.capacity))
        # resets all other vars
        self.table = [[] for i in range(0, self.capacity)]
        vals = self.values
        self.values = []
        self.keys = []
        self.size = 0
        for value in vals:
            self.put(value.Artist, value)

    def put(self, key, value):
        location = self.h1(key)
        if self.cutoff():  # if max size reached
            self.rehash()
            self.put(key, value)
        elif not self.table[location]:  # if the desired location in the hashtable is empty
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
        else:  # there needs to be a second try (aka double hash it, baby!)
            poss = self.doubleHashing(key)
            if poss[0] is True:  # if double hashing works
                newPos = poss[1] + 1
                self.table[newPos] = [value]
                #   upkeep
                self.size += 1
                self.values.append(value)
                self.keys.append(key)
            else:  # fail safe
                self.rehash()
                self.put(key, value)

    def remove(self, key, value=None):
        pos = self.search(key)
        if not pos:
            return False
        if value:
            try:
                value = self.get(key)
                idx = self.table[pos].index(value)
                removed = self.table[pos].pop(idx)
                self.values.remove(value)
                self.size -= 1
            except ValueError:
                return False
        else:
            try:
                for i in self.table[pos]:
                    self.values.remove(i)
                self.table[pos] = []
                removed = True
                self.keys.remove(key)
                self.size -= 1
                if self.size != 0:
                    self.rehash()
            except ValueError:
                return False
        return removed

    def has(self, key):
        if self.search(key) is not False:
            return True
        else:
            return False


if __name__ == '__main__':
    print(error("Please run from main.py"))
