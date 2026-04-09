import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.entry_finder = {}  # map: item -> [priority, item]
        self.REMOVED = '<removed>'
        self.counter = 0  # unique sequence count to break ties

    def add_or_update(self, item, priority):
        if item in self.entry_finder:
            self.remove(item)
        count = self.counter
        entry = [priority, count, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.heap, entry)
        self.counter += 1

    def remove(self, item):
        entry = self.entry_finder.pop(item)
        entry[-1] = self.REMOVED  # mark as removed

    def pop(self):
        while self.heap:
            priority, count, item = heapq.heappop(self.heap)
            if item != self.REMOVED:
                del self.entry_finder[item]
                return item, priority
        return None

if __name__ == "__main__":
    pq = PriorityQueue()
    pq.add_or_update('task1', 1)
    pq.add_or_update('task2', float('inf'))
    pq.add_or_update('task3', float('inf'))

    print(pq.pop())  # Should print ('task1', 1)
    pq.add_or_update('task2', 0)  # Update priority of 'task2'
    print(pq.pop())  # Should print ('task2', 0)
    print(pq.pop())  # Should print ('task3', 3)