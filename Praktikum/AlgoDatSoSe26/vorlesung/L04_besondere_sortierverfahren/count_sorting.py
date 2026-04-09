from utils.algo_context import AlgoContext
from utils.algo_array import Array
from utils.algo_range import Range


def count_sort(a: Array, b: Array, k: int, ctx: AlgoContext):
    """
    Counting Sort.

    a  – Eingabe-Array mit Werten aus [0, k]
    b  – Ausgabe-Array (gleiche Länge wie a)
    k  – maximaler Wert in a
    """
    c = Array([0] * (k + 1), ctx)   # Zählarray

    # Häufigkeiten zählen
    for j in Range(len(a)):
        c[a[j]] = c[a[j]] + 1

    # Kumulierte Summen bilden
    for i in Range(1, k + 1):
        c[i] = c[i] + c[i - 1]

    # Stabil in b einsortieren (rückwärts für Stabilität)
    for j in Range(len(a) - 1, -1, -1):
        b[c[a[j]] - 1] = a[j]
        c[a[j]] = c[a[j]] - 1


def analyze_complexity(sizes, presorted=False):
    ctx = AlgoContext()
    for size in sizes:
        ctx.reset()
        if presorted:
            z = Array.sorted(size, ctx)
        else:
            z = Array.random(size, 0, 100, ctx)
        dest = Array([0] * size, ctx)
        count_sort(z, dest, 100, ctx)
        ctx.save_stats(size)

    ctx.plot_stats(["reads", "writes"])


if __name__ == '__main__':
    ctx = AlgoContext()
    a = Array([2, 5, 3, 0, 2, 3, 0, 3], ctx)
    b = Array([0] * len(a), ctx)
    count_sort(a, b, 5, ctx)
    print(b)

    sizes = range(10, 101, 10)
    analyze_complexity(sizes)
