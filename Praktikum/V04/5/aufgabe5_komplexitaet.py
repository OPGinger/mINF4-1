"""
Daniel Baer
09.05.2026

mINF4/1, V04, Task 5 "Complexity Analysis"

aufgabe5_komplexitaet.py

This script compares insertion complexity by counting comparisons for:
- BST with sorted input (worst case)
- BST with random input (average case)
- AVL with sorted input (self-balancing)

It generates a plot and writes measured values plus interpretation.
"""

import random
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Resolve local directories relative to this task folder.
TASK_DIR = Path(__file__).resolve().parent
V04_DIR = TASK_DIR.parent
ALGODAT_DIR = V04_DIR.parent / "AlgoDatSoSe26"

# Add lecture project to import path.
sys.path.insert(0, str(ALGODAT_DIR))

from utils.algo_context import AlgoContext  # type: ignore[import-not-found]
from vorlesung.L05_binaere_baeume.bin_tree import BinaryTree  # type: ignore[import-not-found]
from vorlesung.L05_binaere_baeume.avl_tree import AVLTree  # type: ignore[import-not-found]


def build_bst(values: list[int]) -> int:
    """Build BST and return number of comparisons used for insertion."""
    ctx = AlgoContext()
    tree = BinaryTree(ctx)
    for value in values:
        tree.insert(value)
    return ctx.comparisons


def build_avl(values: list[int]) -> int:
    """Build AVL tree and return number of comparisons used for insertion."""
    ctx = AlgoContext()
    tree = AVLTree(ctx)
    for value in values:
        tree.insert(value)
    return ctx.comparisons


def run_experiment(sizes: list[int]) -> tuple[list[int], list[int], list[int]]:
    """Run all three complexity scenarios for each input size."""
    bst_sorted: list[int] = []
    bst_random: list[int] = []
    avl_sorted: list[int] = []

    for n in sizes:
        sorted_values = list(range(1, n + 1))
        rnd = random.Random(42 + n)
        random_values = sorted_values[:]
        rnd.shuffle(random_values)

        bst_sorted.append(build_bst(sorted_values))
        bst_random.append(build_bst(random_values))
        avl_sorted.append(build_avl(sorted_values))

    return bst_sorted, bst_random, avl_sorted


def write_results(
    sizes: list[int],
    bst_sorted: list[int],
    bst_random: list[int],
    avl_sorted: list[int],
) -> None:
    """Write numeric results to text files for reproducibility."""
    table_lines = [
        "n,bst_sorted_comparisons,bst_random_comparisons,avl_sorted_comparisons"
    ]
    for n, bs, br, avl in zip(sizes, bst_sorted, bst_random, avl_sorted):
        table_lines.append(f"{n},{bs},{br},{avl}")

    (TASK_DIR / "messwerte.csv").write_text("\n".join(table_lines) + "\n", encoding="utf-8")

    interpretation = (
        "Task 5 - Complexity Analysis\n"
        "Measured metric: comparisons during insertion\n"
        "Scenarios:\n"
        "1) BST with sorted input (worst case)\n"
        "2) BST with random input (average case)\n"
        "3) AVL with sorted input (self-balancing)\n\n"
        "Interpretation:\n"
        "- BST(sorted) grows approximately quadratically over full build (sum of linear path lengths).\n"
        "- BST(random) grows slower, close to n*log(n) behavior in practice.\n"
        "- AVL(sorted) also stays near n*log(n) due to balancing rotations.\n"
    )
    (TASK_DIR / "antworten.txt").write_text(interpretation, encoding="utf-8")


def save_plot(
    sizes: list[int],
    bst_sorted: list[int],
    bst_random: list[int],
    avl_sorted: list[int],
) -> Path:
    """Create and save complexity comparison plot."""
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(sizes, bst_sorted, marker="o", label="BST sorted input")
    ax.plot(sizes, bst_random, marker="s", label="BST random input")
    ax.plot(sizes, avl_sorted, marker="^", label="AVL sorted input")

    ax.set_title("Task 5 - Insertion Complexity Comparison")
    ax.set_xlabel("n")
    ax.set_ylabel("comparisons")
    ax.grid(True)
    ax.legend()

    out_file = TASK_DIR / "komplexitaet_plot.png"
    fig.tight_layout()
    fig.savefig(out_file, dpi=150)
    plt.close(fig)
    return out_file


def main() -> None:
    sizes = list(range(50, 551, 50))
    bst_sorted, bst_random, avl_sorted = run_experiment(sizes)
    write_results(sizes, bst_sorted, bst_random, avl_sorted)
    plot_file = save_plot(sizes, bst_sorted, bst_random, avl_sorted)

    print("Task 5 finished.")
    print(f"Plot: {plot_file}")
    print(f"Last row (n={sizes[-1]}):")
    print(f"BST sorted comparisons: {bst_sorted[-1]}")
    print(f"BST random comparisons: {bst_random[-1]}")
    print(f"AVL sorted comparisons: {avl_sorted[-1]}")


if __name__ == "__main__":
    main()
