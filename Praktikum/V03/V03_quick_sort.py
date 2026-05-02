"""
Daniel Baer
01.05.2026

mINF4/1, V03, "Quick Sort"

V03_quick_sort.py


This application implements different variants of the Quick Sort algorithm to sort an array of integers.
"""

# import necessary modules and classes
import sys
import time

# add path of AlgoDatSoSe26 directory
sys.path.insert(0, 'AlgoDatSoSe26')

# import classes from utils module
from utils.algo_context import AlgoContext
from utils.algo_array import Array
from utils.algo_int import Int


# quicksort with rightmost element as pivot
def quicksort_r(arr : Array, left, right, ctx : AlgoContext):

    if left < right:
        # Partitioniere das Array und erhalte den Pivot-Index
        pivot_index = partition_alt_r(arr, left, right)

        # recursive sort of left and right subarrays
        quicksort_r(arr, left, pivot_index - 1, ctx)
        quicksort_r(arr, pivot_index + 1, right, ctx)

    return arr


# quicksort with leftmost element as pivot
def quicksort_l(arr : Array, left, right, ctx : AlgoContext):

    if left < right:
        # Partitioniere das Array und erhalte den Pivot-Index
        pivot_index = partition_alt_l(arr, left, right)

        # recursive sort of left and right subarrays
        quicksort_l(arr, left, pivot_index - 1, ctx)
        quicksort_l(arr, pivot_index + 1, right, ctx)

    return arr


# quicksort with median of pivot selection
def quicksort_m(arr : Array, left, right, ctx : AlgoContext):

    if left < right:
        # Partitioniere das Array und erhalte den Pivot-Index
        pivot_index = partition_alt_m(arr, left, right)

        # recursive sort of left and right subarrays
        quicksort_m(arr, left, pivot_index - 1, ctx)
        quicksort_m(arr, pivot_index + 1, right, ctx)

    return arr


# partition function for quicksort with rightmost element as pivot
def partition_alt_r(arr : Array, left, right):
    
    # take right element as pivot
    pivot = arr[right].value
    
    # index of element in front of the pivot
    i = left - 1
    
    # compare each element with the pivot
    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            
            # swap elements
            arr[i], arr[j] = arr[j].value, arr[i].value
    
    # swap elements
    arr[i + 1], arr[right] = arr[right].value, arr[i + 1].value
    
    return i + 1


# partition function for quicksort with leftmost element as pivot
def partition_alt_l(arr : Array, left, right):
    
    # take left element as pivot
    pivot = arr[left].value
    
    # index of element in front of the pivot
    i = left
    
    # compare each element with the pivot
    for j in range(left + 1, right + 1):
        if arr[j] <= pivot:
            i += 1
            
            # swap elements
            arr[i], arr[j] = arr[j].value, arr[i].value
    
    # swap elements
    arr[left], arr[i] = arr[i].value, arr[left].value
    
    return i


# partition function for quicksort with middle element as pivot
def partition_alt_m(arr : Array, left, right):
    
    mid = (left + right) // 2
    pivot = arr[mid]
    if(arr[left].value >= arr[mid].value >= arr[right].value or arr[left].value <= arr[mid].value <= arr[right].value):
        pivot = arr[mid]
    else:
        return partition_alt_l(arr, left, right)

    # index of element in front of the pivot
    i = left - 1
    
    # compare each element with the pivot
    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            
            # swap elements
            arr[i], arr[j] = arr[j].value, arr[i].value
    
    # swap elements
    arr[i + 1], arr[right] = arr[right].value, arr[i + 1].value
    
    return i + 1
        
        
# helper function to check if array is sorted
def is_sorted(arr : Array) -> bool:
    for i in range(1, len(arr)):
        if int(arr[i]) < int(arr[i-1]):
            return False
    return True


# list of algorithms to test
algorithms = [
    ("right", quicksort_r),
    ("left", quicksort_l),
    ("median", quicksort_m),
]

def main() -> None:
    
    # instance of AlgoContext to track comparisons and additions
    ctx = AlgoContext()
    
    # array to store results for each algorithm and sequence
    results = [[] for _ in range(3)]
    
    # execute algorithm for each sequence file
    for i in range(4):
        
        filename = f"AlgoDatSoSe26/data/seq{i}.txt"
        
        # read in sequence from file
        with open(filename, 'r') as f:
            sequence = [int(line.strip()) for line in f]
        
        # execute each variant of quicksort and save results
        for variant in range(3):
            
            # reset AlgoContext
            ctx.reset()
            arr = Array(sequence, ctx)
            
            # get start time
            start_time = time.time()
            
            # execute quicksort with pivot variant
            sorted_arr = algorithms[variant][1](arr, 0, len(arr) - 1, ctx)
            
            # get end time
            end_time = time.time()
            
            # save results
            results[variant].append(
                (f"seq{i}",
                f"{len(sequence)}",
                f"{algorithms[variant][0]}",
                f"{ctx.comparisons}",
                f"{is_sorted(sorted_arr)}",
                f"{((end_time - start_time)*1000):.4f} ms"))

    # print results in tabular format
    for result in results:
        
        print("\nQuick sort with {} pivot selection:".format(result[0][2]))
        
        print("{:>10} {:>10} {:>15} {:>10} {:>15}".format("Sequence", "Size","Comparisons", "Sorted", "Duration"))
        for seq, siz, piv, comp, sort, dur in result:
            print("{:>10} {:>10} {:>15} {:>10} {:>15}".format(seq, siz, comp, sort, dur))

        
if __name__ == "__main__":
    main()
