"""
Daniel Baer
10.05.2026

mINF4/1, V04, Task 5 "Complexity Analysis"

aufgabe5_komplexitaet.py

This script measures search comparisons on already built trees for n = 10, 100, 500.
Scenarios:
- random Binary Search Tree
- sorted Binary Search Tree
- sorted AVL Tree

Only successful searches are measured (searching all inserted keys once).
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


def build_bst(values: list[int], ctx: AlgoContext) -> BinaryTree:
    """Build and return a BST with the provided insertion order."""
    tree = BinaryTree(ctx)
    for value in values:
        tree.insert(value)
    return tree


def build_avl(values: list[int], ctx: AlgoContext) -> AVLTree:
    """Build and return an AVL tree with the provided insertion order."""
    tree = AVLTree(ctx)
    for value in values:
        tree.insert(value)
    return tree


def count_search_comparisons(tree, ctx: AlgoContext, search_values: list[int]) -> tuple[int, float]:
    """Measure comparisons for successful searches in an already finished tree."""
    ctx.reset()
    for value in search_values:
        tree.search(value)
    total = ctx.comparisons
    avg = total / len(search_values) if search_values else 0.0
    return total, avg


def run_experiment(sizes: list[int]) -> list[dict[str, float]]:
    """Run all required scenarios for each n and return measured metrics."""
    rows: list[dict[str, float]] = []

    for n in sizes:
        sorted_values = list(range(1, n + 1))
        rnd = random.Random(1000 + n)
        random_values = sorted_values[:]
        rnd.shuffle(random_values)

        # Scenario 1: random BST
        ctx_random_bst = AlgoContext()
        random_bst = build_bst(random_values, ctx_random_bst)
        random_bst_total, random_bst_avg = count_search_comparisons(
            random_bst, ctx_random_bst, sorted_values
        )

        # Scenario 2: sorted BST
        ctx_sorted_bst = AlgoContext()
        sorted_bst = build_bst(sorted_values, ctx_sorted_bst)
        sorted_bst_total, sorted_bst_avg = count_search_comparisons(
            sorted_bst, ctx_sorted_bst, sorted_values
        )

        # Scenario 3: sorted AVL
        ctx_sorted_avl = AlgoContext()
        sorted_avl = build_avl(sorted_values, ctx_sorted_avl)
        sorted_avl_total, sorted_avl_avg = count_search_comparisons(
            sorted_avl, ctx_sorted_avl, sorted_values
        )

        rows.append(
            {
                "n": n,
                "random_bst_total": random_bst_total,
                "random_bst_avg": random_bst_avg,
                "sorted_bst_total": sorted_bst_total,
                "sorted_bst_avg": sorted_bst_avg,
                "sorted_avl_total": sorted_avl_total,
                "sorted_avl_avg": sorted_avl_avg,
            }
        )

    return rows


def write_results(rows: list[dict[str, float]]) -> None:
    """Write numeric table and concise interpretation to files."""
    header = (
        "n,"
        "random_bst_total,random_bst_avg,"
        "sorted_bst_total,sorted_bst_avg,"
        "sorted_avl_total,sorted_avl_avg"
    )
    lines = [header]
    for row in rows:
        lines.append(
            f"{int(row['n'])},"
            f"{int(row['random_bst_total'])},{row['random_bst_avg']:.4f},"
            f"{int(row['sorted_bst_total'])},{row['sorted_bst_avg']:.4f},"
            f"{int(row['sorted_avl_total'])},{row['sorted_avl_avg']:.4f}"
        )

    (TASK_DIR / "messwerte.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")

    answer_lines = [
        "Task 5 - Search Comparison Counts",
        "Measured metric: comparisons during successful search in already built trees",
        "Sizes: n = 10, 100, 500",
        "Scenarios: random BST, sorted BST, sorted AVL",
        "",
    ]
    for row in rows:
        answer_lines.extend(
            [
                f"n = {int(row['n'])}",
                f"- random BST: total = {int(row['random_bst_total'])}, avg = {row['random_bst_avg']:.4f}",
                f"- sorted BST: total = {int(row['sorted_bst_total'])}, avg = {row['sorted_bst_avg']:.4f}",
                f"- sorted AVL: total = {int(row['sorted_avl_total'])}, avg = {row['sorted_avl_avg']:.4f}",
                "",
            ]
        )
    answer_lines.extend(
        [
            "Interpretation:",
            "- sorted BST search comparisons grow strongly because the tree degenerates.",
            "- random BST stays clearly lower.",
            "- sorted AVL remains near logarithmic search depth due to balancing.",
        ]
    )
    (TASK_DIR / "antworten.txt").write_text("\n".join(answer_lines) + "\n", encoding="utf-8")


def save_plot(rows: list[dict[str, float]]) -> Path:
    """Create a line plot for total search comparisons over n."""
    sizes = [int(row["n"]) for row in rows]
    random_bst_total = [int(row["random_bst_total"]) for row in rows]
    sorted_bst_total = [int(row["sorted_bst_total"]) for row in rows]
    sorted_avl_total = [int(row["sorted_avl_total"]) for row in rows]

    fig = plt.figure(figsize=(9, 5))
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(sizes, random_bst_total, marker="o", label="random BST")
    ax.plot(sizes, sorted_bst_total, marker="s", label="sorted BST")
    ax.plot(sizes, sorted_avl_total, marker="^", label="sorted AVL")

    ax.set_title("Task 5 - Search Comparisons")
    ax.set_xlabel("n")
    ax.set_ylabel("total comparisons for searching all n keys")
    ax.grid(True)
    ax.legend()

    out_file = TASK_DIR / "komplexitaet_plot.png"
    fig.tight_layout()
    fig.savefig(out_file, dpi=150)
    plt.close(fig)
    return out_file


def main() -> None:
    sizes = [10, 100, 500]
    rows = run_experiment(sizes)
    write_results(rows)
    plot_file = save_plot(rows)

    print("Task 5 finished.")
    print("Search comparisons measured for finished trees.")
    print(f"Plot: {plot_file}")
    for row in rows:
        print(f"n = {int(row['n'])}")
        print(f"  random BST total: {int(row['random_bst_total'])}")
        print(f"  sorted BST total: {int(row['sorted_bst_total'])}")
        print(f"  sorted AVL total: {int(row['sorted_avl_total'])}")


if __name__ == "__main__":
    main()
