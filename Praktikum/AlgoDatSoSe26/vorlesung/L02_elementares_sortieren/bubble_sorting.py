from utils.algo_context import AlgoContext
from utils.algo_array import Array
from utils.algo_range import Range


def bubble_sort_stepwise(z: Array, ctx: AlgoContext):
    """
    Bubble Sort – schrittweise Variante (Generator).

    Gibt nach jedem Tausch den aktuellen Array-Zustand zurück.
    Wird von bubble_game.py für die Visualisierung verwendet.
    """
    n = len(z)
    for i in Range(n - 1):
        for j in Range(n - 1, i, -1):
            if z[j - 1] > z[j]:
                z.swap(j - 1, j)
                yield z


def bubble_sort2_stepwise(z: Array, ctx: AlgoContext):
    """
    Optimierter Bubble Sort mit Frühausstieg – schrittweise Variante.

    Bricht ab, wenn in einem Durchlauf kein Tausch stattgefunden hat.
    """
    n = len(z)
    while True:
        swapped = False
        for i in Range(n - 1):
            if z[i] > z[i + 1]:
                z.swap(i, i + 1)
                swapped = True
                yield z
        n -= 1
        if not swapped or n <= 1:
            break


def bubble_sort(z: Array, ctx: AlgoContext):
    """Bubble Sort – vollständige Ausführung ohne Visualisierung."""
    for _ in bubble_sort_stepwise(z, ctx):
        pass


def bubble_sort2(z: Array, ctx: AlgoContext):
    """Optimierter Bubble Sort – vollständige Ausführung ohne Visualisierung."""
    for _ in bubble_sort2_stepwise(z, ctx):
        pass


def analyze_complexity(sort_func, sizes, presorted=False):
    """
    Analysiert die Komplexität einer Sortierfunktion über mehrere Eingabegrößen.

    Parameters
    ----------
    sort_func : callable
        Signatour: sort_func(z: Array, ctx: AlgoContext)
    sizes : list[int]
        Eingabegrößen für die Analyse.
    presorted : bool
        True → sortiertes Eingabe-Array (Best-Case-Analyse).
    """
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
    analyze_complexity(bubble_sort,  [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
#   analyze_complexity(bubble_sort2, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
#   analyze_complexity(bubble_sort,  [10, 20, 30, 40, 50, 60, 70, 80, 90, 100], True)
#   analyze_complexity(bubble_sort2, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100], True)
