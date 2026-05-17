"""
Daniel Baer
17.05.2026

mINF4/1, V05, "B-Baum"

V05_02a.py

this application implements a B-Tree visualization using Graphviz.
It defines a BTreeVis class that extends the BTree implementation to generate a PDF visualization of the tree structure after inserting values from seq0.txt.
The application also collects properties of the tree such as the number of keys in the root and the depths of leaf nodes to verify the balance property of B-trees.

"""

import os
import sys
from pathlib import Path

from graphviz import Digraph

""" add paths for imports """
SCRIPT_DIR = Path(__file__).resolve().parent
PRAKTIKUM_DIR = SCRIPT_DIR.parent.parent
ALGODAT_DIR = PRAKTIKUM_DIR / "AlgoDatSoSe26"

BTREE_DIR = ALGODAT_DIR / "vorlesung" / "L06_b_baeume"
sys.path.insert(0, str(ALGODAT_DIR))

GRAPHVIZ_DOT = PRAKTIKUM_DIR / "Graphviz-14.1.5-win64" / "bin" / "dot.exe"
sys.path.insert(0, str(BTREE_DIR))


from utils.algo_array import Array          # type: ignore[import-not-found]
from utils.algo_context import AlgoContext  # type: ignore[import-not-found]
from b_tree import BTree                    # type: ignore[import-not-found]

def configure_graphviz() -> None:
    """Use local Graphviz installation from V04 """
    if GRAPHVIZ_DOT.exists():
        os.environ["GRAPHVIZ_DOT"] = str(GRAPHVIZ_DOT)
        os.environ["PATH"] = str(GRAPHVIZ_DOT.parent) + os.pathsep + os.environ.get("PATH", "")


class BTreeVis(BTree):
    """B-Tree subclass with Graphviz output."""

    def graph_traversal(self, output_path: str = "btree") -> Path:
        
        """ create a Graphviz Digraph to visualize the B-Tree structure """
        dot = Digraph("BTree", format="pdf")
        
        """ set node shape to record for better visualization of keys """
        dot.attr("node", shape="record")

        """ helper to create node labels based on keys """
        def node_label(node) -> str:
            """ create label string for a node based on its keys """
            keys = [str(node.value[i]) for i in range(node.n)]
            
            if not keys:
                return "empty"
            
            """ join keys with | to create a record label """
            return " | ".join(keys)

        def walk(node) -> None:
            """ add current node to graph with label of its keys """
            dot.node(f"node_{id(node)}", label=node_label(node))
            
            if node.leaf:
                return
            
            """ recursively add children and edges """
            for idx in range(node.n + 1):
                
                """ get child node at index idx """
                child = node.children[idx]
                if child is None:
                    continue
                
                """ add edge from current node to child """
                dot.edge(f"node_{id(node)}", f"node_{id(child)}")
                
                """ recursively walk child node """
                walk(child)
                
        """ start traversal from root to build the graph """
        walk(self.root)
        
        
        out_file = SCRIPT_DIR / output_path
        rendered = Path(dot.render(filename=str(out_file), cleanup=True))
        return rendered


def collect_leaf_depths(tree: BTree) -> list[int]:
    """Collect all leaf depths to verify B-tree balance property."""
    depths: list[int] = []

    """ helper function to walk the tree and collect depths of leaf nodes """
    def walk(node, depth: int) -> None:
        """ if current node is a leaf, record its depth """
        if node.leaf:
            depths.append(depth)
            return
        
        """ recursively walk all children of the current node """
        for idx in range(node.n + 1):
            child = node.children[idx]
            if child is not None:
                walk(child, depth + 1)

    """ start walking from the root at depth 0 """
    walk(tree.root, 0)
    
    return depths


def main() -> None:
    configure_graphviz()

    """ create context and load data from seq1.txt """
    ctx = AlgoContext()
    sequence = "seq0"
    data = Array.from_file(f"data/{sequence}.txt", ctx)
    order = 3

    """ build the B-Tree and generate the Graphviz visualization """
    tree = BTreeVis(order, ctx)
    
    """ insert values from the data file into the B-Tree """
    for value in data:
        tree.insert(value)

    """ generate PDF visualization of the B-Tree structure """
    pdf_file = tree.graph_traversal(f"BTree_O{order}_{sequence}")

    """ collect properties of the B-Tree for analysis """
    root_key_count = tree.root.n
    leaf_depths = collect_leaf_depths(tree)
    
    """ collect all keys in the tree to verify they are in sorted order """
    keys_list: list[int] = []
    tree.traversal(lambda key: keys_list.append(int(key)))  # Ensure all nodes are loaded for accurate properties
    
    """ check if all keys are in sorted order to verify B-Tree properties """
    is_sorted = all(keys_list[i] <= keys_list[i + 1] for i in range(len(keys_list) - 1))

    """ print out the collected properties and the path to the generated PDF visualization """
    print(f"PDF: {pdf_file}")
    print(f"Root Key Count: {root_key_count}")
    print(f"Leaf Depths: {leaf_depths}")
    print(f"All Keys: {keys_list}")
    print(f"Keys in Sorted Order: {is_sorted}")


if __name__ == "__main__":
    main()
