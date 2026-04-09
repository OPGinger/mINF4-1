from vorlesung.L05_binaere_baeume.bin_tree_node import BinaryTreeNode
from utils.algo_context import AlgoContext


class AVLTreeNode(BinaryTreeNode):

    def __init__(self, value, ctx: AlgoContext):
        super().__init__(value, ctx)
        self.parent = None
        self.balance = 0   # plain int – Metadaten, kein Zähler

    def __repr__(self):
        return f"TreeNode(id={id(self)} value={self.value}, left={self.left}, right={self.right})"

    def graphviz_rep(self, row, col, dot):
        dot.node(str(id(self)), label=str(self.value), pos=f"{col},{-row}!", xlabel=str(self.balance))

    def update_balance(self):
        left_height  = self.left.height()  if self.left  else 0
        right_height = self.right.height() if self.right else 0
        self.balance = right_height - left_height

    def right_rotate(self):
        new_root = self.left
        new_root.parent = self.parent
        self.left = new_root.right
        if self.left:
            self.left.parent = self
        new_root.right = self
        self.parent = new_root
        if new_root.parent:
            if new_root.parent.left is self:
                new_root.parent.left = new_root
            else:
                new_root.parent.right = new_root
        self.update_balance()
        new_root.update_balance()
        return new_root

    def left_rotate(self):
        new_root = self.right
        new_root.parent = self.parent
        self.right = new_root.left
        if self.right:
            self.right.parent = self
        new_root.left = self
        self.parent = new_root
        if new_root.parent:
            if new_root.parent.left is self:
                new_root.parent.left = new_root
            else:
                new_root.parent.right = new_root
        self.update_balance()
        new_root.update_balance()
        return new_root

    def right_left_rotate(self):
        self.right = self.right.right_rotate()
        return self.left_rotate()

    def left_right_rotate(self):
        self.left = self.left.left_rotate()
        return self.right_rotate()
