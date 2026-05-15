"""
Praktikum V05 - Aufgabe 1: Graphviz-Visualisierung eines B-Baums.

- Implementiert BTreeVis(BTree) mit graph_traversal()
- Fuegt seq1.txt in einen B-Baum der Ordnung 3 ein
- Erzeugt eine PDF-Visualisierung und schreibt die Antworten in antworten.txt
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from graphviz import Digraph

TASK_DIR = Path(__file__).resolve().parent
PRAKTIKUM_DIR = TASK_DIR.parent.parent
ALGODAT_DIR = PRAKTIKUM_DIR.parent / "AlgoDatSoSe26"
BTREE_DIR = ALGODAT_DIR / "vorlesung" / "L06_b_baeume"
GRAPHVIZ_DOT = PRAKTIKUM_DIR / "V04" / "Graphviz-14.1.5-win64" / "bin" / "dot.exe"

sys.path.insert(0, str(ALGODAT_DIR))
sys.path.insert(0, str(BTREE_DIR))

from utils.algo_array import Array  # type: ignore[import-not-found]
from utils.algo_context import AlgoContext  # type: ignore[import-not-found]
from b_tree import BTree  # type: ignore[import-not-found]


def configure_graphviz() -> None:
    """Use local Graphviz installation from V04 if available."""
    if GRAPHVIZ_DOT.exists():
        os.environ["GRAPHVIZ_DOT"] = str(GRAPHVIZ_DOT)
        os.environ["PATH"] = str(GRAPHVIZ_DOT.parent) + os.pathsep + os.environ.get("PATH", "")


class BTreeVis(BTree):
    """B-Tree subclass with Graphviz output."""

    def graph_traversal(self, output_stem: str = "btree_seq1_order3") -> Path:
        dot = Digraph("BTree", format="pdf")
        dot.attr("node", shape="record")

        def node_id(node) -> str:
            return f"node_{id(node)}"

        def node_label(node) -> str:
            keys = [str(node.value[i]) for i in range(node.n)]
            if not keys:
                return "empty"
            return " | ".join(keys)

        def walk(node) -> None:
            cur_id = node_id(node)
            dot.node(cur_id, label=node_label(node))
            if node.leaf:
                return
            for idx in range(node.n + 1):
                child = node.children[idx]
                if child is None:
                    continue
                child_id = node_id(child)
                dot.edge(cur_id, child_id)
                walk(child)

        walk(self.root)
        out_file = TASK_DIR / output_stem
        rendered = Path(dot.render(filename=str(out_file), cleanup=True))
        return rendered


def collect_leaf_depths(tree: BTree) -> list[int]:
    """Collect all leaf depths to verify B-tree balance property."""
    depths: list[int] = []

    def walk(node, depth: int) -> None:
        if node.leaf:
            depths.append(depth)
            return
        for idx in range(node.n + 1):
            child = node.children[idx]
            if child is not None:
                walk(child, depth + 1)

    walk(tree.root, 0)
    return depths


def main() -> None:
    configure_graphviz()

    ctx = AlgoContext()
    values = Array.from_file("data/seq1.txt", ctx)

    tree = BTreeVis(3, ctx)
    for cell in values:
        tree.insert(cell)

    pdf_file = tree.graph_traversal()

    root_key_count = tree.root.n
    leaf_depths = collect_leaf_depths(tree)
    all_same_depth = len(set(leaf_depths)) == 1

    answer_lines = [
        "Praktikum 5 - Aufgabe 1: Graphviz-Visualisierung",
        f"Erzeugte PDF: {pdf_file.name}",
        "",
        f"Anzahl Schluessel in der Wurzel: {root_key_count}",
        f"Blatttiefen: {leaf_depths}",
        f"Alle Blaetter auf derselben Tiefe: {all_same_depth}",
        "",
        "Begruendung:",
        "Ja, in einem B-Baum liegen alle Blattknoten immer auf derselben Tiefe.",
        "Bei jedem Split wird nur lokal umstrukturiert und die Hoehe global nur am Root erhoeht.",
        "Dadurch bleibt die Balance-Invariante erhalten.",
    ]

    (TASK_DIR / "antworten.txt").write_text("\n".join(answer_lines) + "\n", encoding="utf-8")

    print("Aufgabe 1 abgeschlossen")
    print(f"PDF: {pdf_file}")
    print(f"Wurzel-Schluessel: {root_key_count}")
    print(f"Blatttiefen: {leaf_depths}")


if __name__ == "__main__":
    main()
