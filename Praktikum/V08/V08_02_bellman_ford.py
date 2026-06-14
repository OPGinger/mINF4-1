"""Minimal Bellman-Ford solution for Praktikum V08 Aufgabe 2."""

import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
PRAKTIKUM_DIR = TASK_DIR.parent
ALGODAT_DIR = PRAKTIKUM_DIR / "AlgoDatSoSe26"

sys.path.insert(0, str(ALGODAT_DIR))

from vorlesung.L08_graphen.graph import AdjacencyListGraph


def bellman_ford(graph, start_name: str):
    """Return (distance_map, predecessor_map, has_negative_cycle)."""
    vertices = graph.all_vertices()
    distance_map = {vertex: float("inf") for vertex in vertices}
    predecessor_map = {vertex: None for vertex in vertices}

    start_vertex = graph.get_vertex(start_name)
    distance_map[start_vertex] = 0

    # Relax all edges at most |V|-1 times.
    for _ in range(len(vertices) - 1):
        changed = False
        for src_name, dest_name, weight in graph.all_edges():
            src_vertex = graph.get_vertex(src_name)
            dest_vertex = graph.get_vertex(dest_name)

            if distance_map[src_vertex] == float("inf"):
                continue

            candidate = distance_map[src_vertex] + weight
            if candidate < distance_map[dest_vertex]:
                distance_map[dest_vertex] = candidate
                predecessor_map[dest_vertex] = src_vertex
                changed = True

        if not changed:
            break

    # One extra pass detects a reachable negative cycle.
    has_negative_cycle = False
    for src_name, dest_name, weight in graph.all_edges():
        src_vertex = graph.get_vertex(src_name)
        dest_vertex = graph.get_vertex(dest_name)

        if distance_map[src_vertex] == float("inf"):
            continue

        if distance_map[src_vertex] + weight < distance_map[dest_vertex]:
            has_negative_cycle = True
            break

    return distance_map, predecessor_map, has_negative_cycle


def build_graph():
    """Build the graph from the assignment table."""
    graph = AdjacencyListGraph()
    for name in ["a", "b", "c", "d", "e"]:
        graph.insert_vertex(name)

    graph.connect("a", "b", 9)
    graph.connect("a", "d", 4)
    graph.connect("b", "c", 1)
    graph.connect("b", "d", 2)
    graph.connect("c", "b", 5)
    graph.connect("c", "e", 4)
    graph.connect("d", "c", -2)
    graph.connect("d", "e", 2)
    return graph


def reconstruct_path(graph, predecessor_map, start_name: str, destination_name: str) -> list[str]:
    """Reconstruct one shortest path start -> destination from predecessor_map."""
    destination_vertex = graph.get_vertex(destination_name)
    start_vertex = graph.get_vertex(start_name)

    path = []
    current = destination_vertex
    while current is not None:
        path.insert(0, current.value)
        if current == start_vertex:
            return path
        current = predecessor_map[current]

    return []


def main() -> None:
    graph = build_graph()

    distance_map, predecessor_map, has_negative_cycle = bellman_ford(graph, "a")
    
    for vertex in sorted(graph.all_vertices(), key=lambda item: item.value):
        distance = distance_map[vertex]
        distance_text = "inf" if distance == float("inf") else str(int(distance))
        path = reconstruct_path(graph, predecessor_map, "a", vertex.value)
        path_text = " -> ".join(path) if path else "unreachable"
        print(f"- {vertex.value}: distance={distance_text}, path={path_text}")
    print(f"- has_negative_cycle={has_negative_cycle}")

    # Add e -> b with weight -8 and run again.
    print("\nAdd edge e -> b with weight -8")
    graph.connect("e", "b", -8)
    _, _, has_negative_cycle_after = bellman_ford(graph, "a")
    print(f"- has_negative_cycle={has_negative_cycle_after}")


if __name__ == "__main__":
    main()
