from utils.algo_context import AlgoContext
from utils.algo_array import Array
from utils.algo_int import Int
from utils.algo_range import Range


def insert_sort_stepwise(z: Array, ctx: AlgoContext):
    """
    Insertion Sort – schrittweise Variante (Generator).

    Gibt nach jedem Einfügevorgang den aktuellen Array-Zustand zurück.
    """
    n = len(z)
    elem = Int(0, ctx)   # Zwischenregister für das einzufügende Element

    for i in Range(n):
        elem.set(z[i])               # 1 read + 1 write
        j = Int(int(i), ctx)
        while j > 0 and z[j - 1] > elem:
            z[j] = z[j - 1]         # 1 read + 1 write
            j -= 1
            yield z
        z[j] = elem                  # 1 read + 1 write
        yield z


def insert_sort(z: Array, ctx: AlgoContext):
    """Insertion Sort – vollständige Ausführung ohne Visualisierung."""
    for _ in insert_sort_stepwise(z, ctx):
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
    analyze_complexity(insert_sort, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
#   analyze_complexity(insert_sort, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100], True)
