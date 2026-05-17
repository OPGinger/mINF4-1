"""
Daniel Baer
17.05.2026

mINF4/1, V05, "B-Baum"

V05_03.py

this application implements an experiment to analyze the disk I/O behavior of B-Trees with different orders (m).
It defines a function that generates a random sequence of 500 unique integers and inserts them into B-Trees of various orders while collecting metrics such as tree height, number of comparisons, and disk loads/saves.
The results are plotted using Matplotlib to visualize how the order of the B-Tree affects its performance characteristics.

"""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path
from datetime import datetime

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

TASK_DIR = Path(__file__).resolve().parent
PRAKTIKUM_DIR = TASK_DIR.parent.parent
ALGODAT_DIR = PRAKTIKUM_DIR / "AlgoDatSoSe26"
BTREE_DIR = ALGODAT_DIR / "vorlesung" / "L06_b_baeume"

sys.path.insert(0, str(ALGODAT_DIR))
sys.path.insert(0, str(BTREE_DIR))

from utils.algo_context import AlgoContext  # type: ignore[import-not-found]
from b_tree import BTree  # type: ignore[import-not-found]
from b_tree_node import BTreeNode  # type: ignore[import-not-found]
from utils.algo_int import Int  # type: ignore[import-not-found]

def collect_nodes(tree: BTree) -> list[BTreeNode]:
    """Collect all unique BTreeNode objects in the tree via DFS."""
    nodes: list[BTreeNode] = []
    seen = set()

    def walk(node) -> None:
        if node is None:
            return
        if not isinstance(node, BTreeNode):
            raise TypeError(f"Unexpected child type in tree: {type(node)} (value={node})")
        marker = id(node)
        if marker in seen:
            return
        seen.add(marker)
        nodes.append(node)
        if node.leaf:
            return
        for idx in range(node.n + 1):
            walk(node.children[idx])

    walk(tree.root)
    
    return nodes

def save_plot(rows: list[dict[str, float]]) -> None:
    """ collect data for plotting from the results """
    ms = [int(row["m"]) for row in rows]
    heights = [float(row["height"]) for row in rows]
    comparisons = [float(row["comparisons"]) for row in rows]
    loaded = [float(row["loaded"]) for row in rows]
    saved = [float(row["saved"]) for row in rows]

    """ create subplots for each metric vs order m """
    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    flat = list(axes.flat)

    """ create plots for height, comparisons, loaded count, and saved count vs order m """
    flat[0].plot(ms, heights, marker="o")
    flat[0].set_title("Tree Height")
    flat[0].set_xlabel("Order m")
    flat[0].set_ylabel("Height")
    flat[0].grid(True)

    flat[1].plot(ms, comparisons, marker="o")
    flat[1].set_title("Comparisons")
    flat[1].set_xlabel("Order m")
    flat[1].set_ylabel("Comparisons")
    flat[1].grid(True)

    flat[2].plot(ms, loaded, marker="o")
    flat[2].set_title("Disk-Loads")
    flat[2].set_xlabel("Order m")
    flat[2].set_ylabel("Loaded Count")
    flat[2].grid(True)

    flat[3].plot(ms, saved, marker="o")
    flat[3].set_title("Disk-Saves")
    flat[3].set_xlabel("Order m")
    flat[3].set_ylabel("Saved Count")
    flat[3].grid(True)

    fig.tight_layout()
    fig.savefig(TASK_DIR / "V05_03_plots.png")
    plt.close(fig)



def main() -> None:
    """ orders to test """
    orders = [2, 3, 5, 10, 20]
    
    """ random seed based on current timestamp to generate a sequence of values """
    seed = int(datetime.now().timestamp())
    rnd = random.Random(seed)
    
    """ generate a random sequence of 500 unique integers in the range -500 to 500 """
    values = rnd.sample(range(-500, 500), 500)
    
    output: list[dict[str, float]] = []

    """ run the experiment for each order m and collect results """
    for m in orders:
        ctx = AlgoContext()
        tree = BTree(m, ctx)
        
        """ insert all values into the B-Tree """
        for value in values:
            tree.insert(value)

        """ collect all nodes in the tree to sum up loaded and saved counts """
        nodes = collect_nodes(tree)
        loaded_total = sum(n.loaded_count for n in nodes)
        saved_total = sum(n.saved_count for n in nodes)

        """ append the results for the current order m to the output list """
        output.append(
            {
                "m": m,
                "height": tree.height(),
                "comparisons": ctx.comparisons,
                "loaded": loaded_total,
                "saved": saved_total,
            }
        )
    
    """ save the collected results and generate the plot """
    save_plot(output)
    
    """ print the results """
    for row in output:
        print(
            f"Order={int(row['m']):<3}: height={int(row['height']):<2}, comparisons={int(row['comparisons']):<5}, "
            f"loads={int(row['loaded']):<5}, saves={int(row['saved']):<5}"
        )


if __name__ == "__main__":
    main()
