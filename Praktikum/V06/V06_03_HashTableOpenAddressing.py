"""
Daniel Baer
26.05.2026

mINF4/1, V06, Task 3 "Hashtabelle mit offener Adressierung"

V06_03_HashTableOpenAddressing.py


This script analyzes delete/search behavior for open addressing with m=20.
"""

import sys
from pathlib import Path

# Resolve local directories relative to this task folder.
TASK_DIR = Path(__file__).resolve().parent
V06_DIR = TASK_DIR.parent
PRAKTIKUM_DIR = V06_DIR.parent
ALGODAT_DIR = PRAKTIKUM_DIR / "AlgoDatSoSe26"

# Add module path for AlgoDat lecture code.
sys.path.insert(0, str(ALGODAT_DIR))

from utils.algo_context import AlgoContext  # type: ignore[import-not-found]
from utils.algo_int import Int  # type: ignore[import-not-found]
from vorlesung.L07_hashtable.analyze_hashtable import h, f  # type: ignore[import-not-found]
from vorlesung.L07_hashtable.hashtable import HashTableOpenAddressing  # type: ignore[import-not-found]


def load_seq0() -> list[int]:
    """ load integers from data/seq0.txt """
    
    # build path to seq0.txt
    seq_file = ALGODAT_DIR / "data" / "seq0.txt"
    
    with seq_file.open("r", encoding="utf-8") as f:
        return [int(line.strip()) for line in f if line.strip()]

def main() -> None:
    ctx = AlgoContext()
    seq0 = load_seq0()

    # create hash table and insert all values from seq0
    table = HashTableOpenAddressing(20, f, ctx)
    for value in seq0:
        table.insert(Int(value, ctx))

    # a) remove 52 and print the chain at its slot before and after deletion
    print(f"before delete: {str(table)}")
    table.delete(Int(52, ctx))
    print(f"delete 52")
    print(f"after delete:  {str(table)}\n")
    
    # d) insert value 24
    print(f"before insertion: {str(table)}")
    table.insert(Int(24, ctx))
    print(f"insert 24, f(24) = {f(Int(24, ctx), Int(1, ctx), Int(20, ctx))}")
    print(f"after insertion:  {str(table)}")


if __name__ == "__main__":
    main()
