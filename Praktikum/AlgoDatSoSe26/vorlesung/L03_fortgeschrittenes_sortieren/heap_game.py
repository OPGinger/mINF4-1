import random
import pygame
from utils.algo_game import Game
from utils.algo_context import AlgoContext
from utils.algo_array import Array
from heap_sorting import heap_sort_stepwise

WHITE = (255, 255, 255)
BLUE  = (0,   0, 255)


class HeapGame(Game):

    def __init__(self):
        super().__init__("Heap Game", fps=20, size=(400, 400))
        random.seed()
        l = list(range(1, 101))
        random.shuffle(l)
        self.ctx = AlgoContext()
        self.z = Array(l, self.ctx)
        self.finished = False
        self.sort_generator = heap_sort_stepwise(self.z, self.ctx)

    def update_game(self):
        if not self.finished:
            try:
                next(self.sort_generator)
            except StopIteration:
                self.finished = True
        return True

    def draw_game(self):
        self.screen.fill(WHITE)
        for i, cell in enumerate(self.z):
            x = 50 + i * 3
            y = 350 - cell.value * 3
            pygame.draw.rect(self.screen, BLUE, (x, y, 3, 3))
        super().draw_game()


if __name__ == "__main__":
    sort_game = HeapGame()
    sort_game.run()
