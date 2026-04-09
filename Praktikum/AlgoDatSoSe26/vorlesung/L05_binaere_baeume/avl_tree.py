from vorlesung.L05_binaere_baeume.avl_tree_node import AVLTreeNode
from vorlesung.L05_binaere_baeume.bin_tree import BinaryTree
from utils.algo_context import AlgoContext
from utils.algo_array import Array


class AVLTree(BinaryTree):

    def __init__(self, ctx: AlgoContext):
        super().__init__(ctx)

    def new_node(self, value):
        return AVLTreeNode(value, self.ctx)

    def balance(self, node: AVLTreeNode):
        node.update_balance()
        if node.balance == -2:
            if node.left.balance <= 0:
                node = node.right_rotate()
            else:
                node = node.left_right_rotate()
        elif node.balance == 2:
            if node.right.balance >= 0:
                node = node.left_rotate()
            else:
                node = node.right_left_rotate()
        if node.parent:
            self.balance(node.parent)
        else:
            self.root = node

    def insert(self, value):
        insert_generator = self.insert_stepwise(value)
        node, parent = None, None
        while True:
            try:
                node, parent = next(insert_generator)
            except StopIteration:
                break
        return node, parent

    def insert_stepwise(self, value):
        node, parent = super().insert(value)
        yield None, None
        node.parent = parent
        if parent:
            self.balance(parent)
        return node, parent

    def delete(self, value):
        node, parent = super().delete(value)
        if node:
            node.parent = parent
        if parent:
            self.balance(parent)

    def graph_filename(self):
        return "AVLTree"


if __name__ == "__main__":
    ctx = AlgoContext()
    tree = AVLTree(ctx)

    values = Array.from_file("data/seq2.txt", ctx)
    for cell in values:
        tree.insert(cell.value)

    def print_node(node, indent=0, level=0):
        print((indent * 3) * " ", node.value)

    print("In-order traversal:")
    tree.in_order_traversal(print_node)
    print("\nTree structure traversal:")
    tree.tree_structure_traversal(print_node)

    tree.insert(9)
    print("\nDeleting 5:")
    tree.delete(5)
    print("In-order traversal after deletion:")
    tree.in_order_traversal(print_node)
