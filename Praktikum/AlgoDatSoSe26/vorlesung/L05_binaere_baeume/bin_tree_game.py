import random
import pygame
from utils.algo_game import Game
from utils.algo_context import AlgoContext
from bin_tree import BinaryTree

WHITE = (255, 255, 255)
BLUE  = (0,   0, 255)
BLACK = (0,   0,   0)
WIDTH, HEIGHT, MARGIN = 800, 400, 20


class BinTreeGame(Game):

    def __init__(self):
        super().__init__("BinTree Game", fps=10, size=(WIDTH, HEIGHT))
        random.seed()
        self.z = list(range(1, 101))
        random.shuffle(self.z)
        self.finished = False
        self.ctx = AlgoContext()
        self.tree = BinaryTree(self.ctx)
        self.tree.get_height = lambda node: (
            0 if node is None
            else 1 + max(self.tree.get_height(node.left), self.tree.get_height(node.right))
        )
        self.height = self.tree.get_height(self.tree.root)

    def update_game(self):
        if not self.finished:
            self.tree.insert(self.z.pop())
            self.height = self.tree.get_height(self.tree.root)
            if len(self.z) == 0:
                self.finished = True
        return True

    def draw_game(self):
        self.screen.fill(WHITE)
        if self.height > 0:
            self.draw_tree(self.tree.root, WIDTH // 2, MARGIN, WIDTH // 4 - MARGIN)
        super().draw_game()

    def draw_tree(self, node, x, y, x_offset):
        y_offset = (HEIGHT - 2 * MARGIN) / self.height
        if node is not None:
            pygame.draw.circle(self.screen, BLUE, (x, y), 2)
            if node.left is not None:
                pygame.draw.line(self.screen, BLACK, (x, y), (x - x_offset, y + y_offset))
                self.draw_tree(node.left, x - x_offset, y + y_offset, x_offset // 2)
            if node.right is not None:
                pygame.draw.line(self.screen, BLACK, (x, y), (x + x_offset, y + y_offset))
                self.draw_tree(node.right, x + x_offset, y + y_offset, x_offset // 2)


if __name__ == "__main__":
    tree_game = BinTreeGame()
    tree_game.run()
