from utils.algo_context import AlgoContext
from utils.algo_array import Array
from utils.algo_int import Int


def quick_sort_stepwise(z: Array, ctx: AlgoContext, l: int = 0, r: int = None):
    """
    Quicksort – schrittweise Variante (Generator).

    l, r sind 0-basierte Grenzen (plain int). Alle Vergleiche auf Array-Inhalten
    werden über Int automatisch gezählt.
    """
    if r is None:
        r = len(z) - 1
    if l < r:
        q = partition(z, l, r, ctx)
        yield z
        yield from quick_sort_stepwise(z, ctx, l, q - 1)
        yield from quick_sort_stepwise(z, ctx, q + 1, r)
        yield z


def partition(z: Array, l: int, r: int, ctx: AlgoContext) -> int:
    """
    Lomuto-Partitionierung.

    Wählt z[r] als Pivot. Gibt den endgültigen Pivot-Index zurück.
    """
    pivot = Int(z[r].value, ctx)   # Pivot-Wert kopieren
    ctx.reads += 1
    i = Int(l, ctx)
    j = Int(r - 1, ctx)

    while i < j:
        while int(i) <= int(j) and z[i] < pivot:
            i += 1
        while int(j) >= l and z[j] >= pivot:
            j -= 1
        if i < j:
            z.swap(int(i), int(j))
            i += 1
            j -= 1

    if i == j and z[i] < pivot:
        i += 1
    if z[i] != pivot:
        z.swap(int(i), r)

    return int(i)


def quick_sort(z: Array, ctx: AlgoContext, l: int = None, r: int = None):
    """Quicksort – vollständige Ausführung ohne Visualisierung."""
    if l is None:
        l = 0
    if r is None:
        r = len(z) - 1
    for _ in quick_sort_stepwise(z, ctx, l, r):
        pass


def analyze_complexity(sort_func, sizes, presorted=False):
    ctx = AlgoContext()
    for size in sizes:
        ctx.reset()
        if presorted:
            z = Array.sorted(size, ctx)
        else:
            z = Array.random(size, -100, 100, ctx)
        sort_func(z, ctx)
        ctx.save_stats(size)

    ctx.plot_stats(["comparisons", "writes"])


if __name__ == '__main__':
    sizes = range(10, 101, 5)
    analyze_complexity(quick_sort, sizes)
#   analyze_complexity(quick_sort, sizes, True)
