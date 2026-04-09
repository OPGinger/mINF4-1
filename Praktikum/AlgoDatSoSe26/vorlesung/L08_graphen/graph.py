from collections import deque
from typing import List
from enum import Enum
import graphviz
import math
import heapq
from datetime import datetime
from utils.algo_path import path
from utils.algo_priority_queue import PriorityQueue
from vorlesung.L09_mst.disjoint import DisjointValue


class NodeColor(Enum):
    """Enumeration for node colors in a graph traversal."""
    WHITE = 1       # WHITE: not visited
    GRAY = 2        # GRAY: visited but not all neighbors visited
    BLACK = 3       # BLACK: visited and all neighbors visited


class Vertex:
    """A vertex in a graph."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"Vertex({self.value})"



class Graph:
    """A graph."""
    def insert_vertex(self, name: str):
        raise NotImplementedError("Please implement this method in subclass")

    def connect(self, name1: str, name2: str, weight: float = 1):
        raise NotImplementedError("Please implement this method in subclass")

    def all_vertices(self) -> List[Vertex]:
        raise NotImplementedError("Please implement this method in subclass")

    def get_vertex(self, name: str) -> Vertex:
        raise NotImplementedError("Please implement this method in subclass")

    def get_adjacent_vertices(self, name: str) -> List[Vertex]:
        raise NotImplementedError("Please implement this method in subclass")

    def get_adjacent_vertices_with_weight(self, name: str) -> List[tuple[Vertex, float]]:
        raise NotImplementedError("Please implement this method in subclass")

    def all_edges(self) -> List[tuple[str, str, float]]:
        raise NotImplementedError("Please implement this method in subclass")

    def bfs(self, start_name: str):
        """
        Perform a breadth-first search starting at the given vertex.
        :param start_name: the name of the vertex to start at
        :return: a tuple of two dictionaries, the first mapping vertices to distances from the start vertex,
                 the second mapping vertices to their predecessors in the traversal tree
        """

        color_map = {}                  # maps vertices to their color
        distance_map = {}               # maps vertices to their distance from the start vertex
        predecessor_map = {}            # maps vertices to their predecessor in the traversal tree

        # Initialize the maps
        for vertex in self.all_vertices():
            color_map[vertex] = NodeColor.WHITE
            distance_map[vertex] = None
            predecessor_map[vertex] = None

        # Start at the given vertex
        start_node = self.get_vertex(start_name)
        color_map[start_node] = NodeColor.GRAY
        distance_map[start_node] = 0

        # Initialize the queue with the start vertex
        queue = deque()
        queue.append(start_node)

        # Process the queue
        while len(queue) > 0:
            vertex = queue.popleft()
            for dest in self.get_adjacent_vertices(vertex.value):
                if color_map[dest] == NodeColor.WHITE:
                    color_map[dest] = NodeColor.GRAY
                    distance_map[dest] = distance_map[vertex] + 1
                    predecessor_map[dest] = vertex
                    queue.append(dest)
            color_map[vertex] = NodeColor.BLACK

        # Return the distance and predecessor maps
        return distance_map, predecessor_map

    def dfs(self):
        """
        Perform a depth-first search starting at the first vertex.
        :return: a tuple of two dictionaries, the first mapping vertices to distances from the start vertex,
                 the second mapping vertices to their predecessors in the traversal tree
        """
        color_map : dict[Vertex, NodeColor]= {}
        enter_map : dict[Vertex, int] = {}
        leave_map : dict[Vertex, int] = {}
        predecessor_map : dict[Vertex, Vertex | None] = {}
        white_vertices = set(self.all_vertices())
        time_counter = 0

        def dfs_visit(vertex):
            nonlocal time_counter
            color_map[vertex] = NodeColor.GRAY
            white_vertices.remove(vertex)
            time_counter += 1
            enter_map[vertex] = time_counter
            for dest in self.get_adjacent_vertices(vertex.value):
                if color_map[dest] == NodeColor.WHITE:
                    predecessor_map[dest] = vertex
                    dfs_visit(dest)
            color_map[vertex] = NodeColor.BLACK
            time_counter += 1
            leave_map[vertex] = time_counter

        # Initialize the maps
        for vertex in self.all_vertices():
            color_map[vertex] = NodeColor.WHITE
            predecessor_map[vertex] = None

        while white_vertices:
            v = white_vertices.pop()
            dfs_visit(v)

        return enter_map, leave_map, predecessor_map


    def path(self, destination, map):
        """
        Compute the path from the start vertex to the given destination vertex.
        The map parameter is the predecessor map
        """
        path = []
        destination_node = self.get_vertex(destination)
        while destination_node is not None:
            path.insert(0, destination_node.value)
            destination_node = map[destination_node]
        return path

    def graph(self, filename: str = "Graph"):
        dot = graphviz.Digraph( name=filename,
                                node_attr={"fontname": "Arial"},
                                format="pdf" )
        for vertex in self.all_vertices():
            dot.node(str(id(vertex)), label=str(vertex.value))
        for edge in self.all_edges():
            dot.edge(str(id(self.get_vertex(edge[0]))), str(id(self.get_vertex(edge[1]))), label=str(edge[2]))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename}_{timestamp}.gv"
        filename = path(filename)
        dot.render(filename)

    def dijkstra(self, start_name: str) -> tuple[dict[Vertex, float], dict[Vertex, Vertex | None]]:
        """
        Führt den Dijkstra-Algorithmus für kürzeste Pfade durch, implementiert mit Knotenfarben.

        Args:
            start_name: Name des Startknotens

        Returns:
            Ein Tupel aus zwei Dictionaries:
            - distance_map: Abbildung von Knoten auf ihre kürzeste Distanz vom Startknoten
            - predecessor_map: Abbildung von Knoten auf ihre Vorgänger im kürzesten Pfad
        """

        def relax(vertex, dest, weight):
            """
            Entspannt die Kante zwischen vertex und dest.
            Aktualisiert die Distanz und den Vorgänger, wenn ein kürzerer Pfad gefunden wird.
            """
            if distance_map[vertex] + weight < distance_map[dest]:
                distance_map[dest] = distance_map[vertex] + weight
                predecessor_map[dest] = vertex
                queue.add_or_update(dest, distance_map[dest])

        # Initialisierung der Maps
        distance_map = {}  # Speichert kürzeste Distanzen
        predecessor_map = {}  # Speichert Vorgänger

        # Initialisiere alle Knoten
        queue = PriorityQueue()
        for vertex in self.all_vertices():
            distance_map[vertex] = float('inf')  # Initiale Distanz unendlich
            predecessor_map[vertex] = None  # Initialer Vorgänger None
            queue.add_or_update(vertex, distance_map[vertex])  # Füge Knoten zur Prioritätswarteschlange hinzu



        # Setze Startknoten
        start_node = self.get_vertex(start_name)
        distance_map[start_node] = 0
        queue.add_or_update(start_node, distance_map[start_node])

        while True:
            entry = queue.pop()
            if entry is None:
                break
            vertex = entry[0]
            for dest, weight in self.get_adjacent_vertices_with_weight(vertex.value):
                relax(vertex, dest, weight)
        return distance_map, predecessor_map

    def mst_prim(self, start_name: str = None):
        """ Compute the minimum spanning tree of the graph using Prim's algorithm. """

        distance_map = {}   # maps vertices to their current distance from the spanning tree
        parent_map = {}     # maps vertices to their predecessor in the spanning tree

        Vertex.__lt__ = lambda self, other: distance_map[self] < distance_map[other]

        queue = []

        if start_name is None:
            start_name = self.all_vertices()[0].value

        # Initialize the maps
        for vertex in self.all_vertices():
            distance_map[vertex] = 0 if vertex.value == start_name else math.inf
            parent_map[vertex] = None
            queue.append(vertex)

        heapq.heapify(queue)    # Convert the list into a heap

        # Process the queue
        cost = 0 # The cost of the minimum spanning tree
        while len(queue) > 0:
            vertex = heapq.heappop(queue)
            cost += distance_map[vertex] # Add the cost of the edge to the minimum spanning tree
            for (dest, w) in self.get_adjacent_vertices_with_weight(vertex.value):
                if dest in queue and distance_map[dest] > w:
                    # Update the distance and parent maps
                    queue.remove(dest)
                    distance_map[dest] = w
                    parent_map[dest] = vertex
                    queue.append(dest)      # Add the vertex back to the queue
                    heapq.heapify(queue)    # Re-heapify the queue

        # Return the distance and predecessor maps
        return parent_map, cost

    def mst_kruskal(self, start_name: str = None):
        """ Compute the minimum spanning tree of the graph using Kruskal's algorithm. """

        cost = 0
        result = []
        edges = self.all_edges()

        # Create a disjoint set for each vertex
        vertex_map = {v.value: DisjointValue(v) for v in self.all_vertices()}

        # Sort the edges by weight
        edges.sort(key=lambda edge: edge[2])

        # Process the edges
        for edge in edges:
            start_name, end_name, weight = edge
            # Check if the edge creates a cycle
            if not vertex_map[start_name].same_set(vertex_map[end_name]):
                result.append(edge)
                vertex_map[start_name].union(vertex_map[end_name])
                cost += weight

        return result, cost


