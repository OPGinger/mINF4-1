"""
Daniel Baer
21.06.2026

mINF4/1, V09, Aufgabe "Kruskal - AoC 2025 Day 8 Playground"

V09_kruskal_utils.py

Hilfsfunktionen fuer Parsing, Distanzberechnung, Union-Find und Kruskal.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


Point3D = tuple[int, int, int]


@dataclass(order=True)
class Edge:
    dist: float
    u: int
    v: int


class DisjointSet:
    """Union-Find mit path compression und union by size."""

    def __init__(self) -> None:
        self.parent: dict[int, int] = {}
        self.size: dict[int, int] = {}

    def make_set(self, value: int) -> None:
        self.parent[value] = value
        self.size[value] = 1

    def find_set(self, value: int) -> int:
        parent = self.parent[value]
        if parent != value:
            self.parent[value] = self.find_set(parent)
        return self.parent[value]

    def union(self, u: int, v: int) -> bool:
        root_u = self.find_set(u)
        root_v = self.find_set(v)

        if root_u == root_v:
            return False

        if self.size[root_u] < self.size[root_v]:
            root_u, root_v = root_v, root_u

        self.parent[root_v] = root_u
        self.size[root_u] += self.size[root_v]
        del self.size[root_v]
        return True

    def component_size(self, value: int) -> int:
        return self.size[self.find_set(value)]

    def component_sizes_desc(self) -> list[int]:
        return sorted(self.size.values(), reverse=True)

    def component_count(self) -> int:
        return len(self.size)


def is_coordinate_line(line: str) -> bool:
    parts = line.strip().split(",")
    if len(parts) != 3:
        return False
    for part in parts:
        stripped = part.strip()
        if not stripped:
            return False
        if stripped[0] == "-":
            if len(stripped) == 1 or not stripped[1:].isdigit():
                return False
        elif not stripped.isdigit():
            return False
    return True


def parse_points_from_lines(lines: list[str]) -> list[Point3D]:
    points: list[Point3D] = []
    for line in lines:
        if not is_coordinate_line(line):
            continue
        x_str, y_str, z_str = [part.strip() for part in line.strip().split(",")]
        points.append((int(x_str), int(y_str), int(z_str)))
    return points


def euclidean_distance(p1: Point3D, p2: Point3D) -> float:
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    return sqrt(dx * dx + dy * dy + dz * dz)


def build_all_edges(points: list[Point3D]) -> list[Edge]:
    edges: list[Edge] = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            edges.append(Edge(euclidean_distance(points[i], points[j]), i, j))
    edges.sort()
    return edges


def init_disjoint_set(count: int) -> DisjointSet:
    ds = DisjointSet()
    for index in range(count):
        ds.make_set(index)
    return ds


def product_of_three_largest(sizes_desc: list[int]) -> int:
    if len(sizes_desc) < 3:
        raise ValueError("Mindestens drei Schaltkreise werden benoetigt.")
    return sizes_desc[0] * sizes_desc[1] * sizes_desc[2]


def apply_first_k_edges(
    ds: DisjointSet,
    edges_sorted: list[Edge],
    k: int,
) -> tuple[int, int]:
    considered = min(k, len(edges_sorted))
    merged = 0
    for edge in edges_sorted[:considered]:
        if ds.union(edge.u, edge.v):
            merged += 1
    return considered, merged


def continue_until_single_circuit(
    ds: DisjointSet,
    edges_sorted: list[Edge],
    start_index: int,
) -> tuple[Edge | None, int]:
    last_effective_edge: Edge | None = None
    considered = 0

    for edge in edges_sorted[start_index:]:
        considered += 1
        if ds.union(edge.u, edge.v):
            last_effective_edge = edge
            if ds.component_count() == 1:
                break

    return last_effective_edge, considered