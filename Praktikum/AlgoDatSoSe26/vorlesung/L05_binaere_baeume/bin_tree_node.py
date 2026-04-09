from utils.algo_int import Int
from utils.algo_context import AlgoContext


class BinaryTreeNode(Int):
    """
    Knoten eines binären Suchbaums.

    Erbt von Int – Vergleiche zwischen Knoten werden automatisch im
    AlgoContext gezählt.
    """

    def __init__(self, value, ctx: AlgoContext):
        super().__init__(value, ctx)
        self.left = None
        self.right = None

    def height(self):
        left_height  = self.left.height()  if self.left  else 0
        right_height = self.right.height() if self.right else 0
        return 1 + max(left_height, right_height)

    def __repr__(self):
        return f"TreeNode(value={self.value}, left={self.left}, right={self.right})"

    def __str__(self):
        return str(self.value)

    def graphviz_rep(self, row, col, dot):
        dot.node(str(id(self)), label=str(self.value), pos=f"{col},{-row}!")
