"""
Daniel Baer
25.05.2026

mINF4/1, V06, "Hashtabellen"

V06_hashtable_chaining.py


This module implements a hash table with chaining.
It follows the API style of HashTableOpenAddressing used in the lecture.
"""

from collections.abc import Callable

from utils.algo_context import AlgoContext
from utils.algo_int import Int


class HashTableChaining:
    def __init__(self, m: int, h: Callable[[Int, Int], Int], ctx: AlgoContext):
        self.ctx = ctx
        self.m = Int(m, ctx)
        self.h = h
        
        # each slot stores one chain (Python list) of Int keys
        self.table: list[list[Int]] = [[] for _ in range(m)]
        
        # total number of stored keys
        self.n = 0

    def _checkInt(self, x: int | Int) -> Int:
        """ check and normalize incoming values to Int """
        if isinstance(x, Int):
            return x
        return Int(x, self.ctx)

    def _hashSlot(self, x: Int) -> int:
        """ get slot index by using the provided hash function """
        return int(self.h(x, self.m))

    def insert(self, x: int | Int) -> bool:
        """ insert x if it is not already exists """
        key = self._checkInt(x)
        idx = self._hashSlot(key)

        # duplicate check (same as search)
        for current in self.table[idx]:
            if current == key:
                return False

        self.table[idx].append(key)
        self.n += 1
        return True

    def search(self, x: int | Int) -> bool:
        """Return True if x is present in its chain, otherwise False."""
       
        key = self._checkInt(x)
        idx = self._hashSlot(key)
        
        for current in self.table[idx]:
            if current == key:
                return True
            
        return False

    def delete(self, x: int | Int) -> bool:
        """ remove x from chain if present """
        key = self._checkInt(x)
        idx = self._hashSlot(key)
        chain = self.table[idx]

        for pos, current in enumerate(chain):
            if current == key:
                del chain[pos]
                self.n -= 1
                return True
        return False

    def alpha(self) -> float:
        """ load factor n/m """
        return self.n / int(self.m)

    def __str__(self) -> str:
        """ return all slots and their chains as a formatted string """
        lines: list[str] = []
        for idx, chain in enumerate(self.table):
            values = ", ".join(str(int(key)) for key in chain)
            lines.append(f"{idx:2d}: [{values}]")
        return "\n".join(lines)
