"""
Daniel Baer
10.05.2026

mINF4/1, V04, Task 4 "Deletion in AVL Tree"

szenario_zwei_kinder.py

Scenario 3: Delete a node with two children in an AVL tree.
"""

import os
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
V04_DIR = TASK_DIR.parent.parent
ALGODAT_DIR = V04_DIR.parent / "AlgoDatSoSe26"
GRAPHVIZ_DOT = V04_DIR / "Graphviz-14.1.5-win64" / "bin" / "dot.exe"

sys.path.insert(0, str(ALGODAT_DIR))

from utils.algo_context import AlgoContext  # type: ignore[import-not-found]
from vorlesung.L05_binaere_baeume.avl_tree import AVLTree  # type: ignore[import-not-found]
import vorlesung.L05_binaere_baeume.bin_tree as bin_tree_module  # type: ignore[import-not-found]


class NamedAVLTree(AVLTree):
    def __init__(self, ctx: AlgoContext, graph_name: str):
        super().__init__(ctx)
        self._graph_name = graph_name

    def graph_filename(self):
        return self._graph_name

    def set_graph_filename(self, graph_name: str) -> None:
        self._graph_name = graph_name


def configure_graphviz() -> None:
    if GRAPHVIZ_DOT.exists():
        os.environ["GRAPHVIZ_DOT"] = str(GRAPHVIZ_DOT)
        os.environ["PATH"] = str(GRAPHVIZ_DOT.parent) + os.pathsep + os.environ.get("PATH", "")


def redirect_graph_output_to_task_folder() -> None:
    def local_path(filename: str) -> Path:
        return TASK_DIR / filename

    bin_tree_module.path = local_path


def latest_pdf_for_prefix(prefix: str) -> Path:
    files = sorted(TASK_DIR.glob(f"{prefix}_*.gv.pdf"), key=lambda p: p.stat().st_mtime)
    if not files:
        raise FileNotFoundError(f"No generated PDF found for prefix: {prefix}")
    return files[-1]


def in_order_values(tree: AVLTree) -> list[int]:
    out: list[int] = []
    tree.in_order_traversal(lambda node: out.append(node.value))
    return out


def main() -> None:
    configure_graphviz()
    redirect_graph_output_to_task_folder()

    insert_values = [30, 20, 40, 10, 25, 35, 50, 5, 15, 27]
    delete_value = 20  # node with two children (10 and 25)

    tree = NamedAVLTree(AlgoContext(), "AVL_TwoChildren_Before_Delete")
    for value in insert_values:
        tree.insert(value)

    before_height = tree.root.height() if tree.root else 0
    before_in_order = in_order_values(tree)
    tree.graph_traversal()
    before_pdf = latest_pdf_for_prefix("AVL_TwoChildren_Before_Delete")

    tree.delete(delete_value)
    tree.set_graph_filename("AVL_TwoChildren_After_Delete")

    after_height = tree.root.height() if tree.root else 0
    after_in_order = in_order_values(tree)
    tree.graph_traversal()
    after_pdf = latest_pdf_for_prefix("AVL_TwoChildren_After_Delete")

    answer_text = (
        "Task 4 - Scenario 3 (Two-Children Node Deletion)\n"
        f"Inserted values: {insert_values}\n"
        f"Deleted value: {delete_value}\n"
        f"Height before deletion: {before_height}\n"
        f"Height after deletion: {after_height}\n"
        f"In-order before deletion: {before_in_order}\n"
        f"In-order after deletion: {after_in_order}\n"
        f"Graph before deletion: {before_pdf.name}\n"
        f"Graph after deletion: {after_pdf.name}\n"
    )

    (TASK_DIR / "antworten.txt").write_text(answer_text, encoding="utf-8")
    print(answer_text)


if __name__ == "__main__":
    main()
