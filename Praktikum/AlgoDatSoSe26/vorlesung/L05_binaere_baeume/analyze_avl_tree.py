from utils.algo_context import AlgoContext
from utils.algo_array import Array
from vorlesung.L05_binaere_baeume.avl_tree import AVLTree


def analyze_complexity(sizes):
    ctx = AlgoContext()
    for size in sizes:
        z = Array.random(size, -100, 100, ctx)
        tree = AVLTree(ctx)
        for i in range(size - 1):
            tree.insert(z[i].value)
        ctx.reset()
        tree.insert(z[size - 1].value)
        ctx.save_stats(size)

    ctx.plot_stats(["comparisons"])


if __name__ == "__main__":
    sizes = range(1, 1001, 2)
    analyze_complexity(sizes)
