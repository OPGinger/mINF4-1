"""
Praktikum V05 - Aufgabe 2: Eigenschaften des B-Baums.

- Liest seq3.txt
- Baut B-Baeume fuer Ordnung 3 und 5
- Ermittelt Hoehe, sortierte Traversierung, Knoten mit Schluessel 0
- Schreibt Ergebnisse nach antworten.txt
"""

from __future__ import annotations

import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
PRAKTIKUM_DIR = TASK_DIR.parent.parent
ALGODAT_DIR = PRAKTIKUM_DIR.parent / "AlgoDatSoSe26"
BTREE_DIR = ALGODAT_DIR / "vorlesung" / "L06_b_baeume"

sys.path.insert(0, str(ALGODAT_DIR))
sys.path.insert(0, str(BTREE_DIR))

from utils.algo_array import Array  # type: ignore[import-not-found]
from utils.algo_context import AlgoContext  # type: ignore[import-not-found]
from b_tree import BTree  # type: ignore[import-not-found]


def build_tree(order_m: int, values: Array, ctx: AlgoContext) -> BTree:
    tree = BTree(order_m, ctx)
    for cell in values:
        tree.insert(cell)
    return tree


def in_order_values(tree: BTree) -> list[int]:
    out: list[int] = []
    tree.traversal(lambda key: out.append(int(key)))
    return out


def main() -> None:
    base_ctx = AlgoContext()
    values = Array.from_file("data/seq3.txt", base_ctx)

    ctx_m3 = AlgoContext()
    tree_m3 = build_tree(3, values, ctx_m3)

    ctx_m5 = AlgoContext()
    tree_m5 = build_tree(5, values, ctx_m5)

    h3 = tree_m3.height()
    h5 = tree_m5.height()

    traversal_m3 = in_order_values(tree_m3)
    traversal_m5 = in_order_values(tree_m5)
    sorted_m3 = traversal_m3 == sorted(traversal_m3)
    sorted_m5 = traversal_m5 == sorted(traversal_m5)

    node_0_m3 = tree_m3.search(0)
    node_0_m5 = tree_m5.search(0)

    node_0_m3_str = str(node_0_m3) if node_0_m3 is not None else "nicht gefunden"
    node_0_m5_str = str(node_0_m5) if node_0_m5 is not None else "nicht gefunden"

    answer_lines = [
        "Praktikum 5 - Aufgabe 2: Eigenschaften des B-Baums",
        "Datensatz: seq3.txt",
        "",
        f"Hoehe bei Ordnung 3: {h3}",
        f"Hoehe bei Ordnung 5: {h5}",
        "",
        f"Traversal Ordnung 3 sortiert: {sorted_m3}",
        f"Traversal Ordnung 5 sortiert: {sorted_m5}",
        "",
        f"Knoten mit Wert 0 bei Ordnung 3: {node_0_m3_str}",
        f"Knoten mit Wert 0 bei Ordnung 5: {node_0_m5_str}",
        "",
        "Warum enthaelt der Knoten bei Ordnung 5 tendenziell mehr Schluessel?",
        "Bei groesserem m darf ein Knoten bis zu 2m-1 Schluessel halten.",
        "Splits treten spaeter auf, deshalb werden Werte laenger in einem Knoten gesammelt.",
        "Dadurch ist die mittlere Fuellung pro Knoten bei groesserem m typischerweise hoeher.",
    ]

    (TASK_DIR / "antworten.txt").write_text("\n".join(answer_lines) + "\n", encoding="utf-8")

    print("Aufgabe 2 abgeschlossen")
    print(f"Hoehe m=3: {h3}, Hoehe m=5: {h5}")
    print(f"Node(0) m=3: {node_0_m3_str}")
    print(f"Node(0) m=5: {node_0_m5_str}")


if __name__ == "__main__":
    main()
