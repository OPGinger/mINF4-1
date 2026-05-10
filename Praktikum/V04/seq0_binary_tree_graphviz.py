"""
Daniel Baer
09.05.2026

mINF4/1, V04, "Binary Tree mit Graphviz"

seq0_binary_tree_graphviz.py


This application reads the sequence seq0 from AlgoDatSoSe26/data/seq0.txt,
inserts the numbers into a binary search tree, and renders the tree with Graphviz.
"""

import os
import sys
from pathlib import Path
import graphviz

# add path of AlgoDatSoSe26 directory
SCRIPT_DIR = Path(__file__).resolve().parent
ALGODAT_DIR = SCRIPT_DIR.parent / "AlgoDatSoSe26"
sys.path.insert(0, str(ALGODAT_DIR))

from utils.algo_context import AlgoContext  # type: ignore[import-not-found]
from vorlesung.L05_binaere_baeume.bin_tree import BinaryTree  # type: ignore[import-not-found]
import vorlesung.L05_binaere_baeume.bin_tree as bin_tree_module  # type: ignore[import-not-found]


def configure_graphviz() -> None:
    local_dot = SCRIPT_DIR / "Graphviz-14.1.5-win64" / "bin" / "dot.exe"

    if local_dot.exists():
        local_bin = str(local_dot.parent)
        os.environ["PATH"] = local_bin + os.pathsep + os.environ.get("PATH", "")
        os.environ["GRAPHVIZ_DOT"] = str(local_dot)


def read_sequence(filename: Path) -> list:
    with open(filename, "r") as f:
        return [int(line.strip()) for line in f if line.strip()]


def build_tree(values: list, ctx: AlgoContext) -> BinaryTree:
    tree = BinaryTree(ctx)
    for value in values:
        tree.insert(value)
    return tree


def count_leaves(node) -> int:
    if node is None:
        return 0
    if node.left is None and node.right is None:
        return 1
    return count_leaves(node.left) + count_leaves(node.right)


def redirect_graph_output_to_v04() -> None:
    def local_path(filename: str) -> Path:
        return SCRIPT_DIR / filename

    # graph_traversal in bin_tree.py resolves output via module function "path"
    bin_tree_module.path = local_path


def latest_v04_pdf() -> Path:
    pdf_files = sorted(SCRIPT_DIR.glob("BinaryTree_*.gv.pdf"), key=lambda p: p.stat().st_mtime)
    if not pdf_files:
        raise FileNotFoundError("Kein erzeugtes BinaryTree PDF in V04 gefunden.")
    return pdf_files[-1]


def main() -> None:
    configure_graphviz()
    redirect_graph_output_to_v04()

    filename = ALGODAT_DIR / "data" / "seq0.txt"

    sequence = read_sequence(filename)
    ctx = AlgoContext()
    tree = build_tree(sequence, ctx)
    root = tree.root

    if root is None:
        print("seq0 ist leer.")
        return

    try:
        tree.graph_traversal()
        output_file = latest_v04_pdf()
    except graphviz.backend.execute.ExecutableNotFound:
        print("Graphviz executable 'dot' wurde nicht gefunden.")
        print("Erwartet: ./Graphviz-14.1.5-win64/bin/dot.exe oder dot im PATH")
        return

    root_value = root.value
    leaf_count = count_leaves(root)
    height = root.height()

    print(f"Datei: {filename}")
    print(f"Anzahl Werte: {len(sequence)}")
    print(f"Ausgabe: {output_file}")
    print(f"Wurzel: {root_value}")
    print(f"Blattknoten: {leaf_count}")
    print(f"Hoehe: {height}")


if __name__ == "__main__":
    main()
