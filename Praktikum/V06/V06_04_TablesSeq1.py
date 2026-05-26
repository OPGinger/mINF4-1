"""
Daniel Baer
26.05.2026

mINF4/1, V06, Task 4 "Belegungsfaktoren und Sonierungszahlen"

V06_04_TablesSeq1.py


This script compares open addressing behavior for m=90 and m=89,
and chaining behavior for m=20 using seq1.
"""


import sys
from pathlib import Path

# Resolve local directories relative to this task folder.
TASK_DIR = Path(__file__).resolve().parent
V06_DIR = TASK_DIR.parent
PRAKTIKUM_DIR = V06_DIR.parent
ALGODAT_DIR = PRAKTIKUM_DIR / "AlgoDatSoSe26"

# Add module paths
sys.path.insert(0, str(V06_DIR))
sys.path.insert(0, str(ALGODAT_DIR))

from utils.algo_context import AlgoContext  # type: ignore[import-not-found]
from utils.algo_int import Int  # type: ignore[import-not-found]
from vorlesung.L07_hashtable.analyze_hashtable import f, h  # type: ignore[import-not-found]
from vorlesung.L07_hashtable.hashtable import HashTableOpenAddressing  # type: ignore[import-not-found]
from V06_hashtable_chaining import HashTableChaining


def load_seq1() -> list[int]:
    """ load integers from data/seq1.txt """
    
    # build path to seq1.txt
    seq_file = ALGODAT_DIR / "data" / "seq1.txt"
    
    with seq_file.open("r", encoding="utf-8") as f:
        return [int(line.strip()) for line in f if line.strip()]


def run_open_addressing(seq: list[int], m: int) -> dict[str, float | int]:
    """ insert all values into open addressing table and return summary """
    ctx = AlgoContext()
    ht = HashTableOpenAddressing(m, f, ctx)

    # insert values and count how many were inserted and rejected
    inserted = 0
    rejected = 0
    for value in seq:
        if ht.insert(Int(value, ctx)):
            inserted += 1
        else:
            rejected += 1

    # count unused slots for summary
    unused_slots = 0
    for idx in range(m):
        if ht.table[Int(idx, ctx)].value == "UNUSED":
            unused_slots += 1

    return {
        "inserted": inserted,
        "rejected": rejected,
        "unused": unused_slots,
        "alpha": ht.alpha(),
    }


def run_chaining(seq: list[int], m: int) -> dict[str, float | int]:
    """ insert all values into chaining table and return summary """
    ctx = AlgoContext()
    ht = HashTableChaining(m, h, ctx)

    # insert values and count how many were inserted
    inserted_before = ht.n
    for value in seq:
        ht.insert(Int(value, ctx))
    inserted = ht.n - inserted_before

    return {
        "inserted": inserted,
        "alpha": ht.alpha(),
    }


def main() -> None:
    sequence = load_seq1()

    # a) rejection behaviour open addressing for m=90
    open_90 = run_open_addressing(sequence, 90)
    print(f"for m=90:\ninserted: {open_90['inserted']}\nrejected: {open_90['rejected']}\nunused slots: {open_90['unused']}\nalpha: {open_90['alpha']:.4f}\n ")

    # b) rejection behaviour open addressing for m=89
    open_89 = run_open_addressing(sequence, 89)
    print(f"for m=89:\ninserted: {open_89['inserted']}\nrejected: {open_89['rejected']}\nunused slots: {open_89['unused']}\nalpha: {open_89['alpha']:.4f}\n ")
    
    # c) chaining behaviour for m=20
    chaining_20 = run_chaining(sequence, 20)
    print(f"for m=20:\ninserted: {chaining_20['inserted']}\nalpha: {chaining_20['alpha']:.4f}\n ")

    # d) probe number for 0.5 to 0.9 for open addressing
    print("probe numbers for open addressing:")
    print(f"alpha=0.5: {1.0 / (1.0 - 0.5):.4f}")
    print(f"alpha=0.6: {1.0 / (1.0 - 0.6):.4f}")
    print(f"alpha=0.7: {1.0 / (1.0 - 0.7):.4f}")
    print(f"alpha=0.8: {1.0 / (1.0 - 0.8):.4f}")
    print(f"alpha=0.9: {1.0 / (1.0 - 0.9):.4f}")


if __name__ == "__main__":
    main()