class AdjacencyListGraph(Graph):
    """A graph implemented as an adjacency list."""
    def __init__(self):
        self.adjacency_map = {}     # maps vertex names to lists of adjacent vertices
        self.vertex_map = {}        # maps vertex names to vertices

    def insert_vertex(self, name: str):
        if name not in self.vertex_map:
            self.vertex_map[name] = Vertex(name)
        if name not in self.adjacency_map:
            self.adjacency_map[name] = []

    def connect(self, name1: str, name2: str, weight: float = 1):
        adjacency_list = self.adjacency_map[name1]
        dest = self.vertex_map[name2]
        adjacency_list.append((dest, weight))

    def all_vertices(self) -> List[Vertex]:
        return list(self.vertex_map.values())

    def get_vertex(self, name: str) -> Vertex:
        return self.vertex_map[name]

    def get_adjacent_vertices(self, name: str) -> List[Vertex]:
        return list(map(lambda x: x[0], self.adjacency_map[name]))

    def get_adjacent_vertices_with_weight(self, name: str) -> List[tuple[Vertex, float]]:
        return self.adjacency_map[name]

    def all_edges(self) -> List[tuple[str, str, float]]:
        result = []
        for name in self.adjacency_map:
            for (dest, weight) in self.adjacency_map[name]:
                result.append((name, dest.value, weight))
        return result


