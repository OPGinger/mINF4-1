from utils.algo_context import AlgoContext
from utils.algo_array import Array
from utils.algo_int import Int
from utils.algo_range import Range


def select_sort_stepwise(z: Array, ctx: AlgoContext):
    """
    Selection Sort – schrittweise Variante (Generator).

    Gibt nach jedem Platztausch den aktuellen Array-Zustand zurück.
    """
    n = len(z)
    cur_min = Int(0, ctx)   # Index des aktuellen Minimums

    for i in Range(n):
        cur_min.set(Int(int(i), ctx))
        for j in Range(int(i) + 1, n):
            if z[j] < z[cur_min]:
                cur_min.set(Int(int(j), ctx))
        z.swap(int(i), int(cur_min))
        yield z


def select_sort(z: Array, ctx: AlgoContext):
    """Selection Sort – vollständige Ausführung ohne Visualisierung."""
    for _ in select_sort_stepwise(z, ctx):
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
    analyze_complexity(select_sort, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
#   analyze_complexity(select_sort, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100], True)
