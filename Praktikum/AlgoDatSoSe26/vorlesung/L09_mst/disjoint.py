

class DisjointValue():

    def __init__(self, value):
        self.value = value
        self.parent = None

    def canonical(self):
        if self.parent:
            return self.parent.canonical()
        return self

    def same_set(self, other):
        return self.canonical() == other.canonical()

    def union(self, other):
        self.canonical().parent = other.canonical()
