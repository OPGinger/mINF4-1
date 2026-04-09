from utils.algo_context import AlgoContext
from utils.algo_array import Array
from b_tree import BTree
from b_tree_node import BTreeNode


def count_loads(root: BTreeNode) -> int:
    """Summiert load()-Aufrufe über alle Knoten des Baums."""
    if root is None:
        return 0
    total = root.loaded_count
    for child in root.children:
        if child is not None:
            total += count_loads(child)
    return total


def count_saves(root: BTreeNode) -> int:
    """Summiert save()-Aufrufe über alle Knoten des Baums."""
    if root is None:
        return 0
    total = root.saved_count
    for child in root.children:
        if child is not None:
            total += count_saves(child)
    return total


def analyze_complexity(sizes):
    ctx = AlgoContext()
    stats: dict[int, dict] = {}

    for size in sizes:
        ctx.reset()
        z = Array.random(size, -100, 100, ctx)
        tree = BTree(5, ctx)
        for i in range(size - 1):
            tree.insert(z[i])
        ctx.reset()
        tree.insert(z[size - 1])
        stats[size] = {
            "comparisons": ctx.comparisons,
            "writes":      ctx.writes,
            "loads":       count_loads(tree.root),
            "saves":       count_saves(tree.root),
        }

    # Einfaches Liniendiagramm über alle gespeicherten Metriken
    import matplotlib.pyplot as plt
    x = list(stats.keys())
    fig, axes = plt.subplots(len(stats[x[0]]), 1, figsize=(8, 12), sharex=True)
    for ax, label in zip(axes, stats[x[0]].keys()):
        ax.plot(x, [stats[k][label] for k in x], label=label)
        ax.set_ylabel(label)
        ax.legend()
    plt.xlabel("n")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    sizes = range(1, 1001, 2)
    analyze_complexity(sizes)
