"""
Daniel Baer
20.05.2026

mINF4/1, V06, Task 4 "Table Sizes and Probing Behavior"

aufgabe4_tabellengroessen_seq1.py

This script compares open addressing behavior for m=90 and m=89,
and chaining behavior for m=20 using seq1.
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
from vorlesung.L07_hashtable.analyze_hashtable import f, h  # type: ignore[import-not-found]
from vorlesung.L07_hashtable.hashtable import HashTableOpenAddressing  # type: ignore[import-not-found]
from hashtable_chaining import HashTableChaining


UNUSED_MARK = "UNUSED"


def load_seq1() -> list[int]:
    """Load integers from data/seq1.txt."""
    seq_file = ALGODAT_DIR / "data" / "seq1.txt"
    with seq_file.open("r", encoding="utf-8") as f:
        return [int(line.strip()) for line in f if line.strip()]


def run_open_addressing(seq: list[int], m: int) -> dict[str, float | int]:
    """Insert all values into open addressing table and return summary metrics."""
    ctx = AlgoContext()
    ht = HashTableOpenAddressing(m, f, ctx)

    inserted = 0
    rejected = 0
    for value in seq:
        if ht.insert(Int(value, ctx)):
            inserted += 1
        else:
            rejected += 1

    unused_slots = 0
    for idx in range(m):
        if ht.table[Int(idx, ctx)].value == UNUSED_MARK:
            unused_slots += 1

    return {
        "m": m,
        "inserted": inserted,
        "rejected": rejected,
        "unused_slots": unused_slots,
        "alpha": ht.alpha(),
    }


def max_probe_coverage(seq: list[int], m: int) -> int:
    """Return the maximum number of unique probe positions visited for sampled keys."""
    ctx = AlgoContext()
    max_unique = 0

    # Sampling keys from seq keeps the explanation tied to the actual dataset.
    sample = seq[: min(30, len(seq))]
    for value in sample:
        visited: set[int] = set()
        key = Int(value, ctx)
        for i in range(m):
            pos = int(f(key, Int(i, ctx), Int(m, ctx)))
            visited.add(pos)
        max_unique = max(max_unique, len(visited))

    return max_unique


def run_chaining(seq: list[int], m: int) -> dict[str, float | int]:
    """Insert all values into chaining table and return summary metrics."""
    ctx = AlgoContext()
    ht = HashTableChaining(m, h, ctx)

    inserted_before = ht.n
    for value in seq:
        ht.insert(Int(value, ctx))
    inserted = ht.n - inserted_before

    return {
        "m": m,
        "inserted": inserted,
        "alpha": ht.alpha(),
    }


def write_answers(
    open_90: dict[str, float | int],
    open_89: dict[str, float | int],
    chaining_20: dict[str, float | int],
    max_cov_90: int,
    max_cov_89: int,
    theo_05: float,
    theo_09: float,
) -> None:
    """Write answers for questions 4a to 4d."""
    out = TASK_DIR / "antworten.txt"
    out.write_text(
        "Task 4 - Open Addressing vs Chaining on seq1\n\n"
        "4a) Open addressing with m=90 and 100 input values:\n"
        f"inserted = {open_90['inserted']}\n"
        f"rejected = {open_90['rejected']}\n"
        f"unused slots after insertion = {open_90['unused_slots']}\n"
        f"alpha = {float(open_90['alpha']):.4f}\n"
        f"max unique probe positions (sampled keys) = {max_cov_90} of 90\n"
        "Reason: quadratic probing f can cycle through only a subset of slots for non-prime m,\n"
        "so insert may fail even when other slots are still free.\n\n"
        "4b) Open addressing with m=89:\n"
        f"inserted = {open_89['inserted']}\n"
        f"rejected = {open_89['rejected']}\n"
        f"unused slots after insertion = {open_89['unused_slots']}\n"
        f"alpha = {float(open_89['alpha']):.4f}\n"
        f"max unique probe positions (sampled keys) = {max_cov_89} of 89\n"
        "Prime table sizes are advantageous because probe sequences are less likely to get trapped\n"
        "in short cycles, so more slots become reachable.\n\n"
        "4c) Chaining with m=20 and seq1:\n"
        f"inserted = {chaining_20['inserted']}\n"
        f"alpha = {float(chaining_20['alpha']):.4f}\n"
        "Chaining can store all (distinct) keys by extending chains in occupied slots.\n\n"
        "4d) Theoretical mean probe count 1/(1-alpha):\n"
        f"for alpha = 0.5: {theo_05:.4f}\n"
        f"for alpha = 0.9: {theo_09:.4f}\n"
        "Practical note: open addressing is usually still comfortable up to roughly alpha <= 0.7;\n"
        "near 0.9 probe lengths become large and performance degrades strongly.\n",
        encoding="utf-8",
    )


def main() -> None:
    seq1 = load_seq1()

    open_90 = run_open_addressing(seq1, 90)
    open_89 = run_open_addressing(seq1, 89)
    chaining_20 = run_chaining(seq1, 20)

    max_cov_90 = max_probe_coverage(seq1, 90)
    max_cov_89 = max_probe_coverage(seq1, 89)

    theo_05 = 1.0 / (1.0 - 0.5)
    theo_09 = 1.0 / (1.0 - 0.9)

    write_answers(open_90, open_89, chaining_20, max_cov_90, max_cov_89, theo_05, theo_09)

    print("Task 4 finished.")
    print(f"m=90 inserted/rejected: {open_90['inserted']}/{open_90['rejected']}")
    print(f"m=89 inserted/rejected: {open_89['inserted']}/{open_89['rejected']}")
    print(f"chaining m=20 inserted: {chaining_20['inserted']}")


if __name__ == "__main__":
    main()
