"""
Daniel Baer
25.05.2026

mINF4/1, V06, Task 2 " Verifikation von HashTableChaining"

V06_02_verification.py


This script verifies the chaining implementation on seq0 with table size 20.
"""

import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
V06_DIR = TASK_DIR.parent
PRAKTIKUM_DIR = V06_DIR.parent
ALGODAT_DIR = PRAKTIKUM_DIR / "AlgoDatSoSe26"

sys.path.insert(0, str(V06_DIR))
sys.path.insert(0, str(ALGODAT_DIR))

# import necessary modules and classes
from utils.algo_context import AlgoContext
from utils.algo_int import Int
from vorlesung.L07_hashtable.analyze_hashtable import h
from V06_hashtable_chaining import HashTableChaining


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
    table = HashTableChaining(20, h, ctx)
    for value in seq0:
        table.insert(Int(value, ctx))

    # a) measure alpha after first insert
    print(f"alpha after insert: {table.alpha():.4f}\n")
    
    # b) remove 52 and print the chain at its slot before and after deletion
    print(f"slots before delete:\n{str(table)}\n")
    table.delete(Int(52, ctx))
    print(f"delete 52\n")
    print(f"slots after delete:\n{str(table)}\n")

    # c) insert all values from seq0 again and print alpha
    for value in seq0:
        table.insert(Int(value, ctx))
    print(f"alpha after second insert: {table.alpha():.4f}\n")


if __name__ == "__main__":
    main()
