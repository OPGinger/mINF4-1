"""
Daniel Baer
09.05.2026

mINF4/1, V04, Task 2 "Traversals"

aufgabe2_traversierung.py

This script builds a Binary Search Tree and outputs traversal orders:
in-order, pre-order, post-order, and level-order.
"""

import sys
from pathlib import Path

# Resolve local directories relative to this task folder.
TASK_DIR = Path(__file__).resolve().parent
V04_DIR = TASK_DIR.parent
ALGODAT_DIR = V04_DIR.parent / "AlgoDatSoSe26"

# Add the lecture project path so imports from AlgoDatSoSe26 work from this folder.
sys.path.insert(0, str(ALGODAT_DIR))

from utils.algo_context import AlgoContext  # type: ignore[import-not-found]
from vorlesung.L05_binaere_baeume.bin_tree import BinaryTree  # type: ignore[import-not-found]


def load_seq0() -> list[int]:
    """Read seq0 values from shared data folder."""
    seq_file = ALGODAT_DIR / "data" / "seq0.txt"
    with seq_file.open("r", encoding="utf-8") as f:
        return [int(line.strip()) for line in f if line.strip()]


def build_tree(values: list[int]) -> BinaryTree:
    """Build tree by insertion order."""
    ctx = AlgoContext()
    tree = BinaryTree(ctx)
    for value in values:
        tree.insert(value)
    return tree


def pre_order(node, out: list[int]) -> None:
    """Pre-order traversal: Root, Left, Right."""
    if node is None:
        return
    out.append(node.value)
    pre_order(node.left, out)
    pre_order(node.right, out)


def post_order(node, out: list[int]) -> None:
    """Post-order traversal: Left, Right, Root."""
    if node is None:
        return
    post_order(node.left, out)
    post_order(node.right, out)
    out.append(node.value)


def run_traversals(tree: BinaryTree) -> dict[str, list[int]]:
    """Collect all traversal orders into a dictionary."""
    in_order_values: list[int] = []
    level_order_values: list[int] = []
    pre_order_values: list[int] = []
    post_order_values: list[int] = []

    tree.in_order_traversal(lambda node: in_order_values.append(node.value))
    tree.level_order_traversal(lambda node, _level: level_order_values.append(node.value))
    pre_order(tree.root, pre_order_values)
    post_order(tree.root, post_order_values)

    return {
        "in_order": in_order_values,
        "pre_order": pre_order_values,
        "post_order": post_order_values,
        "level_order": level_order_values,
    }


def write_outputs(values: list[int], traversals: dict[str, list[int]]) -> None:
    """Write traversal outputs for grading and readability."""
    out_txt = TASK_DIR / "traversierung_ausgabe.txt"
    out_txt.write_text(
        "Task 2 - Traversals\n"
        f"Input sequence ({len(values)}): {values}\n\n"
        f"In-order:   {traversals['in_order']}\n"
        f"Pre-order:  {traversals['pre_order']}\n"
        f"Post-order: {traversals['post_order']}\n"
        f"Level-order:{traversals['level_order']}\n",
        encoding="utf-8",
    )

    answer_txt = TASK_DIR / "antworten.txt"
    answer_txt.write_text(
        "Task 2 - Traversals\n"
        "The script computed all requested traversal orders.\n"
        f"In-order: {traversals['in_order']}\n"
        f"Pre-order: {traversals['pre_order']}\n"
        f"Post-order: {traversals['post_order']}\n"
        f"Level-order: {traversals['level_order']}\n",
        encoding="utf-8",
    )


def main() -> None:
    values = load_seq0()
    tree = build_tree(values)
    traversals = run_traversals(tree)
    write_outputs(values, traversals)

    print("Task 2 finished.")
    print(f"In-order:   {traversals['in_order']}")
    print(f"Pre-order:  {traversals['pre_order']}")
    print(f"Post-order: {traversals['post_order']}")
    print(f"Level-order:{traversals['level_order']}")


if __name__ == "__main__":
    main()
