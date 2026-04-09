import random
from utils.algo_context import AlgoContext
from utils.algo_array import Array
from utils.algo_int import Int


def binary_search(z: Array, s: Int, l: int = None, r: int = None):
    """
    Binäre Suche auf dem sortierten Array z nach dem Wert s.

    l, r  – 0-basierte Grenzen (plain int, optional).
    Gibt den Index als plain int zurück, oder None wenn nicht gefunden.
    """
    if l is None:
        l = 0
    if r is None:
        r = len(z) - 1
    if l > r:
        return None

    m = Int((l + r) // 2, s._ctx)
    if s < z[m]:
        return binary_search(z, s, l, int(m) - 1)
    elif s > z[m]:
        return binary_search(z, s, int(m) + 1, r)
    else:
        return int(m)


def analyze_complexity(sizes):
    ctx = AlgoContext()
    for size in sizes:
        ctx.reset()
        z = Array.sorted(size, ctx)
        search_value = Int(random.randint(0, size - 1), ctx)
        binary_search(z, search_value)
        ctx.save_stats(size)

    ctx.plot_stats(["comparisons", "additions"])


if __name__ == "__main__":
    ctx = AlgoContext()
    arr = Array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ctx)
    s = Int(8, ctx)
    result = binary_search(arr, s)
    if result is not None:
        print(f"Value {s} found at index {result}.")
    else:
        print(f"Value {s} not found.")

    sizes = range(1, 1001, 2)
    analyze_complexity(sizes)
