from utils.algo_context import AlgoContext
from utils.algo_array import Array
from utils.algo_int import Int
from utils.algo_range import Range


def max_sequence_1(z: Array, ctx: AlgoContext):
    """O(n³) – dreifach verschachtelte Schleife."""
    n = len(z)
    m = Int(float('-inf'), ctx)
    s = Int(0, ctx)
    l = Int(0, ctx)
    r = Int(0, ctx)

    for i in Range(n):
        for j in Range(int(i), n):
            s.set(0)
            for k in Range(int(i), int(j)):
                s += z[k]
            if s > m:
                m.set(s)
                l.set(Int(int(i), ctx))
                r.set(Int(int(j), ctx))
    return m, l, r


def max_sequence_2(z: Array, ctx: AlgoContext):
    """O(n²) – doppelt verschachtelte Schleife."""
    n = len(z)
    m = Int(float('-inf'), ctx)
    s = Int(0, ctx)
    left = Int(0, ctx)
    right = Int(0, ctx)

    for i in Range(n):
        s.set(0)
        for j in Range(int(i), n):
            s += z[j]
            if s > m:
                m.set(s)
                left.set(Int(int(i), ctx))
                right.set(Int(int(j), ctx))
    return m, left, right




def max_sequence_4(z: Array, ctx: AlgoContext):
    """O(n) – Kadane's Algorithmus."""
    n = len(z)
    m = Int(float('-inf'), ctx)
    cur_sum = Int(0, ctx)
    cur_left = Int(0, ctx)
    left = Int(0, ctx)
    right = Int(0, ctx)

    for i in Range(n):
        cur_sum += z[i]
        if cur_sum > m:
            m.set(cur_sum)
            left.set(cur_left)
            right.set(Int(int(i), ctx))
        if cur_sum < 0:
            cur_sum.set(0)
            cur_left.set(Int(int(i) + 1, ctx))

    return m, left, right


def example(max_sequence_func):
    ctx = AlgoContext()
    data = [-59, 52, 46, 14, -50, 58, -87, -77, 34, 15]
    print(data)
    z = Array(data, ctx)
    m, l, r = max_sequence_func(z, ctx)
    print(m, l, r)


def seq(filename, max_sequence_func):
    ctx = AlgoContext()
    z = Array.from_file(filename, ctx)
    m, l, r = max_sequence_func(z, ctx)
    print(m, l, r)


def analyze_complexity(max_sequence_func, sizes):
    ctx = AlgoContext()
    for size in sizes:
        ctx.reset()
        z = Array.random(size, -100, 100, ctx)
        max_sequence_func(z, ctx)
        ctx.save_stats(size)

    ctx.plot_stats(["additions"])


if __name__ == '__main__':
    example(max_sequence_2)
    for filename in ["data/seq0.txt", "data/seq1.txt"]:
        print(filename)
        seq(filename, max_sequence_2)
    analyze_complexity(max_sequence_2, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
