"""
Daniel Baer
02.05.2026

mINF4/1, V03, "Priority Queue"

prio_queue.py

This implements a priority queue class using a heap data structure.
"""

# priority queue implementation
class priority_queue:

    # Initialize the priority queue with an array
    def __init__(self, arr):
        self.arr = arr
        self.size = len(arr)

    # Insert a new priority into the priority queue
    def insert(self, priority):
        # Add the new priority to the end of the array and increase the size
        self.arr.append(priority)
        self.size += 1

        # Maintain the heap property by sifting up the newly added element
        self._sift_up(self.size - 1)
    
    # Remove and return the highest priority element from the priority queue
    def pop(self):
        # If the priority queue is empty, raise an exception
        if self.is_empty():
            raise IndexError("Priority Queue is empty")
        
        # Store the top element to return later, replace it with the last element, and decrease the size
        top = self.arr[0]
        self.arr[0] = self.arr[-1]
        self.arr.pop()
        self.size -= 1
        self._sift_down(0)

        return top
    
    # Return the highest priority element without removing it
    def peek(self):
        if self.is_empty():
            # If the priority queue is empty, raise an exception
            raise IndexError("Priority Queue is empty")
        
        return self.arr[0]
    
    # Check if the priority queue is empty
    def is_empty(self):
        return self.size == 0
    
    # Helper function to maintain the heap property after inserting a new element
    def _sift_up(self, index):
        # Calculate the parent index of the current index
        parent = (index - 1) // 2

        # If index is greater than 0 and current element is greater than its parent,
        # swap and continue sifting up
        if index > 0 and self.arr[index] > self.arr[parent]:
            self.arr[index], self.arr[parent] = self.arr[parent], self.arr[index]
            self._sift_up(parent)
    
    # Helper function to maintain the heap property after removing the top element
    def _sift_down(self, index):
        # Initialize the largest element as the current index
        largest = index

        # Calculate left and right child indices
        left = 2 * index + 1
        right = 2 * index + 2
        
        # If the left child is larger than the current largest, update largest
        if left < self.size and self.arr[left] > self.arr[largest]:
            largest = left

        # If the right child is larger than the current largest, update largest
        if right < self.size and self.arr[right] > self.arr[largest]:
            largest = right

        # If the largest element is not the current index, swap and continue sifting down
        if largest != index:
            # Swap the current element with the largest element and continue sifting down
            self.arr[index], self.arr[largest] = self.arr[largest], self.arr[index]
            self._sift_down(largest)
