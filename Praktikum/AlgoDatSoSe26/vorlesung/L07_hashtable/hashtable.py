from collections.abc import Callable
from utils.algo_context import AlgoContext
from utils.algo_array import Array
from utils.algo_int import Int
from utils.algo_range import Range


UNUSED_MARK  = "UNUSED"
DELETED_MARK = "DELETED"


class HashTableOpenAddressing:
    """
    Hashtabelle mit offener Adressierung.

    f  – Sondierungsfunktion  f(x: Int, i: Int, m: Int) -> Int
         Liefert die Tabellenposition für Schlüssel x beim i-ten Versuch.
    """

    def __init__(self, m: int, f: Callable[[Int, Int, Int], Int], ctx: AlgoContext):
        self.ctx = ctx
        self.m = Int(m, ctx)
        self.f = f
        self.table = Array([UNUSED_MARK] * m, ctx)

    def insert(self, x: Int) -> bool:
        i = Int(0, self.ctx)
        while i < self.m:
            j = self.f(x, i, self.m)
            if self.is_free(j):
                self.table[j] = x
                return True
            i += 1
        return False

    def search(self, x: Int) -> bool:
        i = Int(0, self.ctx)
        while i < self.m:
            j = self.f(x, i, self.m)
            if self.is_unused(j):
                return False
            if self.table[j] == x:
                return True
            i += 1
        return False

    def delete(self, x: Int) -> bool:
        i = Int(0, self.ctx)
        while i < self.m:
            j = self.f(x, i, self.m)
            if self.is_unused(j):
                return False
            if self.table[j] == x:
                self.table[j].set(DELETED_MARK)   # Tombstone setzen (1 write)
                return True
            i += 1
        return False

    def __str__(self):
        return str(self.table)

    def alpha(self) -> float:
        """Belegungsfaktor der Tabelle."""
        used = sum(0 if self.is_free(Int(i, self.ctx)) else 1
                   for i in range(int(self.m)))
        return used / int(self.m)

    def is_unused(self, i: Int) -> bool:
        return self.table[i].value == UNUSED_MARK

    def is_deleted(self, i: Int) -> bool:
        return self.table[i].value == DELETED_MARK

    def is_free(self, i: Int) -> bool:
        return self.is_unused(i) or self.is_deleted(i)
