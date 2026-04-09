import math
import random
from utils.algo_context import AlgoContext
from utils.algo_int import Int
from utils.algo_array import Array
from vorlesung.L07_hashtable.hashtable import HashTableOpenAddressing

# Goldener Schnitt (Konstante, nicht instrumentiert)
_A = (math.sqrt(5) - 1) / 2


def h(x: Int, m: Int) -> Int:
    """Hashfunktion nach multiplikativer Methode."""
    full = x.value * _A
    return Int(int(abs(full - int(full)) * int(m)), x._ctx)


def f(x: Int, i: Int, m: Int) -> Int:
    """Quadratische Sondierung."""
    c1, c2 = 1, 5
    base = int(h(x, m))
    probe = base + c1 * int(i) + c2 * int(i) ** 2
    return Int(probe % int(m), x._ctx)


def fs(x: Int, i: Int, m: Int) -> Int:
    """Symmetrische quadratische Sondierung."""
    base = int(h(x, m))
    sq = int(i) ** 2
    if int(i) % 2 == 0:
        probe = base + sq
    else:
        probe = base - sq
    return Int(probe % int(m), x._ctx)


def analyze_complexity(sizes):
    ctx = AlgoContext()
    for size in sizes:
        ctx.reset()
        ht = HashTableOpenAddressing(size, f, ctx)
        z = Array.random(size, -100, 100, ctx)
        for cell in z:
            ht.insert(cell)
        ctx.reset()
        target = z[random.randint(0, size - 1)]
        ht.search(target)
        ctx.save_stats(size)

    ctx.plot_stats(["comparisons"])


if __name__ == "__main__":
    sizes = range(1, 1001, 10)
    analyze_complexity(sizes)
