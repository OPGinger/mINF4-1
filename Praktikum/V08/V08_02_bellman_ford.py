"""
Daniel Baer
14.06.2026

mINF4/1, V08, Aufgabe 2 "Bellman-Ford"

V08_02_bellman_ford.py

Implementiert Bellman-Ford analog zu dijkstra() fuer die Graph-Klasse aus der Vorlesung,
inklusive Erkennung negativer Zyklen.
"""

import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
PRAKTIKUM_DIR = TASK_DIR.parent
ALGODAT_DIR = PRAKTIKUM_DIR / "AlgoDatSoSe26"

sys.path.insert(0, str(ALGODAT_DIR))

from vorlesung.L08_graphen.graph import AdjacencyListGraph


def bellman_ford(graph, start_name: str):
    """
    Berechnet kuerzeste Wege mit Bellman-Ford.

    Rueckgabe:
    (distance_map, predecessor_map, has_negative_cycle)
    """
    vertices = graph.all_vertices()
    distance_map = {vertex: float("inf") for vertex in vertices}
    predecessor_map = {vertex: None for vertex in vertices}

    start_vertex = graph.get_vertex(start_name)
    distance_map[start_vertex] = 0

    vertex_count = len(vertices)

    for _ in range(vertex_count - 1):
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


def build_lecture_graph() -> AdjacencyListGraph:
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


def reconstruct_path(graph, predecessor_map, destination_name: str) -> list[str]:
    destination_vertex = graph.get_vertex(destination_name)

    if predecessor_map[destination_vertex] is None and destination_name != "a":
        return [destination_name]

    path = []
    current = destination_vertex
    while current is not None:
        path.insert(0, current.value)
        current = predecessor_map[current]

    return path


def append_to_answer_file(section_text: str) -> None:
    answer_path = TASK_DIR / "V08_Antworten.txt"

    if answer_path.exists():
        old_text = answer_path.read_text(encoding="utf-8")
    else:
        old_text = "Praktikum 8 - Kuerzeste Wege\n"

    if not old_text.endswith("\n"):
        old_text += "\n"

    answer_path.write_text(old_text + "\n" + section_text + "\n", encoding="utf-8")


def main() -> None:
    print("Aufgabe 2: Bellman-Ford")
    print("=" * 60)

    graph = build_lecture_graph()

    print("a) Implementierung")
    print("- bellman_ford(graph, start_name) nutzt |V|-1 Relaxationsrunden und eine Pruefrunde.")
    print()

    print("b) Test auf Vorlesungsgraph (Start a)")
    distance_map, predecessor_map, has_negative_cycle = bellman_ford(graph, "a")

    vertices_sorted = sorted(graph.all_vertices(), key=lambda vertex: vertex.value)

    table_lines = []
    for vertex in vertices_sorted:
        distance = distance_map[vertex]
        path = reconstruct_path(graph, predecessor_map, vertex.value)
        path_text = " -> ".join(path)
        distance_text = "inf" if distance == float("inf") else str(int(distance))

        table_lines.append(
            f"- {vertex.value}: Distanz={distance_text}, Pfad={path_text}"
        )

    for line in table_lines:
        print(line)

    print(f"- has_negative_cycle: {has_negative_cycle}")
    print()

    print("c) Negativer Zyklus")
    graph.connect("e", "b", -8)
    _, _, has_negative_cycle_2 = bellman_ford(graph, "a")

    print("- Zusatzkante: e -> b mit Gewicht -8")
    print(f"- has_negative_cycle: {has_negative_cycle_2}")
    print("- Erkannter Zyklus: b -> d -> e -> b")
    print("- Zyklusgewicht: 2 + 2 + (-8) = -4")
    print("- Erkennung durch abschliessende Pruefrunde: weitere Relaxation ist moeglich.")
    print()

    print("d) Komplexitaet")
    print("- Bellman-Ford: O(|V|*|E|)")
    print("- Dijkstra (Min-Heap): O(|V| log |V| + |E|)")
    print("- Dijkstra ist vorzuziehen ohne negative Kanten (in der Regel schneller).")
    print("- Bellman-Ford muss genutzt werden bei negativen Kanten oder wenn")
    print("  negative Zyklen erkannt werden sollen.")

    section_lines = [
        "Aufgabe 2: Bellman-Ford",
        "",
        "a) Implementierung",
        "- bellman_ford(graph, start_name) mit |V|-1 Relaxationsrunden und Pruefrunde.",
        "",
        "b) Test auf Vorlesungsgraph (Start a)",
    ]
    section_lines.extend(table_lines)
    section_lines.append(f"- has_negative_cycle: {has_negative_cycle}")
    section_lines.append("")
    section_lines.append("c) Negativer Zyklus")
    section_lines.append("- Zusatzkante: e -> b mit Gewicht -8")
    section_lines.append(f"- has_negative_cycle: {has_negative_cycle_2}")
    section_lines.append("- Betroffener Zyklus: b -> d -> e -> b")
    section_lines.append("- Zyklusgewicht: -4")
    section_lines.append("")
    section_lines.append("d) Komplexitaet")
    section_lines.append("- Bellman-Ford: O(|V|*|E|)")
    section_lines.append("- Dijkstra (Min-Heap): O(|V| log |V| + |E|)")
    section_lines.append("- Dijkstra bei nicht-negativen Kanten, Bellman-Ford bei negativen Kanten/Zyklenpruefung.")

    append_to_answer_file("\n".join(section_lines))
    print()
    print("Aufgabe-2-Ergebnisse wurden in V08_Antworten.txt ergaenzt.")


if __name__ == "__main__":
    main()
