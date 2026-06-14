"""
Daniel Baer
14.06.2026

mINF4/1, V08, Aufgabe 1 "Dijkstra - Reindeer Maze"

V08_01_dijkstra.py

Modelliert das AoC Day-16-Labyrinth als gerichteten Zustandsgraphen
(Zeile, Spalte, Richtung) und berechnet den guenstigsten Pfad mit Dijkstra.
"""

import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
PRAKTIKUM_DIR = TASK_DIR.parent
ALGODAT_DIR = PRAKTIKUM_DIR / "AlgoDatSoSe26"

sys.path.insert(0, str(ALGODAT_DIR))

from vorlesung.L08_graphen.graph import AdjacencyListGraph


EXAMPLE_MAZE_TEXT = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

DIRECTIONS = ["N", "O", "S", "W"]
DIR_TO_INDEX = {direction: index for index, direction in enumerate(DIRECTIONS)}
DELTA_BY_DIRECTION = {
    "N": (-1, 0),
    "O": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}


def state_name(row: int, col: int, direction: str) -> str:
    return f"{row},{col},{direction}"


def parse_state_name(name: str) -> tuple[int, int, str]:
    row_str, col_str, direction = name.split(",")
    return int(row_str), int(col_str), direction


def load_grid_from_lines(lines: list[str]) -> tuple[list[list[str]], tuple[int, int], tuple[int, int]]:
    stripped = [line.rstrip("\n") for line in lines if line.strip()]
    if not stripped:
        raise ValueError("Die Eingabekarte ist leer.")

    width = len(stripped[0])
    for line in stripped:
        if len(line) != width:
            raise ValueError("Die Karte ist nicht rechteckig.")

    grid = [list(line) for line in stripped]
    start = None
    end = None

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            char = grid[row][col]
            if char == "S":
                if start is not None:
                    raise ValueError("Mehrere Startpunkte S gefunden.")
                start = (row, col)
            elif char == "E":
                if end is not None:
                    raise ValueError("Mehrere Zielpunkte E gefunden.")
                end = (row, col)
            elif char not in {"#", "."}:
                raise ValueError(f"Unbekanntes Kartenzeichen: {char}")

    if start is None:
        raise ValueError("Kein Startpunkt S gefunden.")
    if end is None:
        raise ValueError("Kein Zielpunkt E gefunden.")

    return grid, start, end


def is_walkable(grid: list[list[str]], row: int, col: int) -> bool:
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return False
    return grid[row][col] != "#"


def build_reindeer_state_graph(grid: list[list[str]]) -> tuple[AdjacencyListGraph, int, int, int]:
    graph = AdjacencyListGraph()
    rows = len(grid)
    cols = len(grid[0])

    walkable_cells = 0
    for row in range(rows):
        for col in range(cols):
            if is_walkable(grid, row, col):
                walkable_cells += 1
                for direction in DIRECTIONS:
                    graph.insert_vertex(state_name(row, col, direction))

    edge_count = 0

    for row in range(rows):
        for col in range(cols):
            if not is_walkable(grid, row, col):
                continue

            for direction in DIRECTIONS:
                current = state_name(row, col, direction)

                right_direction = DIRECTIONS[(DIR_TO_INDEX[direction] + 1) % 4]
                left_direction = DIRECTIONS[(DIR_TO_INDEX[direction] - 1) % 4]

                graph.connect(current, state_name(row, col, right_direction), 1000)
                graph.connect(current, state_name(row, col, left_direction), 1000)
                edge_count += 2

                delta_row, delta_col = DELTA_BY_DIRECTION[direction]
                next_row = row + delta_row
                next_col = col + delta_col
                if is_walkable(grid, next_row, next_col):
                    graph.connect(current, state_name(next_row, next_col, direction), 1)
                    edge_count += 1

    vertex_count = walkable_cells * 4
    return graph, walkable_cells, vertex_count, edge_count


def theoretical_counts_no_walls(rows: int, cols: int) -> tuple[int, int, int]:
    vertex_count = 4 * rows * cols
    forward_edges = 2 * (rows - 1) * cols + 2 * rows * (cols - 1)
    turn_edges = 8 * rows * cols
    edge_count = forward_edges + turn_edges
    return vertex_count, edge_count, forward_edges


def reconstruct_vertex_path(end_vertex, predecessor_map) -> list[str]:
    path = []
    current = end_vertex
    while current is not None:
        path.insert(0, current.value)
        current = predecessor_map[current]
    return path


def actions_from_state_path(path_states: list[str]) -> list[str]:
    if len(path_states) <= 1:
        return []

    actions = []
    for index in range(1, len(path_states)):
        prev_row, prev_col, prev_dir = parse_state_name(path_states[index - 1])
        cur_row, cur_col, cur_dir = parse_state_name(path_states[index])

        if prev_row == cur_row and prev_col == cur_col:
            prev_idx = DIR_TO_INDEX[prev_dir]
            cur_idx = DIR_TO_INDEX[cur_dir]
            if cur_idx == (prev_idx + 1) % 4:
                actions.append("R")
            elif cur_idx == (prev_idx - 1) % 4:
                actions.append("L")
            else:
                actions.append("?")
        elif prev_dir == cur_dir:
            actions.append("F")
        else:
            actions.append("?")

    return actions


