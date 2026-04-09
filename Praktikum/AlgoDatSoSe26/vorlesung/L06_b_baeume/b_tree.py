from utils.algo_context import AlgoContext
from utils.algo_array import Array
from utils.algo_int import Int
from b_tree_node import BTreeNode


class BTree:

    def __init__(self, m: int, ctx: AlgoContext):
        self.m = m
        self.ctx = ctx
        self.root = BTreeNode(m, ctx)

    def _new_node(self):
        return BTreeNode(self.m, self.ctx)

    def search(self, value, start: BTreeNode = None) -> BTreeNode | None:
        if not start:
            start = self.root
        start.load()
        if not isinstance(value, Int):
            value = Int(value, self.ctx)
        i = 0
        while i < start.n and value > start.value[i]:
            i += 1
        if i < start.n and value == start.value[i]:
            return start
        if start.leaf:
            return None
        return self.search(value, start.children[i])

    def split_child(self, parent: BTreeNode, i: int):
        child = parent.children[i]
        child.load()
        h = self._new_node()
        h.leaf = child.leaf
        h.n = self.m - 1
        for j in range(self.m - 1):
            h.value[j] = child.value[j + self.m]
        if not h.leaf:
            for j in range(self.m):
                h.children[j] = child.children[j + self.m]
            for j in range(self.m, child.n + 1):
                child.children[j] = None
        child.n = self.m - 1
        child.save()
        h.save()
        for j in range(parent.n, i, -1):
            parent.children[j + 1] = parent.children[j]
            parent.value[j] = parent.value[j - 1]
        parent.children[i + 1] = h
        parent.value[i] = child.value[self.m - 1]
        parent.n += 1
        parent.save()

    def insert(self, value):
        if not isinstance(value, Int):
            value = Int(value, self.ctx)
        r = self.root
        if r.n == 2 * self.m - 1:
            h = self._new_node()
            self.root = h
            h.leaf = False
            h.n = 0
            h.children[0] = r
            self.split_child(h, 0)
            self.insert_in_node(h, value)
        else:
            self.insert_in_node(r, value)

    def insert_in_node(self, start: BTreeNode, value: Int):
        start.load()
        i = start.n
        if start.leaf:
            while i >= 1 and value < start.value[i - 1]:
                start.value[i] = start.value[i - 1]
                i -= 1
            start.value[i] = value
            start.n += 1
            start.save()
        else:
            j = 0
            while j < start.n and value > start.value[j]:
                j += 1
            if start.children[j].n == 2 * self.m - 1:
                self.split_child(start, j)
                if value > start.value[j]:
                    j += 1
            self.insert_in_node(start.children[j], value)

    def traversal(self, callback):
        def _rec(node, callback):
            i = 0
            while i < node.n:
                if not node.leaf:
                    _rec(node.children[i], callback)
                callback(node.value[i])
                i += 1
            if not node.leaf:
                _rec(node.children[i], callback)
        _rec(self.root, callback)

    def walk(self):
        self.traversal(lambda key: print(key, end=" "))

    def height(self, start: BTreeNode = None):
        if not start:
            start = self.root
        if start.leaf:
            return 0
        return 1 + self.height(start.children[0])


if __name__ == "__main__":
    ctx = AlgoContext()
    a = Array.from_file("data/seq3.txt", ctx)
    tree = BTree(3, ctx)
    for cell in a:
        tree.insert(cell)
    print(f"Height: {tree.height()}")
    tree.walk()
    s = tree.search(0)
    print(f"\nKnoten mit 0: {str(s)}")
