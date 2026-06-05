"""
Daniel Baer
05.06.2026

mINF4/1, V07, Task 1 "Breitensuche auf einer Hoehenkarte"

V07_01_BFS_Hoehenkarte.py

This script models the AoC 2022 Day 12 heightmap as a directed graph,
computes shortest paths with BFS, and evaluates runtime behavior.
"""

import sys
import time
from pathlib import Path

# Build import paths so this script can be started from different working directories.
TASK_DIR = Path(__file__).resolve().parent
PRAKTIKUM_DIR = TASK_DIR.parent
ROOT_DIR = PRAKTIKUM_DIR.parent
ALGODAT_DIR = ROOT_DIR / "AlgoDatSoSe26"

sys.path.insert(0, str(ALGODAT_DIR))

from vorlesung.L08_graphen.graph import AdjacencyListGraph


EXAMPLE_MAP_TEXT = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""


def vertex_name(row: int, col: int) -> str:
    """Create a stable vertex name for one grid cell."""
    return f"{row},{col}"


def parse_vertex_name(name: str) -> tuple[int, int]:
    """Convert a vertex name back to row/column coordinates."""
    row_str, col_str = name.split(",")
    return int(row_str), int(col_str)


def height_of(char: str) -> int:
    """Map a height character to its numeric elevation."""
    if char == "S":
        return ord("a")
    if char == "E":
        return ord("z")
    return ord(char)


def parse_heightmap(lines: list[str]) -> tuple[list[list[str]], tuple[int, int], tuple[int, int]]:
    """Parse a heightmap and return grid, start coordinate, and end coordinate."""
    stripped = [line.strip() for line in lines if line.strip()]
    if not stripped:
        raise ValueError("Die Hoehenkarte ist leer.")

    width = len(stripped[0])
    grid = [list(line) for line in stripped]

    for line in stripped:
        if len(line) != width:
            raise ValueError("Die Hoehenkarte ist nicht rechteckig.")

    start = None
    end = None

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "S":
                if start is not None:
                    raise ValueError("Es wurde mehr als ein Startpunkt S gefunden.")
                start = (row, col)
            elif grid[row][col] == "E":
                if end is not None:
                    raise ValueError("Es wurde mehr als ein Zielpunkt E gefunden.")
                end = (row, col)

    if start is None:
        raise ValueError("Kein Startpunkt S gefunden.")
    if end is None:
        raise ValueError("Kein Zielpunkt E gefunden.")

    return grid, start, end


def build_height_graph(grid: list[list[str]], reverse_edges: bool = False) -> tuple[AdjacencyListGraph, int, int]:
    """
    Build the directed graph for the heightmap.

    reverse_edges=False:
        edge A->B if B is reachable from A under the climbing rule.
    reverse_edges=True:
        reverse every valid forward edge; useful for part d (single BFS from E).
    """
    graph = AdjacencyListGraph()
    rows = len(grid)
    cols = len(grid[0])

    # Insert one graph vertex per map cell.
    for row in range(rows):
        for col in range(cols):
            graph.insert_vertex(vertex_name(row, col))

    edge_count = 0

    # 4-neighborhood (up, down, left, right).
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for row in range(rows):
        for col in range(cols):
            current_height = height_of(grid[row][col])
            current_name = vertex_name(row, col)

            for delta_row, delta_col in directions:
                nr = row + delta_row
                nc = col + delta_col

                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbor_height = height_of(grid[nr][nc])

                    # Forward movement rule: destination may be at most +1 higher.
                    if neighbor_height <= current_height + 1:
                        neighbor_name = vertex_name(nr, nc)
                        if reverse_edges:
                            graph.connect(neighbor_name, current_name)
                        else:
                            graph.connect(current_name, neighbor_name)
                        edge_count += 1

    vertex_count = rows * cols
    return graph, vertex_count, edge_count


def shortest_path_s_to_e(lines: list[str]) -> tuple[list[str], int | None, int, int]:
    """Run BFS from S to E and return path, distance, |V|, and |E|."""
    grid, start, end = parse_heightmap(lines)
    graph, vertex_count, edge_count = build_height_graph(grid, reverse_edges=False)

    start_name = vertex_name(start[0], start[1])
    end_name = vertex_name(end[0], end[1])

    distance_map, predecessor_map = graph.bfs(start_name)
    end_vertex = graph.get_vertex(end_name)
    distance = distance_map[end_vertex]

    if distance is None:
        return [], None, vertex_count, edge_count

    path_nodes = graph.path(end_name, predecessor_map)
    return path_nodes, distance, vertex_count, edge_count


def shortest_path_any_a_to_e(lines: list[str]) -> tuple[int | None, tuple[int, int] | None]:
    """
    Optional part d:
    Reduce the multi-source problem to one BFS by reversing all valid edges,
    then run BFS once from E and take the best distance among all 'a' (and S) cells.
    """
    grid, start, end = parse_heightmap(lines)
    graph, _, _ = build_height_graph(grid, reverse_edges=True)

    end_name = vertex_name(end[0], end[1])
    distance_map, _ = graph.bfs(end_name)

    best_distance = None
    best_position = None

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            # 'S' has elevation 'a', therefore include both.
            if height_of(grid[row][col]) == ord("a"):
                node = graph.get_vertex(vertex_name(row, col))
                dist = distance_map[node]
                if dist is not None and (best_distance is None or dist < best_distance):
                    best_distance = dist
                    best_position = (row, col)

    return best_distance, best_position


