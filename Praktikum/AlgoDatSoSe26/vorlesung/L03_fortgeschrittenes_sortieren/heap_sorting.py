from utils.algo_context import AlgoContext
from utils.algo_array import Array


# Heap verwendet 1-basierte Indizierung intern;
# adjust_index() rechnet auf 0-basierte Array-Positionen um.

def left_child(i: int) -> int:
    return 2 * i

def right_child(i: int) -> int:
    return 2 * i + 1

def adjust_index(i: int) -> int:
    """Konvertiert 1-basierten Heap-Index in 0-basierten Array-Index."""
    return i - 1


def heap_sort_stepwise(z: Array, ctx: AlgoContext):
    """
    Heapsort – schrittweise Variante (Generator).

    Baut zunächst einen Max-Heap auf, dann sortiert er durch Tauschen.
    """
    n = len(z)
    yield from make_max_heap(z, n, ctx)
    heapsize = n
    for i in range(n, 1, -1):
        z.swap(0, i - 1)
        yield z
        heapsize -= 1
        yield from max_heapify(z, 1, heapsize, ctx)


def heap_sort(z: Array, ctx: AlgoContext):
    """Heapsort – vollständige Ausführung ohne Visualisierung."""
    for _ in heap_sort_stepwise(z, ctx):
        pass


def make_max_heap(z: Array, n: int, ctx: AlgoContext):
    """Baut einen Max-Heap in-place auf."""
    for i in range(n // 2, 0, -1):
        yield from max_heapify(z, i, n, ctx)


def max_heapify(z: Array, i: int, heapsize: int, ctx: AlgoContext):
    """
    Stellt die Max-Heap-Eigenschaft für den Teilbaum bei Index i wieder her.

    i und heapsize sind plain int (1-basiert). Vergleiche auf Array-Inhalten
    werden über Int automatisch gezählt.
    """
    l = left_child(i)
    r = right_child(i)
    max_val = i

    if l <= heapsize and z[adjust_index(l)] > z[adjust_index(i)]:
        max_val = l
    if r <= heapsize and z[adjust_index(r)] > z[adjust_index(max_val)]:
        max_val = r

    if max_val != i:
        z.swap(adjust_index(i), adjust_index(max_val))
        yield z
        yield from max_heapify(z, max_val, heapsize, ctx)


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
    sizes = range(10, 101, 10)
    analyze_complexity(heap_sort, sizes)