def solve_maze(lines: list[str]) -> dict:
    grid, start, end = load_grid_from_lines(lines)
    graph, walkable_cells, vertex_count, edge_count = build_reindeer_state_graph(grid)

    start_name = state_name(start[0], start[1], "O")
    distance_map, predecessor_map = graph.dijkstra(start_name)

    best_end_vertex = None
    best_cost = float("inf")
    for direction in DIRECTIONS:
        candidate_vertex = graph.get_vertex(state_name(end[0], end[1], direction))
        candidate_cost = distance_map[candidate_vertex]
        if candidate_cost < best_cost:
            best_cost = candidate_cost
            best_end_vertex = candidate_vertex

    if best_end_vertex is None or best_cost == float("inf"):
        return {
            "rows": len(grid),
            "cols": len(grid[0]),
            "walkable": walkable_cells,
            "vertex_count": vertex_count,
            "edge_count": edge_count,
            "cost": None,
            "path_states": [],
            "actions": [],
        }

    path_states = reconstruct_vertex_path(best_end_vertex, predecessor_map)
    actions = actions_from_state_path(path_states)

    return {
        "rows": len(grid),
        "cols": len(grid[0]),
        "walkable": walkable_cells,
        "vertex_count": vertex_count,
        "edge_count": edge_count,
        "cost": int(best_cost),
        "path_states": path_states,
        "actions": actions,
    }


def load_lines(file_path: Path) -> list[str]:
    with file_path.open("r", encoding="utf-8") as file:
        return file.readlines()


def write_answer_file(example_result: dict, own_result: dict) -> None:
    answer_path = TASK_DIR / "V08_Antworten.txt"

    rows = own_result["rows"]
    cols = own_result["cols"]
    v_theory, e_theory, e_forward = theoretical_counts_no_walls(rows, cols)

    own_path_full = " -> ".join(own_result["path_states"])
    own_actions = "".join(own_result["actions"])

    text_lines = [
        "Praktikum 8 - Kuerzeste Wege",
        "",
        "Aufgabe 1: Dijkstra - Reindeer Maze",
        "",
        "a) Modellierung",
        "- Zustand: (Zeile, Spalte, Richtung) mit Richtung in {N, O, S, W}.",
        "- Fuer eine Karte ohne Waende mit R Zeilen und C Spalten gilt:",
        f"  Knotenanzahl |V| = 4 * R * C = 4 * {rows} * {cols} = {v_theory}",
        f"  Vorwaertskanten = 2*(R-1)*C + 2*R*(C-1) = {e_forward}",
        f"  Drehkanten = 8*R*C = {8 * rows * cols}",
        f"  Gesamtkanten |E| = {e_theory}",
        "- Geeignete Darstellung: Adjazenzliste, da der Graph duenn besetzt ist",
        "  und eine Adjazenzmatrix O(|V|^2) Speicher benoetigen wuerde.",
        "",
        "b) Dijkstra auf dem Beispiel-Labyrinth",
        f"- Kosten minimaler Pfad: {example_result['cost']}",
        f"- Anzahl Zustaende im Pfad: {len(example_result['path_states'])}",
        f"- Aktionsfolge (F/L/R): {''.join(example_result['actions'])}",
        f"- Zustandspfad: {' -> '.join(example_result['path_states'])}",
        "",
        "c) Eigener AoC-Parcours (input_generated.txt)",
        f"- Kartengroesse: {own_result['rows']} x {own_result['cols']}",
        f"- Begehbare Felder: {own_result['walkable']}",
        f"- Zustandsgraf: |V|={own_result['vertex_count']}, |E|={own_result['edge_count']}",
        f"- Minimale Kosten: {own_result['cost']}",
        f"- Anzahl Zustaende im Pfad: {len(own_result['path_states'])}",
        f"- Aktionsfolge (F/L/R): {own_actions}",
        f"- Zustandspfad: {own_path_full}",
        "",
    ]

    answer_path.write_text("\n".join(text_lines), encoding="utf-8")


def main() -> None:
    print("Aufgabe 1: Dijkstra - Reindeer Maze")
    print("=" * 60)

    own_input_path = TASK_DIR / "input_generated.txt"
    own_lines = load_lines(own_input_path)

    example_lines = EXAMPLE_MAZE_TEXT.splitlines()

    example_result = solve_maze(example_lines)
    own_result = solve_maze(own_lines)

    rows = own_result["rows"]
    cols = own_result["cols"]
    v_theory, e_theory, e_forward = theoretical_counts_no_walls(rows, cols)

    print("a) Modellierung")
    print(f"- |V| = 4*R*C = {v_theory} fuer R={rows}, C={cols}")
    print(f"- Vorwaertskanten = 2*(R-1)*C + 2*R*(C-1) = {e_forward}")
    print(f"- Gesamtkanten |E| = {e_theory}")
    print("- Wahl: Adjazenzliste (duenner Graph)")
    print()

    print("b) Beispiel-Labyrinth")
    print(f"- Minimalen Kosten: {example_result['cost']}")
    print(f"- Pfadlaenge (Zustaende): {len(example_result['path_states'])}")
    print(f"- Pfad (Zustaende): {' -> '.join(example_result['path_states'])}")
    print()

    print("c) Eigener Parcours aus input_generated.txt")
    print(f"- |V|={own_result['vertex_count']}, |E|={own_result['edge_count']}")
    print(f"- Minimale Kosten: {own_result['cost']}")
    print(f"- Pfadlaenge (Zustaende): {len(own_result['path_states'])}")

    write_answer_file(example_result, own_result)
    print()
    print("Ergebnisse wurden nach V08_Antworten.txt geschrieben.")


if __name__ == "__main__":
    main()
