"""
Daniel Baer
20.05.2026

mINF4/1, V06, Task 2 "Check HashTableChaining with seq0"

aufgabe2_chaining_seq0.py

This script verifies the chaining implementation on seq0 with table size 20.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
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
from vorlesung.L07_hashtable.analyze_hashtable import h  # type: ignore[import-not-found]


class HashTableChaining:
    """Hash table with separate chaining (one Python list per slot)."""

    def __init__(self, m: int, h_fun: Callable[[Int, Int], Int], ctx: AlgoContext):
        self.ctx = ctx
        self.m = Int(m, ctx)
        self.h = h_fun
        # Each slot holds a chain (list) of keys.
        self.table: list[list[Int]] = [[] for _ in range(m)]
        self.n = 0

    def _wrap(self, x: int | Int) -> Int:
        """Convert plain int values to Int for consistent instrumentation."""
        if isinstance(x, Int):
            return x
        return Int(x, self.ctx)

    def _slot(self, x: Int) -> int:
        """Compute the slot index with the provided hash function."""
        return int(self.h(x, self.m))

    def insert(self, x: int | Int) -> bool:
        """Insert x into its chain unless it already exists."""
        key = self._wrap(x)
        idx = self._slot(key)
        for current in self.table[idx]:
            if current == key:
                return True
        self.table[idx].append(key)
        self.n += 1
        return True

    def search(self, x: int | Int) -> bool:
        """Return True if x is present, otherwise False."""
        key = self._wrap(x)
        idx = self._slot(key)
        for current in self.table[idx]:
            if current == key:
                return True
        return False

    def delete(self, x: int | Int) -> bool:
        """Remove x from the chain if available."""
        key = self._wrap(x)
        idx = self._slot(key)
        chain = self.table[idx]
        for pos, current in enumerate(chain):
            if current == key:
                del chain[pos]
                self.n -= 1
                return True
        return False

    def alpha(self) -> float:
        """Return load factor n/m."""
        return self.n / int(self.m)

    def __str__(self) -> str:
        """Render all slots, including empty ones."""
        lines: list[str] = []
        for idx, chain in enumerate(self.table):
            values = ", ".join(str(int(key)) for key in chain)
            lines.append(f"{idx:2d}: [{values}]")
        return "\n".join(lines)


def load_seq0() -> list[int]:
    """Load integers from data/seq0.txt."""
    seq_file = ALGODAT_DIR / "data" / "seq0.txt"
    with seq_file.open("r", encoding="utf-8") as f:
        return [int(line.strip()) for line in f if line.strip()]


def write_answers(
    alpha_after_insert: float,
    deleted_52: bool,
    slot_52: int,
    slot_before: str,
    slot_after: str,
    alpha_after_reinsert: float,
    table_after_delete: str,
) -> None:
    """Write answers for questions 2a to 2d."""
    out = TASK_DIR / "antworten.txt"
    out.write_text(
        "Task 2 - HashTableChaining with m=20 and seq0\n\n"
        "2a) Load factor after inserting seq0 once:\n"
        f"alpha = {alpha_after_insert:.4f}\n\n"
        "2b) Delete value 52 and verify the affected chain:\n"
        f"slot for 52 = {slot_52}\n"
        f"chain before delete: {slot_before}\n"
        f"delete(52) returned: {deleted_52}\n"
        f"chain after delete: {slot_after}\n"
        "Table after deleting 52:\n"
        f"{table_after_delete}\n\n"
        "2c) Insert seq0 again:\n"
        f"alpha after second insert pass = {alpha_after_reinsert:.4f}\n"
        f"alpha > 1 ? {alpha_after_reinsert > 1.0}\n"
        "Can insert ever return False for chaining? No, not due to capacity.\n"
        "Duplicates are ignored, but insertion does not fail because of full table.\n\n"
        "2d) Why no DELETED_MARK in chaining?\n"
        "In separate chaining, each slot stores an independent list.\n"
        "Removing one key from that list does not break probe sequences of other keys,\n"
        "because search does not rely on tombstone markers across neighboring slots.\n",
        encoding="utf-8",
    )


def main() -> None:
    ctx = AlgoContext()
    seq0 = load_seq0()

    table = HashTableChaining(20, h, ctx)
    for value in seq0:
        table.insert(Int(value, ctx))

    alpha_after_insert = table.alpha()
    slot_52 = int(h(Int(52, ctx), Int(20, ctx)))
    slot_before = str([int(x) for x in table.table[slot_52]])

    deleted_52 = table.delete(Int(52, ctx))
    slot_after = str([int(x) for x in table.table[slot_52]])
    table_after_delete = str(table)

    for value in seq0:
        table.insert(Int(value, ctx))
    alpha_after_reinsert = table.alpha()

    write_answers(
        alpha_after_insert,
        deleted_52,
        slot_52,
        slot_before,
        slot_after,
        alpha_after_reinsert,
        table_after_delete,
    )

    print("Task 2 finished.")
    print(f"alpha after first insert: {alpha_after_insert:.4f}")
    print(f"slot(52) = {slot_52}")
    print(f"chain before delete: {slot_before}")
    print(f"chain after delete:  {slot_after}")
    print(f"alpha after second insert: {alpha_after_reinsert:.4f}")


if __name__ == "__main__":
    main()
