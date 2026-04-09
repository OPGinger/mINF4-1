from __future__ import annotations
from random import randint
from utils.algo_context import AlgoContext, _NullContext, NULL_CTX
from utils.algo_int import Int
from utils.algo_path import path


class Array:
    """
    Instrumentiertes Array.

    Jede Zelle ist ein Int-Objekt, das Operationen an den gemeinsamen
    AlgoContext meldet.

    Zugriff
    -------
    arr[i]         gibt die Int-Zelle zurück (kein Zähler)
    arr[i] = v     setzt den Wert der Zelle (1 write, +1 read falls v ein Int)
    len(arr)       gibt plain int zurück
    arr.length()   gibt Int zurück (für Algorithmen nützlich)
    arr.swap(i,j)  tauscht zwei Elemente (2 reads + 2 writes)

    Hinweis: arr[i] gibt eine Referenz auf die Zelle zurück.
    Lesende Verwendung (Vergleich, Arithmetik) zählt dort – nicht beim Zugriff selbst.

    Fabrikmethoden
    --------------
    Array.random(n, min_val, max_val, ctx)   zufällige Werte
    Array.sorted(n, ctx)                     aufsteigend sortiert  0..n-1
    Array.from_file(filename, ctx)           Werte aus Textdatei (eine Zahl pro Zeile)

    Beispiel
    --------
    ctx = AlgoContext()
    z = Array.random(10, 0, 99, ctx)
    if z[0] > z[1]:          # 2 reads, 1 comparison
        z.swap(0, 1)          # 2 reads, 2 writes
    """

    def __init__(self, data: list, ctx: AlgoContext | _NullContext):
        self._ctx = ctx
        self._cells = [Int(v, ctx) for v in data]

    # ------------------------------------------------------------------
    # Element-Zugriff
    # ------------------------------------------------------------------

    def __getitem__(self, index) -> Int:
        """Gibt die Int-Zelle zurück. Kein Zähler – Zählung erfolgt bei Nutzung."""
        return self._cells[int(index)]

    def __setitem__(self, index, value):
        """
        Setzt den Wert der Zelle.

        Delegiert an Int.set() → 1 write  (+1 read falls value ein Int ist).
        """
        self._cells[int(index)].set(value)

    # ------------------------------------------------------------------
    # Länge
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._cells)

    def length(self) -> Int:
        """Gibt die Länge als Int zurück (für Algorithmen, die mit Int rechnen)."""
        return Int(len(self._cells), self._ctx)

    # ------------------------------------------------------------------
    # Iteration
    # ------------------------------------------------------------------

    def __iter__(self):
        return iter(self._cells)

    # ------------------------------------------------------------------
    # Tausch
    # ------------------------------------------------------------------

    def swap(self, i, j):
        """
        Tauscht die Werte an Position i und j.

        Zählt: 2 reads + 2 writes.
        """
        ci = self._cells[int(i)]
        cj = self._cells[int(j)]
        self._ctx.reads += 2
        self._ctx.writes += 2
        ci._value, cj._value = cj._value, ci._value

    # ------------------------------------------------------------------
    # Darstellung
    # ------------------------------------------------------------------

    def __str__(self):
        return '[' + ', '.join(str(c) for c in self._cells) + ']'

    def __repr__(self):
        return f"Array({[c.value for c in self._cells]})"

    # ------------------------------------------------------------------
    # Fabrikmethoden
    # ------------------------------------------------------------------

    @staticmethod
    def random(n: int, min_val: int, max_val: int, ctx: AlgoContext) -> Array:
        """Erzeugt ein Array mit n zufälligen Werten aus [min_val, max_val]."""
        n = int(n)
        return Array([randint(min_val, max_val) for _ in range(n)], ctx)

    @staticmethod
    def sorted(n: int, ctx: AlgoContext) -> Array:
        """Erzeugt ein aufsteigend sortiertes Array  0, 1, …, n-1."""
        n = int(n)
        return Array(list(range(n)), ctx)

    @staticmethod
    def from_file(filename: str, ctx: AlgoContext, limit: int | None = None) -> Array:
        """
        Liest Ganzzahlen aus einer Textdatei (eine Zahl pro Zeile).

        Parameters
        ----------
        filename : str
            Pfad relativ zum Projektverzeichnis oder absolut.
        ctx : AlgoContext
        limit : int | None
            Optionale Obergrenze für die Anzahl eingelesener Zeilen.
        """
        filepath = path(filename)
        with open(filepath) as f:
            lines = f.readlines()
        if limit is not None:
            lines = lines[:limit]
        data = [int(line.strip()) for line in lines if line.strip()]
        return Array(data, ctx)
