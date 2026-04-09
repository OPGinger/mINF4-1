from vorlesung.L05_binaere_baeume.bin_tree_node import BinaryTreeNode
from utils.algo_context import AlgoContext
from utils.algo_path import path
from datetime import datetime
import graphviz


class BinaryTree:

    def __init__(self, ctx: AlgoContext):
        self.root = None
        self.size = 0
        self.ctx = ctx

    def new_node(self, value):
        return BinaryTreeNode(value, self.ctx)

    def insert(self, value):
        self.size += 1
        value = self.new_node(value)
        if self.root is None:
            self.root = value
            return self.root, None
        else:
            current = self.root
            while True:
                if value < current:
                    if current.left:
                        current = current.left
                    else:
                        current.left = value
                        return current.left, current
                elif value >= current:
                    if current.right:
                        current = current.right
                    else:
                        current.right = value
                        return current.right, current
                else:
                    return None, None

    def search(self, value):
        current = self.root
        value = self.new_node(value)
        while current:
            if value < current:
                current = current.left
            elif value > current:
                current = current.right
            else:
                return current
        return None

    def delete(self, value):
        parent = None
        current = self.root
        value = self.new_node(value)
        while current:
            if value < current:
                parent = current
                current = current.left
            elif value > current:
                parent = current
                current = current.right
            else:
                break
        else:
            return None, None
        return self.delete_node(current, parent)

    def delete_node(self, current, parent):
        self.size -= 1
        # Fall 3: zwei Kinder → Nachfolger suchen
        if current.left and current.right:
            parent = current
            successor = current.right
            while successor.left:
                parent = successor
                successor = successor.left
            current.set(successor)   # Wert kopieren (1 read + 1 write)
            current = successor

        child = current.left if current.left else current.right

        if not parent:
            self.root = child
            return child, None
        elif parent.left is current:
            parent.left = child
            return child, parent
        else:
            parent.right = child
            return child, parent

    def in_order_traversal(self, callback):
        def _rec(callback, current):
            if current is not None:
                _rec(callback, current.left)
                callback(current)
                _rec(callback, current.right)
        _rec(callback, self.root)

    def level_order_traversal(self, callback):
        if self.root is None:
            return
        queue = [(self.root, 0)]
        while queue:
            current, level = queue.pop(0)
            callback(current, level)
            if current.left  is not None: queue.append((current.left,  level + 1))
            if current.right is not None: queue.append((current.right, level + 1))

    def tree_structure_traversal(self, callback):
        def _rec(callback, current, level):
            nonlocal line
            if current:
                _rec(callback, current.left, level + 1)
                callback(current, level, line)
                line += 1
                _rec(callback, current.right, level + 1)
        line = 0
        _rec(callback, self.root, 0)

    def graph_filename(self):
        return "BinaryTree"

    def graph_traversal(self):
        def define_node(node, level, line):
            nonlocal dot
            if node is not None:
                node.graphviz_rep(level, line, dot)

        def _rec(current):
            nonlocal dot
            if current is not None:
                if current.left:
                    dot.edge(str(id(current)), str(id(current.left)))
                    _rec(current.left)
                if current.right:
                    dot.edge(str(id(current)), str(id(current.right)))
                    _rec(current.right)

        dot = graphviz.Digraph(
            name="BinaryTree",
            engine="neato",
            node_attr={"shape": "circle", "fontname": "Arial"},
            format="pdf")
        self.tree_structure_traversal(define_node)
        _rec(self.root)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dot.render(path(f"{self.graph_filename()}_{timestamp}.gv"))


if __name__ == "__main__":
    ctx = AlgoContext()
    tree = BinaryTree(ctx)
    for v in [5, 3, 7, 2, 4, 6, 5, 8]:
        tree.insert(v)

    def print_node(node, indent=0, line=None):
        print((indent * 3) * " ", node.value)

    print("In-order traversal:")
    tree.in_order_traversal(print_node)
    print("\nLevel-order traversal:")
    tree.level_order_traversal(print_node)

    print("\nDeleting 5:")
    tree.delete(5)
    print("In-order traversal after deletion:")
    tree.in_order_traversal(print_node)

    print("\n", ctx)
