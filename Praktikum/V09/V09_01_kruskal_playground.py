"""
Daniel Baer
21.06.2026

mINF4/1, V09, Aufgabe "Kruskal - AoC 2025 Day 8 Playground"

V09_01_kruskal_playground.py

Loest die Teilaufgaben a-e fuer Praktikum 9.
"""

from __future__ import annotations

import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
PRAKTIKUM_DIR = TASK_DIR.parent
ALGODAT_DIR = PRAKTIKUM_DIR / "AlgoDatSoSe26"

sys.path.insert(0, str(ALGODAT_DIR))

from utils.algo_priority_queue import PriorityQueue

from V09_kruskal_utils import (
    apply_first_k_edges,
    build_all_edges,
    continue_until_single_circuit,
    init_disjoint_set,
    parse_points_from_lines,
    product_of_three_largest,
)


def load_lines(file_path: Path) -> list[str]:
    with file_path.open("r", encoding="utf-8") as file:
        return file.readlines()


def format_size_list(sizes: list[int]) -> str:
    return "[" + ", ".join(str(size) for size in sizes) + "]"


def model_text_for_task_a(n: int, k: int) -> list[str]:
    total_pairs = n * (n - 1) // 2

    # PriorityQueue from AlgoDat can be used as min-priority structure.
    demo_pq = PriorityQueue()
    demo_pq.add_or_update("k-shortest-edge-strategy", float(k))
    demo_pq.add_or_update("full-sort-strategy", float(total_pairs))
    best_strategy, _ = demo_pq.pop()

    return [
        "a) Modellierung",
        f"- Potenzielle Verbindungen bei n Boxen: n*(n-1)/2 = {n}*{n - 1}/2 = {total_pairs}.",
        "- Fuer exakt globale kuerzeste Kanten ist das vollstaendige Paarmodell korrekt.",
        "- Alternative fuer nur k Kandidaten: Heap/PriorityQueue fuer schrittweise Auswahl.",
        f"- Geeignete Datenstruktur: Priority Queue (Demo-Strategieauswahl: {best_strategy}).",
    ]


def write_answer_file(
    answer_path: Path,
    model_lines: list[str],
    example_points_count: int,
    example_k: int,
    example_sizes: list[int],
    example_product: int,
    own_points_count: int,
    own_k: int,
    own_considered: int,
    own_merged: int,
    own_sizes_after_k: list[int],
    own_product_k: int,
    last_point_u: tuple[int, int, int],
    last_point_v: tuple[int, int, int],
    last_x_product: int,
) -> None:
    lines: list[str] = []
    lines.append("Praktikum 9 - Minimal aufspannende Baeume")
    lines.append("")
    lines.extend(model_lines)
    lines.append("")
    lines.append("b) Union-Find")
    lines.append("- Klasse DisjointSet implementiert: make_set, find_set, union.")
    lines.append("- Erweiterung: Groesse je Schaltkreis wird in O(1) am Repraesentanten gefuehrt.")
    lines.append("")
    lines.append("c) Kruskal auf Beispiel aus aoc_day8.txt")
    lines.append(f"- Anzahl Boxen: {example_points_count}")
    lines.append(f"- k kuerzeste Paare: {example_k}")
    lines.append(f"- Schaltkreisgroessen (absteigend): {format_size_list(example_sizes)}")
    lines.append(f"- Produkt der drei groessten: {example_product}")
    lines.append("- Erwartungswert laut Aufgabe: 40")
    lines.append("")
    lines.append("d) AoC Teil 1 (aoc_input_generated.txt)")
    lines.append(f"- Anzahl Boxen: {own_points_count}")
    lines.append(f"- k kuerzeste Paare: {own_k}")
    lines.append(f"- Betrachtete Kanten: {own_considered}, wirksame unions: {own_merged}")
    lines.append(f"- Schaltkreisgroessen (absteigend): {format_size_list(own_sizes_after_k)}")
    lines.append(f"- Produkt der drei groessten Schaltkreise: {own_product_k}")
    lines.append("")
    lines.append("e) AoC Teil 2 (Kruskal bis ein Schaltkreis)")
    lines.append(f"- Letzte wirksame Verbindung: {last_point_u} <-> {last_point_v}")
    lines.append(f"- Produkt der X-Koordinaten: {last_point_u[0]} * {last_point_v[0]} = {last_x_product}")

    answer_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    print("Praktikum 9 - Minimal aufspannende Baeume")
    print("=" * 60)

    example_file = TASK_DIR / "aoc_day8.txt"
    own_file = TASK_DIR / "aoc_input_generated.txt"

    example_points = parse_points_from_lines(load_lines(example_file))
    own_points = parse_points_from_lines(load_lines(own_file))

    model_lines = model_text_for_task_a(len(own_points), 1000)
    for line in model_lines:
        print(line)

    print("\nb) Union-Find")
    print("- DisjointSet orientiert sich an L09_mst/disjoint.py und speichert Groessen effizient.")

    print("\nc) Kruskal auf Beispiel")
    example_edges = build_all_edges(example_points)
    example_ds = init_disjoint_set(len(example_points))
    example_k = 10
    considered_example, merged_example = apply_first_k_edges(example_ds, example_edges, example_k)
    example_sizes = example_ds.component_sizes_desc()
    example_product = product_of_three_largest(example_sizes)

    print(f"- Beispielpunkte: {len(example_points)}")
    print(f"- Betrachtete Kanten: {considered_example}, wirksame Verbindungen: {merged_example}")
    print(f"- Schaltkreisgroessen: {format_size_list(example_sizes)}")
    print(f"- Produkt der drei groessten: {example_product} (erwartet: 40)")

    print("\nd) AoC Teil 1")
    own_edges = build_all_edges(own_points)
    own_ds = init_disjoint_set(len(own_points))
    own_k = 1000
    considered_own, merged_own = apply_first_k_edges(own_ds, own_edges, own_k)
    own_sizes_after_k = own_ds.component_sizes_desc()
    own_product_k = product_of_three_largest(own_sizes_after_k)

    print(f"- Eigene Punkte: {len(own_points)}")
    print(f"- Betrachtete Kanten: {considered_own}, wirksame Verbindungen: {merged_own}")
    print(f"- Produkt der drei groessten Schaltkreise: {own_product_k}")

    print("\ne) AoC Teil 2")
    last_edge, considered_tail = continue_until_single_circuit(own_ds, own_edges, own_k)
    if last_edge is None:
        raise RuntimeError("Keine letzte Verbindung gefunden.")

    point_u = own_points[last_edge.u]
    point_v = own_points[last_edge.v]
    x_product = point_u[0] * point_v[0]

    print(f"- Zus. betrachtete Kanten nach Teil 1: {considered_tail}")
    print(f"- Letzte wirksame Verbindung: {point_u} <-> {point_v}")
    print(f"- Produkt der X-Koordinaten: {x_product}")

    answer_path = TASK_DIR / "V09_Antworten.txt"
    write_answer_file(
        answer_path=answer_path,
        model_lines=model_lines,
        example_points_count=len(example_points),
        example_k=example_k,
        example_sizes=example_sizes,
        example_product=example_product,
        own_points_count=len(own_points),
        own_k=own_k,
        own_considered=considered_own,
        own_merged=merged_own,
        own_sizes_after_k=own_sizes_after_k,
        own_product_k=own_product_k,
        last_point_u=point_u,
        last_point_v=point_v,
        last_x_product=x_product,
    )
    print(f"\nAntworten geschrieben nach: {answer_path}")


if __name__ == "__main__":
    main()