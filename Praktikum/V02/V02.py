"""
Daniel Baer
25.04.2026

mINF4/1, V02, "Merge Sort"

V02.py


This application implements the Merge Sort algorithm to sort an array of integers.
The algorithm recursively divides the array into halves until it reaches arrays of size one, which are inherently sorted.
Then, it merges the sorted halves back together in a way that results in a fully sorted array. 
"""

# import necessary modules and classes
from math import floor, ceil, log2
import sys
import time

# add path of AlgoDatSoSe26 directory
sys.path.insert(0, 'AlgoDatSoSe26')

# import classes from utils module
from utils.algo_context import AlgoContext
from utils.algo_array import Array
from utils.algo_int import Int


# function to perform merge sort on array
def merge_sort(A: Array, ac: AlgoContext):
    
    # exit condition for recursion: if array has 1 or less elements, it is already sorted
    if len(A) <= 1:
        return A
    
    # find the midpoint of the array
    mid = floor(len(A) / 2)
    
    # create left and right subarrays
    left = Array([A[i] for i in range(mid)], ac)
    right = Array([A[i] for i in range(mid, len(A))], ac)
    
    # recursively sort the left and right subarrays
    merge_sort(left, ac)
    merge_sort(right, ac)
    
    # merge the sorted subarrays back into A
    return merge(A, left, right, ac)


    
def merge(A: Array, left: Array, right: Array, ctx: AlgoContext):
    
    # initialize pointers for left, right and merged array
    i = j = k = 0
    
    # merge elements from left and right arrays in sorted order
    while i < len(left) and j < len(right):
        
        if left[i] <= right[j]:
            # move through left array
            A[k] = left[i]
            i += 1
        else:
            # move through right array
            A[k] = right[j]
            j += 1
            
        # increment pointer for merged array
        k += 1
        
    # add remaining elements from left array to merged array
    while i < len(left):
        A[k] = left[i]
        i += 1
        k += 1
        
    # add remaining elements from right array to merged array
    while j < len(right):
        A[k] = right[j]
        j += 1
        k += 1
    
    return A
        
# helper function to check if array is sorted
def is_sorted(arr):
    for i in range(1, len(arr)):
        if int(arr[i]) < int(arr[i-1]):
            return False
    return True


def main() -> None:
    
    # instance of AlgoContext to track comparisons and additions
    ac = AlgoContext()
    
    # execute algorithm for each sequence file
    for i in range(4):

        count_add = 0
        
        filename = f"AlgoDatSoSe26/data/seq{i}.txt"
        
        # read in sequence from file
        with open(filename, 'r') as f:
            sequence = [int(line.strip()) for line in f]
            
        # reset AlgoContext for each new sequence
        ac.reset()
        arr = Array(sequence, ac)
        
        # execute algorithm and measure time
        start_time = time.time()
        
        sorted_arr = merge_sort(arr, ac)
        
        end_time = time.time()
        
        # print results
        print(f"seq{i} ({len(sequence)} elements):")
        print(f"Comparisons: {ac.comparisons}, {ceil(len(sequence)*log2(len(sequence))-len(sequence)-1)} (max)")
        print(f"Sorted correctly: {is_sorted(sorted_arr)}")
        print(f"Duration: {((end_time - start_time)*1000):.6f} ms")
        print(f"Array: {sorted_arr}\n")
        
if __name__ == "__main__":
    main()