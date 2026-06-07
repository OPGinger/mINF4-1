"""
Daniel Baer
07.06.2026

mINF4/1, V07, Zusatz "Graphen erzeugen"

V07_03_Graphen_erzeugen.py

Dieses Skript erzeugt Graph-Dateien fuer Aufgabe 1 und Aufgabe 2.
Es schreibt immer .gv-Dateien und erstellt zusaetzlich .pdf, falls dot verfuegbar ist.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from V07_01_BFS_Hoehenkarte import (
    EXAMPLE_MAP_TEXT,
    build_height_graph,
    load_map_from_file,
    parse_heightmap,
)
from V07_02_DFS_TopSort import build_dependency_graph


SCRIPT_DIR = Path(__file__).resolve().parent
LOCAL_DOT = SCRIPT_DIR.parent / "Graphviz-14.1.5-win64" / "bin" / "dot.exe"


def write_gv_file(file_path: Path, title: str, edges: list[tuple[str, str, float]]) -> None:
    """Write a directed graph in Graphviz DOT syntax."""
    with file_path.open("w", encoding="utf-8") as file:
        file.write(f'digraph "{title}" {{\n')
        file.write("  rankdir=LR;\n")
        file.write('  node [shape=ellipse, fontname="Arial"];\n')

        # Write all edges.
        for src, dst, weight in edges:
            if weight == 1:
                file.write(f'  "{src}" -> "{dst}";\n')
            else:
                file.write(f'  "{src}" -> "{dst}" [label="{weight}"];\n')

        file.write("}\n")


def find_dot_executable() -> str | None:
    """Find dot executable either in PATH or in local Graphviz folder."""
    dot_in_path = shutil.which("dot")
    if dot_in_path:
        return dot_in_path

    if LOCAL_DOT.exists():
        return str(LOCAL_DOT)

    return None


def render_pdf(dot_exe: str, gv_file: Path, pdf_file: Path) -> bool:
    """Render GV file to PDF using dot command."""
    command = [dot_exe, "-Tpdf", str(gv_file), "-o", str(pdf_file)]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False


def main() -> None:
    # Aufgabe 1: Graph fuer Beispielkarte
    example_lines = EXAMPLE_MAP_TEXT.splitlines()
    example_grid, _, _ = parse_heightmap(example_lines)
    example_graph, _, _ = build_height_graph(example_grid)

    gv_a1_example = SCRIPT_DIR / "Aufgabe1_Graph_Beispiel.gv"
    write_gv_file(gv_a1_example, "Aufgabe1_Beispiel", example_graph.all_edges())

    # Aufgabe 1: Graph fuer echte Karte
    real_input = SCRIPT_DIR / "aoc_day12_input.txt"
    if real_input.exists():
        real_lines = load_map_from_file(real_input)
        real_grid, _, _ = parse_heightmap(real_lines)
        real_graph, _, _ = build_height_graph(real_grid)

        gv_a1_real = SCRIPT_DIR / "Aufgabe1_Graph_Echtkarte.gv"
        write_gv_file(gv_a1_real, "Aufgabe1_Echtkarte", real_graph.all_edges())
    else:
        gv_a1_real = None

    # Aufgabe 2: Abhaengigkeitsgraph
    dep_graph, _ = build_dependency_graph()
    gv_a2 = SCRIPT_DIR / "Aufgabe2_Abhaengigkeiten.gv"
    write_gv_file(gv_a2, "Aufgabe2_Abhaengigkeiten", dep_graph.all_edges())

    print("GV-Dateien erzeugt:")
    print(f"- {gv_a1_example}")
    if gv_a1_real is not None:
        print(f"- {gv_a1_real}")
    print(f"- {gv_a2}")

    # Optional PDF rendering via dot.
    dot_exe = find_dot_executable()
    if dot_exe is None:
        print("dot nicht gefunden: PDF-Rendering uebersprungen.")
        return

    print(f"dot gefunden: {dot_exe}")

    pdf_targets: list[tuple[Path, Path]] = [
        (gv_a1_example, SCRIPT_DIR / "Aufgabe1_Graph_Beispiel.pdf"),
        (gv_a2, SCRIPT_DIR / "Aufgabe2_Abhaengigkeiten.pdf"),
    ]
    if gv_a1_real is not None:
        pdf_targets.append((gv_a1_real, SCRIPT_DIR / "Aufgabe1_Graph_Echtkarte.pdf"))

    for gv_file, pdf_file in pdf_targets:
        if render_pdf(dot_exe, gv_file, pdf_file):
            print(f"- PDF erzeugt: {pdf_file}")
        else:
            print(f"- PDF fehlgeschlagen: {pdf_file}")


if __name__ == "__main__":
    main()
