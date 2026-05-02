"""
Daniel Baer
02.05.2026

mINF4/1, V03, "Priority Queue"

prio_queue.py

This application implements a priority queue using a heap data structure.
"""

class priority_queue:
    def __init__(self, arr):
        self.arr = arr
        self.size = len(arr)

    def insert(self, priority):
        self.arr.append(priority)
        self.size += 1
        self._sift_up(self.size - 1)
    
    def pop(self):
        if self.size == 0:
            raise IndexError("Priority Queue is empty")
        top = self.arr[0]
        self.arr[0] = self.arr[-1]
        self.arr.pop()
        self.size -= 1
        self._sift_down(0)
        return top
    
    def peek(self):
        if self.size == 0:
            raise IndexError("Priority Queue is empty")
        return self.arr[0]
    
    def is_empty(self):
        return self.size == 0
    
    def _sift_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.arr[index] > self.arr[parent]:
            self.arr[index], self.arr[parent] = self.arr[parent], self.arr[index]
            self._sift_up(parent)
            
    def _sift_down(self, index):
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2
        
        if left < self.size and self.arr[left] > self.arr[largest]:
            largest = left
        if right < self.size and self.arr[right] > self.arr[largest]:
            largest = right
        if largest != index:
            self.arr[index], self.arr[largest] = self.arr[largest], self.arr[index]
            self._sift_down(largest)