class AdjacencyMatrixGraph(Graph):
    """A graph implemented as an adjacency matrix."""
    def __init__(self):
        self.index_map = {}         # maps vertex names to indices
        self.vertex_list = []       # list of vertices
        self.adjacency_matrix = []  # adjacency matrix

    def insert_vertex(self, name: str):
        if name not in self.index_map:
            self.index_map[name] = len(self.vertex_list)
            self.vertex_list.append(Vertex(name))
            for row in self.adjacency_matrix:   # add a new column to each row
                row.append(None)
            self.adjacency_matrix.append([None] * len(self.vertex_list)) # add a new row

    def connect(self, name1: str, name2: str, weight: float = 1):
        index1 = self.index_map[name1]
        index2 = self.index_map[name2]
        self.adjacency_matrix[index1][index2] = weight


    def all_vertices(self) -> List[Vertex]:
        return self.vertex_list

    def get_vertex(self, name: str) -> Vertex:
        index = self.index_map[name]
        return self.vertex_list[index]

    def get_adjacent_vertices(self, name: str) -> List[Vertex]:
        index = self.index_map[name]
        result = []
        for i in range(len(self.vertex_list)):
            if self.adjacency_matrix[index][i] is not None:
                name = self.vertex_list[i].value
                result.append(self.get_vertex(name))
        return result

    def get_adjacent_vertices_with_weight(self, name: str) -> List[tuple[Vertex, float]]:
        index = self.index_map[name]
        result = []
        for i in range(len(self.vertex_list)):
            if self.adjacency_matrix[index][i] is not None:
                name = self.vertex_list[i].value
                result.append((self.get_vertex(name), self.adjacency_matrix[index][i]))
        return result

    def all_edges(self) -> List[tuple[str, str, float]]:
        result = []
        for i in range(len(self.vertex_list)):
            for j in range(len(self.vertex_list)):
                if self.adjacency_matrix[i][j] is not None:
                    result.append((self.vertex_list[i].value, self.vertex_list[j].value, self.adjacency_matrix[i][j]))
        return result



