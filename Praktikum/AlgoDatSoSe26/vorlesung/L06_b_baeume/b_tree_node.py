from utils.algo_context import AlgoContext
from utils.algo_array import Array


class BTreeNode:
    """
    Knoten eines B-Baums.

    value  – Array der Schlüssel (Kapazität: 2m-1)
    n      – Anzahl aktuell gespeicherter Schlüssel
    leaf   – True wenn Blattknoten
    loaded_count / saved_count – Disk-I/O-Zähler für externe Komplexitätsanalyse
    """

    def __init__(self, m: int, ctx: AlgoContext):
        self.m = m
        self.ctx = ctx
        self.n = 0
        self.leaf = True
        self.value = Array([0] * (2 * m - 1), ctx)
        self.children = [None] * (2 * m)
        self.loaded_count = 0
        self.saved_count = 0

    def load(self):
        self.loaded_count += 1

    def save(self):
        self.saved_count += 1

    def __str__(self):
        return "(" + " ".join([str(self.value[i]) for i in range(self.n)]) + ")"