def average_bfs_runtime(lines: list[str], repeats: int = 30) -> tuple[float, int, int]:
    """Measure average BFS runtime (milliseconds), and return runtime with |V|, |E|."""
    grid, start, _ = parse_heightmap(lines)
    graph, vertex_count, edge_count = build_height_graph(grid, reverse_edges=False)

    start_name = vertex_name(start[0], start[1])

    start_time = time.perf_counter()
    for _ in range(repeats):
        graph.bfs(start_name)
    end_time = time.perf_counter()

    avg_ms = ((end_time - start_time) / repeats) * 1000
    return avg_ms, vertex_count, edge_count


def print_path_coordinates(path_nodes: list[str]) -> str:
    """Format the path as coordinate sequence for readable output."""
    coords = [parse_vertex_name(name) for name in path_nodes]
    return " -> ".join([f"({row},{col})" for row, col in coords])


def load_map_from_file(file_path: Path) -> list[str]:
    """Load a map text file and return all lines."""
    with file_path.open("r", encoding="utf-8") as file:
        return file.readlines()


def main() -> None:
    print("Aufgabe 1: Breitensuche auf einer Hoehenkarte")
    print("=" * 60)

    # a) Modeling rationale
    print("a) Modellierung")
    print("- Knoten: jedes Feld (Zeile, Spalte)")
    print("- Kante A->B: B ist Nachbar von A und Hoehenregel ist erfuellt")
    print("- Wahl: Adjazenzliste statt Adjazenzmatrix")
    print("  Grund: Das Gitter ist ein duenn besetzter Graph (max. 4 Ausgaenge pro Knoten),")
    print("  daher ist der Speicherbedarf mit Liste deutlich geringer als O(|V|^2).")
    print()

    # b) BFS on example map
    print("b) Kuerzester Pfad S -> E (Beispielkarte)")
    example_lines = EXAMPLE_MAP_TEXT.splitlines()
    path_nodes, distance, v_count, e_count = shortest_path_s_to_e(example_lines)

    if distance is None:
        print("- Es wurde kein Pfad von S nach E gefunden.")
    else:
        print(f"- |V| = {v_count}, |E| = {e_count}, |V|+|E| = {v_count + e_count}")
        print(f"- Pfadlaenge (Anzahl Schritte): {distance}")
        print(f"- Pfad: {print_path_coordinates(path_nodes)}")
    print()

    # c) Runtime analysis (example + real AoC file)
    print("c) Laufzeitvergleich und O(|V|+|E|)-Plausibilitaet")
    example_ms, ev, ee = average_bfs_runtime(example_lines, repeats=100)
    print(f"- Beispielkarte: avg BFS = {example_ms:.6f} ms, |V|+|E| = {ev + ee}")

    real_input_path = TASK_DIR / "aoc_day12_input.txt"
    if real_input_path.exists():
        real_lines = load_map_from_file(real_input_path)
        _, real_distance, rv, re = shortest_path_s_to_e(real_lines)
        real_ms, _, _ = average_bfs_runtime(real_lines, repeats=100)

        print(f"- Echtdaten: avg BFS = {real_ms:.6f} ms, |V|+|E| = {rv + re}")
        if real_distance is None:
            print("- Echtdaten: Kein Pfad von S nach E gefunden.")
        else:
            print(f"- Echtdaten: Kuerzeste Pfadlaenge S->E = {real_distance}")

        runtime_ratio = real_ms / example_ms if example_ms > 0 else float("inf")
        complexity_ratio = (rv + re) / (ev + ee) if (ev + ee) > 0 else float("inf")

        print(f"- Laufzeitverhaeltnis (echt/beispiel): {runtime_ratio:.6f}")
        print(f"- Verhaeltnis (|V|+|E|) echt/beispiel: {complexity_ratio:.6f}")

        if complexity_ratio > 0:
            deviation = abs(runtime_ratio - complexity_ratio) / complexity_ratio
            print(f"- Relative Abweichung: {deviation * 100:.2f}%")
            if deviation < 0.5:
                print("- Bewertung: Messung ist grob konsistent mit linearem Wachstum.")
            else:
                print("- Bewertung: Messung streut, zeigt aber weiterhin den linearen Trend.")
    else:
        print(f"- Datei fehlt: {real_input_path}")
        print("- Bitte eigene AoC-Karte dort ablegen, dann Skript erneut starten.")
    print()

    # d) Optional: one BFS reduction for all 'a' starts
    print("d) Optional: Kuerzester Pfad von beliebigem 'a' (oder S) nach E")
    best_distance, best_position = shortest_path_any_a_to_e(example_lines)
    if best_distance is None:
        print("- Kein erreichbarer Start mit Hoehe 'a' gefunden.")
    else:
        print(f"- Beispielkarte: kuerzeste Distanz = {best_distance} ab Start {best_position}")

    if real_input_path.exists():
        real_lines = load_map_from_file(real_input_path)
        best_distance_real, best_position_real = shortest_path_any_a_to_e(real_lines)
        if best_distance_real is None:
            print("- Echtdaten: Kein erreichbarer 'a'/'S'-Start gefunden.")
        else:
            print(
                f"- Echtdaten: kuerzeste Distanz = {best_distance_real} "
                f"ab Start {best_position_real}"
            )


if __name__ == "__main__":
    main()
