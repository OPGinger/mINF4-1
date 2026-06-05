"""
Daniel Baer
05.06.2026

mINF4/1, V07, Task 2 "Tiefensuche und topologisches Sortieren"

V07_02_DFS_TopSort.py

This script models module dependencies as a directed acyclic graph,
executes DFS, and derives a build order from finish times.
"""

import sys
from pathlib import Path

# Build import paths so this script can be started from different working directories.
TASK_DIR = Path(__file__).resolve().parent
PRAKTIKUM_DIR = TASK_DIR.parent
ROOT_DIR = PRAKTIKUM_DIR.parent
ALGODAT_DIR = ROOT_DIR / "AlgoDatSoSe26"

sys.path.insert(0, str(ALGODAT_DIR))

from vorlesung.L08_graphen.graph import AdjacencyListGraph


def build_dependency_graph() -> tuple[AdjacencyListGraph, list[tuple[str, str]]]:
    """
    Create the dependency graph.

    Edge semantics according to assignment:
    A -> B means: A depends on B (B must be built before A).
    """
    graph = AdjacencyListGraph()

    modules = ["main", "parser", "codegen", "optimizer", "ast", "lexer", "utils"]
    for module in modules:
        graph.insert_vertex(module)

    # (module, dependency)
    dependencies = [
        ("main", "parser"),
        ("main", "codegen"),
        ("parser", "lexer"),
        ("parser", "ast"),
        ("codegen", "ast"),
        ("codegen", "optimizer"),
        ("optimizer", "utils"),
        ("ast", "utils"),
    ]

    for module, dependency in dependencies:
        graph.connect(module, dependency)

    return graph, dependencies


def dfs_fallback(graph: AdjacencyListGraph) -> tuple[dict, dict, dict]:
    """
    Local DFS fallback with enter/leave timestamps.
    This is only used if the library DFS raises due an internal bug.
    """
    enter_map = {}
    leave_map = {}
    predecessor_map = {}
    color_map = {}
    time_counter = 0

    for vertex in graph.all_vertices():
        color_map[vertex] = "WHITE"
        predecessor_map[vertex] = None

    def dfs_visit(vertex):
        nonlocal time_counter
        color_map[vertex] = "GRAY"
        time_counter += 1
        enter_map[vertex] = time_counter

        for dest in graph.get_adjacent_vertices(vertex.value):
            if color_map[dest] == "WHITE":
                predecessor_map[dest] = vertex
                dfs_visit(dest)

        color_map[vertex] = "BLACK"
        time_counter += 1
        leave_map[vertex] = time_counter

    for vertex in graph.all_vertices():
        if color_map[vertex] == "WHITE":
            dfs_visit(vertex)

    return enter_map, leave_map, predecessor_map


def build_order_from_leave_times(leave_map: dict) -> list[str]:
    """Sort nodes by descending leave-time and return a candidate build order."""
    sorted_vertices = sorted(leave_map.keys(), key=lambda vertex: leave_map[vertex], reverse=True)
    return [vertex.value for vertex in sorted_vertices]


def verify_build_order(build_order: list[str], dependencies: list[tuple[str, str]]) -> tuple[bool, list[str]]:
    """
    Check all dependency constraints.

    For every edge A -> B (A depends on B), B must appear before A in build_order.
    """
    index_map = {name: idx for idx, name in enumerate(build_order)}
    violations = []

    for module, dependency in dependencies:
        if index_map[dependency] > index_map[module]:
            violations.append(
                f"Verletzung: {module} haengt von {dependency} ab, "
                f"aber {dependency} kommt nach {module}."
            )

    return len(violations) == 0, violations


def print_time_marks(enter_map: dict, leave_map: dict) -> None:
    """Print enter/leave timestamps for each module in tabular form."""
    print("{:>12} {:>10} {:>10}".format("Modul", "enter", "leave"))

    # Sort alphabetically for reproducible output.
    sorted_vertices = sorted(enter_map.keys(), key=lambda vertex: vertex.value)
    for vertex in sorted_vertices:
        print("{:>12} {:>10} {:>10}".format(vertex.value, enter_map[vertex], leave_map[vertex]))


def main() -> None:
    print("Aufgabe 2: Tiefensuche und topologisches Sortieren")
    print("=" * 60)

    # a) Build directed acyclic dependency graph
    graph, dependencies = build_dependency_graph()
    v_count = len(graph.all_vertices())
    e_count = len(graph.all_edges())

    print("a) Graphaufbau")
    print("- Knoten (Module):", ", ".join(sorted([vertex.value for vertex in graph.all_vertices()])))
    print("- Kanten (A -> B bedeutet: A haengt von B ab):")
    for module, dependency in dependencies:
        print(f"  {module} -> {dependency}")
    print()

    # b) Execute DFS and show timestamps
    print("b) DFS mit Zeitmarken")
    try:
        # Required by assignment: use dfs() from graph module.
        enter_map, leave_map, _ = graph.dfs()
    except KeyError as err:
        # Known issue in current library DFS for this repository state.
        print(f"- Hinweis: graph.dfs() wirft aktuell einen Fehler ({err}).")
        print("- Es wird eine lokale DFS-Fallback-Implementierung verwendet.")
        enter_map, leave_map, _ = dfs_fallback(graph)
    print_time_marks(enter_map, leave_map)
    print()

    # c) Topological sorting by descending finish times and dependency check
    print("c) Topologische Sortierung")
    topo_order = build_order_from_leave_times(leave_map)
    print("- Reihenfolge nach absteigender Endzeit:")
    print("  " + " -> ".join(topo_order))

    valid, violations = verify_build_order(topo_order, dependencies)
    if valid:
        print("- Pruefung: Alle Abhaengigkeiten werden eingehalten.")
    else:
        print("- Pruefung: Abhaengigkeiten verletzt in dieser Reihenfolge:")
        for violation in violations:
            print(f"  {violation}")

        # Show corrected build order if needed.
        corrected_order = list(reversed(topo_order))
        corrected_valid, _ = verify_build_order(corrected_order, dependencies)
        if corrected_valid:
            print("- Korrigierte Build-Reihenfolge (inverse Reihenfolge):")
            print("  " + " -> ".join(corrected_order))
    print()

    # d) Complexity discussion on this concrete graph
    print("d) Komplexitaet O(|V| + |E|)")
    print(f"- Anzahl Knoten |V| = {v_count}")
    print(f"- Anzahl Kanten |E| = {e_count}")
    print("- Jeder Knoten wird in DFS genau einmal von WHITE nach GRAY nach BLACK gefaerbt.")
    print("- Jede gerichtete Kante wird genau einmal betrachtet, wenn ihr Startknoten expandiert wird.")
    print("- Daher ist die Laufzeit linear in der Summe aus Knoten und Kanten.")


if __name__ == "__main__":
    main()
