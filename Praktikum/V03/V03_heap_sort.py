"""
Daniel Baer
01.05.2026

mINF4/1, V03, "Heap Sort"

V03_heap_sort.py

This application implements the Heap Sort algorithm to sort an array of integers.
"""

# import necessary modules and classes
import sys
import time

# add path of AlgoDatSoSe26 directory
sys.path.insert(0, 'AlgoDatSoSe26')

# import classes from utils module
from utils.algo_context import AlgoContext
from utils.algo_array import Array


def heapify(arr: Array, n: int, i: int) -> None:
    """Sift down the node at index i in a heap of size n."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr.swap(i, largest)
        heapify(arr, n, largest)


def build_max_heap(arr: Array) -> Array:
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    return arr


def heap_sort(arr: Array, ctx: AlgoContext) -> Array:
    n = len(arr)
    build_max_heap(arr)

    for i in range(n - 1, 0, -1):
        arr.swap(0, i)
        heapify(arr, i, 0)

    return arr


# helper function to check if array is sorted
def is_sorted(arr: Array) -> bool:
    for i in range(1, len(arr)):
        if int(arr[i]) < int(arr[i - 1]):
            return False
    return True


    
def main() -> None:
    ctx = AlgoContext()
    results = []

    for i in range(4):
        filename = f"AlgoDatSoSe26/data/seq{i}.txt"
        with open(filename, 'r') as f:
            sequence = [int(line.strip()) for line in f if line.strip()]

        ctx.reset()
        arr = Array(sequence, ctx)
        start_time = time.time()
        sorted_arr = heap_sort(arr, ctx)
        end_time = time.time()

        results.append(
            (f"seq{i}",
                f"{len(sequence)}",
                f"{ctx.comparisons}",
                f"{is_sorted(sorted_arr)}",
                f"{((end_time - start_time) * 1000):.4f} ms"))
    
    print("Heap Sort:")
    print("{:>10} {:>10} {:>15} {:>10} {:>15}".format("Sequence", "Size","Comparisons", "Sorted", "Duration"))
    for result in results:
        print("{:>10} {:>10} {:>15} {:>10} {:>15}".format(*result))
    print()


if __name__ == '__main__':
    main()
