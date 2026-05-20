"""
Daniel Baer
20.05.2026

mINF4/1, V06, Task 3 "Open Addressing with seq0"

aufgabe3_open_addressing_seq0.py

This script analyzes delete/search behavior for open addressing with m=20.
"""

from __future__ import annotations

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


DELETED_MARK = "DELETED"
UNUSED_MARK = "UNUSED"


def load_seq0() -> list[int]:
    """Load integers from data/seq0.txt."""
    seq_file = ALGODAT_DIR / "data" / "seq0.txt"
    with seq_file.open("r", encoding="utf-8") as f:
        return [int(line.strip()) for line in f if line.strip()]


def find_value_slot(ht: HashTableOpenAddressing, value: int, ctx: AlgoContext) -> int:
    """Locate the slot index currently storing value, or -1 if absent."""
    for idx in range(int(ht.m)):
        cell = ht.table[Int(idx, ctx)].value
        if cell == value:
            return idx
    return -1


def first_free_probe_index(ht: HashTableOpenAddressing, value: int, ctx: AlgoContext) -> tuple[int, list[int]]:
    """Compute manual probe sequence and first free slot for value."""
    probes: list[int] = []
    key = Int(value, ctx)
    for i in range(int(ht.m)):
        j = int(f(key, Int(i, ctx), ht.m))
        probes.append(j)
        cell_value = ht.table[Int(j, ctx)].value
        if cell_value in (UNUSED_MARK, DELETED_MARK):
            return j, probes
    return -1, probes


def find_collision_partner(base_value: int, m: int, ctx: AlgoContext) -> int:
    """Find another key with same h(x, m) as base_value for a concrete counterexample."""
    base = int(h(Int(base_value, ctx), Int(m, ctx)))
    for candidate in range(-1000, 1001):
        if candidate == base_value:
            continue
        slot = int(h(Int(candidate, ctx), Int(m, ctx)))
        if slot == base:
            return candidate
    return base_value + m


def write_answers(
    deleted_slot_before: int,
    deleted_slot_after_value: str,
    counter_x: int,
    counter_y: int,
    counter_h: int,
    manual_slot_24: int,
    actual_slot_24: int,
    probe_sequence_24: list[int],
    table_after_delete: str,
    table_after_insert_24: str,
) -> None:
    """Write answers for questions 3a to 3d."""
    out = TASK_DIR / "antworten.txt"
    out.write_text(
        "Task 3 - Open Addressing with m=20 and seq0\n\n"
        "3a) After deleting 52:\n"
        f"slot containing 52 before delete: {deleted_slot_before}\n"
        f"content of this slot after delete: {deleted_slot_after_value}\n"
        "(The slot contains DELETED, not UNUSED.)\n"
        "Table after deleting 52:\n"
        f"{table_after_delete}\n\n"
        "3b) Why continue search on DELETED but stop on UNUSED?\n"
        "DELETED means this slot was part of a probe chain in the past, so the key\n"
        "might still appear later in the same chain. UNUSED means no key has ever\n"
        "been placed at this probe position, so the chain ends and search can stop.\n\n"
        "3c) What breaks if delete sets UNUSED instead of DELETED?\n"
        f"Concrete example with m=20: choose x={counter_x} and y={counter_y} with h(x)=h(y)={counter_h}.\n"
        "Insert x first, then y. y is stored at a later probe position.\n"
        "If x is deleted and marked UNUSED, searching y stops too early at x's old slot\n"
        "and incorrectly returns False. So search becomes faulty.\n\n"
        "3d) Insert 24 after deleting 52:\n"
        f"manual probe sequence for 24: {probe_sequence_24}\n"
        f"first free slot by manual probing: {manual_slot_24}\n"
        f"actual slot after insert(24): {actual_slot_24}\n"
        f"manual result equals actual result? {manual_slot_24 == actual_slot_24}\n"
        "Table after inserting 24:\n"
        f"{table_after_insert_24}\n",
        encoding="utf-8",
    )


def main() -> None:
    ctx = AlgoContext()
    seq0 = load_seq0()

    ht = HashTableOpenAddressing(20, f, ctx)
    for value in seq0:
        ht.insert(Int(value, ctx))

    slot_52_before = find_value_slot(ht, 52, ctx)
    ht.delete(Int(52, ctx))

    if slot_52_before >= 0:
        slot_after_delete_value = str(ht.table[Int(slot_52_before, ctx)].value)
    else:
        slot_after_delete_value = "NOT_FOUND"

    table_after_delete = str(ht)

    # Construct a concrete collision pair for the counterexample in 3c.
    counter_x = 52
    counter_y = find_collision_partner(counter_x, 20, ctx)
    counter_h = int(h(Int(counter_x, ctx), Int(20, ctx)))

    manual_slot_24, probe_sequence_24 = first_free_probe_index(ht, 24, ctx)
    ht.insert(Int(24, ctx))
    actual_slot_24 = find_value_slot(ht, 24, ctx)
    table_after_insert_24 = str(ht)

    write_answers(
        slot_52_before,
        slot_after_delete_value,
        counter_x,
        counter_y,
        counter_h,
        manual_slot_24,
        actual_slot_24,
        probe_sequence_24,
        table_after_delete,
        table_after_insert_24,
    )

    print("Task 3 finished.")
    print(f"slot of 52 before delete: {slot_52_before}")
    print(f"slot content after delete: {slot_after_delete_value}")
    print(f"manual slot for 24: {manual_slot_24}")
    print(f"actual slot for 24: {actual_slot_24}")


if __name__ == "__main__":
    main()
