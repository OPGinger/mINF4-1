"""
Daniel Baer
20.05.2026

mINF4/1, V06, Shared Module "HashTableChaining"

hashtable_chaining.py

This module implements a hash table with separate chaining.
It follows the API style of HashTableOpenAddressing used in the lecture project.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.algo_context import AlgoContext
from utils.algo_int import Int


class HashTableChaining:
    """Hash table with separate chaining (a Python list per slot)."""

    def __init__(self, m: int, h: Callable[[Int, Int], Int], ctx: AlgoContext):
        self.ctx = ctx
        self.m = Int(m, ctx)
        self.h = h
        # Each table slot stores one chain (Python list) of Int keys.
        self.table: list[list[Int]] = [[] for _ in range(m)]
        # Total number of stored keys across all chains.
        self.n = 0

    def _wrap(self, x: int | Int) -> Int:
        """Normalize incoming values to Int so comparisons are instrumented."""
        if isinstance(x, Int):
            return x
        return Int(x, self.ctx)

    def _slot(self, x: Int) -> int:
        """Compute the slot index for x using the provided hash function h."""
        return int(self.h(x, self.m))

    def insert(self, x: int | Int) -> bool:
        """
        Insert x if it is not already present.

        For chaining, insertion does not fail due to table fullness.
        Therefore this method returns True for all valid inputs.
        """
        key = self._wrap(x)
        idx = self._slot(key)

        # Duplicate protection required by the assignment.
        for current in self.table[idx]:
            if current == key:
                return True

        self.table[idx].append(key)
        self.n += 1
        return True

    def search(self, x: int | Int) -> bool:
        """Return True if x is present in its chain, otherwise False."""
        key = self._wrap(x)
        idx = self._slot(key)
        for current in self.table[idx]:
            if current == key:
                return True
        return False

    def delete(self, x: int | Int) -> bool:
        """Remove x from its chain if present, and return deletion status."""
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
        """Load factor n/m with n as total keys across all chains."""
        return self.n / int(self.m)

    def keys(self) -> list[Int]:
        """Return a flat list of currently stored keys (for analysis scripts)."""
        flat: list[Int] = []
        for chain in self.table:
            flat.extend(chain)
        return flat

    def __str__(self) -> str:
        """Render all slots including empty chains."""
        lines: list[str] = []
        for idx, chain in enumerate(self.table):
            values = ", ".join(str(int(key)) for key in chain)
            lines.append(f"{idx:2d}: [{values}]")
        return "\n".join(lines)
