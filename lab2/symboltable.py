class HashTableSymbolTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * size

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        if self.table[index] is None:
            self.table[index] = []
        self.table[index].append((key, value))

    def lookup(self, key):
        index = self._hash(key)
        if self.table[index] is not None:
            for k, v in self.table[index]:
                if k == key:
                    return v
        return None

    def delete(self, key):
        index = self._hash(key)
        if self.table[index] is not None:
            for item in self.table[index]:
                if item[0] == key:
                    self.table[index].remove(item)

    def display(self):
        return self.table


a = HashTableSymbolTable()
a.insert(0, 30)
a.insert(0, 50)
a.insert(2, 50)
print(a.lookup(0))
a.delete(2)
a.insert("dog", 20)
print(a.display())
