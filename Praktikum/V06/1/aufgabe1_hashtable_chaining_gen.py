"""
Daniel Baer
20.05.2026

mINF4/1, V06, Task 1 "HashTableChaining"

aufgabe1_hashtable_chaining.py

This script implements and demonstrates HashTableChaining methods.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Resolve local directories relative to this task folder.
TASK_DIR = Path(__file__).resolve().parent
V06_DIR = TASK_DIR.parent
PRAKTIKUM_DIR = V06_DIR.parent
ALGODAT_DIR = PRAKTIKUM_DIR / "AlgoDatSoSe26"

# Add module paths for shared V06 code and AlgoDat lecture code.
sys.path.insert(0, str(V06_DIR))
sys.path.insert(0, str(ALGODAT_DIR))

from utils.algo_context import AlgoContext  # type: ignore[import-not-found]
from utils.algo_int import Int  # type: ignore[import-not-found]
from vorlesung.L07_hashtable.analyze_hashtable import h  # type: ignore[import-not-found]
from V06_hashtable_chaining import HashTableChaining


def write_answers(table: HashTableChaining) -> None:
    """Write a compact confirmation that all required methods are available."""
    out = TASK_DIR / "antworten.txt"
    out.write_text(
        "Task 1 - HashTableChaining\n"
        "Implemented methods:\n"
        "- insert(x): inserts x, duplicates are not stored twice\n"
        "- search(x): returns True/False\n"
        "- delete(x): removes x if present\n"
        "- __str__(): prints all slots including empty slots\n"
        "- alpha(): returns n/m\n\n"
        f"Current alpha after demo inserts: {table.alpha():.4f}\n"
        "Current table (all slots):\n"
        f"{table}\n",
        encoding="utf-8",
    )


def main() -> None:
    ctx = AlgoContext()
    table = HashTableChaining(20, h, ctx)

    # Small demo sequence to verify all methods quickly.
    demo_values = [52, 24, 52, 31, 9, 31]
    for value in demo_values:
        table.insert(Int(value, ctx))

    # Demo calls for search and delete.
    present_52 = table.search(Int(52, ctx))
    removed_24 = table.delete(Int(24, ctx))
    present_24_after = table.search(Int(24, ctx))

    write_answers(table)

    print("Task 1 finished.")
    print(f"search(52) -> {present_52}")
    print(f"delete(24) -> {removed_24}")
    print(f"search(24) after delete -> {present_24_after}")
    print(f"alpha = {table.alpha():.4f}")


if __name__ == "__main__":
    main()
