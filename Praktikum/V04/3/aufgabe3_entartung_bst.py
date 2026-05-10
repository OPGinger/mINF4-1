"""
Daniel Baer
09.05.2026

mINF4/1, V04, Task 3 "Degeneration of BST"

aufgabe3_entartung_bst.py

This script demonstrates BST degeneration by inserting sorted values.
It creates two trees (ascending and descending insertion), exports Graphviz PDFs,
and evaluates resulting tree heights.
"""

import os
import sys
from pathlib import Path

# Resolve local directories relative to this task folder.
TASK_DIR = Path(__file__).resolve().parent
V04_DIR = TASK_DIR.parent
ALGODAT_DIR = V04_DIR.parent / "AlgoDatSoSe26"
GRAPHVIZ_DOT = V04_DIR / "Graphviz-14.1.5-win64" / "bin" / "dot.exe"

# Add lecture project to import path.
sys.path.insert(0, str(ALGODAT_DIR))

from utils.algo_context import AlgoContext  # type: ignore[import-not-found]
from vorlesung.L05_binaere_baeume.bin_tree import BinaryTree  # type: ignore[import-not-found]
import vorlesung.L05_binaere_baeume.bin_tree as bin_tree_module  # type: ignore[import-not-found]


class NamedBinaryTree(BinaryTree):
    """BinaryTree variant with configurable graph file base name."""

    def __init__(self, ctx: AlgoContext, graph_name: str):
        super().__init__(ctx)
        self._graph_name = graph_name

    def graph_filename(self):
        return self._graph_name


def configure_graphviz() -> None:
    """Configure local Graphviz executable path for Windows."""
    if GRAPHVIZ_DOT.exists():
        os.environ["GRAPHVIZ_DOT"] = str(GRAPHVIZ_DOT)
        os.environ["PATH"] = str(GRAPHVIZ_DOT.parent) + os.pathsep + os.environ.get("PATH", "")


def redirect_graph_output_to_task_folder() -> None:
    """Force graph_traversal() output files into this task folder only."""

    def local_path(filename: str) -> Path:
        return TASK_DIR / filename

    bin_tree_module.path = local_path


def build_tree(values: list[int], graph_name: str) -> NamedBinaryTree:
    """Build a named BST with deterministic insertion order."""
    tree = NamedBinaryTree(AlgoContext(), graph_name)
    for value in values:
        tree.insert(value)
    return tree


def latest_pdf_for_prefix(prefix: str) -> Path:
    """Return newest graph PDF matching the specific task prefix."""
    files = sorted(TASK_DIR.glob(f"{prefix}_*.gv.pdf"), key=lambda p: p.stat().st_mtime)
    if not files:
        raise FileNotFoundError(f"No generated PDF found for prefix: {prefix}")
    return files[-1]


def main() -> None:
    configure_graphviz()
    redirect_graph_output_to_task_folder()

    n = 15
    ascending_values = list(range(1, n + 1))
    descending_values = list(range(n, 0, -1))

    tree_asc = build_tree(ascending_values, "BST_Degeneration_Ascending")
    tree_desc = build_tree(descending_values, "BST_Degeneration_Descending")

    tree_asc.graph_traversal()
    tree_desc.graph_traversal()

    asc_pdf = latest_pdf_for_prefix("BST_Degeneration_Ascending")
    desc_pdf = latest_pdf_for_prefix("BST_Degeneration_Descending")

    asc_height = tree_asc.root.height() if tree_asc.root else 0
    desc_height = tree_desc.root.height() if tree_desc.root else 0

    answer_text = (
        "Task 3 - Degeneration of BST\n"
        f"Input size n: {n}\n"
        f"Ascending insertion height: {asc_height}\n"
        f"Descending insertion height: {desc_height}\n"
        f"Ascending PDF: {asc_pdf.name}\n"
        f"Descending PDF: {desc_pdf.name}\n"
        "Interpretation: both sorted insertion orders create a degenerated tree (chain),\n"
        "so height grows linearly with n in the worst case.\n"
    )

    (TASK_DIR / "antworten.txt").write_text(answer_text, encoding="utf-8")

    print("Task 3 finished.")
    print(answer_text)


if __name__ == "__main__":
    main()
