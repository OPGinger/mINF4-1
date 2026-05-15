"""
Praktikum V05 - Aufgabe 3: Disk-I/O und der Parameter m.

- Fuegt eine feste Zufallssequenz (500 Werte) in B-Baeume mit m = 2, 3, 5, 10, 20 ein
- Erfasst Hoehe, Vergleiche, loaded_count, saved_count
- Erstellt einen Plot und schreibt die Antworten in antworten.txt
"""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TASK_DIR = Path(__file__).resolve().parent
PRAKTIKUM_DIR = TASK_DIR.parent.parent
ALGODAT_DIR = PRAKTIKUM_DIR.parent / "AlgoDatSoSe26"
BTREE_DIR = ALGODAT_DIR / "vorlesung" / "L06_b_baeume"

sys.path.insert(0, str(ALGODAT_DIR))
sys.path.insert(0, str(BTREE_DIR))

from utils.algo_context import AlgoContext  # type: ignore[import-not-found]
from b_tree import BTree  # type: ignore[import-not-found]


def collect_nodes(tree: BTree) -> list:
    """Return all unique nodes of the tree via DFS."""
    out = []
    seen = set()

    def walk(node) -> None:
        if node is None:
            return
        marker = id(node)
        if marker in seen:
            return
        seen.add(marker)
        out.append(node)
        if node.leaf:
            return
        for idx in range(node.n + 1):
            walk(node.children[idx])

    walk(tree.root)
    return out


def run_experiment(values: list[int], orders: list[int]) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []

    for m in orders:
        ctx = AlgoContext()
        tree = BTree(m, ctx)
        for value in values:
            tree.insert(value)

        nodes = collect_nodes(tree)
        loaded_total = sum(node.loaded_count for node in nodes)
        saved_total = sum(node.saved_count for node in nodes)

        rows.append(
            {
                "m": m,
                "height": tree.height(),
                "comparisons": ctx.comparisons,
                "loaded": loaded_total,
                "saved": saved_total,
            }
        )

    return rows


def save_plot(rows: list[dict[str, float]]) -> Path:
    ms = [int(row["m"]) for row in rows]
    heights = [float(row["height"]) for row in rows]
    comparisons = [float(row["comparisons"]) for row in rows]
    loaded = [float(row["loaded"]) for row in rows]
    saved = [float(row["saved"]) for row in rows]

    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    flat = list(axes.flat)

    flat[0].plot(ms, heights, marker="o")
    flat[0].set_title("Baumhoehe")
    flat[0].set_xlabel("Ordnung m")
    flat[0].set_ylabel("Hoehe")
    flat[0].grid(True)

    flat[1].plot(ms, comparisons, marker="s")
    flat[1].set_title("Vergleiche")
    flat[1].set_xlabel("Ordnung m")
    flat[1].set_ylabel("ctx.comparisons")
    flat[1].grid(True)

    flat[2].plot(ms, loaded, marker="^")
    flat[2].set_title("Disk-Loads")
    flat[2].set_xlabel("Ordnung m")
    flat[2].set_ylabel("sum(loaded_count)")
    flat[2].grid(True)

    flat[3].plot(ms, saved, marker="d")
    flat[3].set_title("Disk-Saves")
    flat[3].set_xlabel("Ordnung m")
    flat[3].set_ylabel("sum(saved_count)")
    flat[3].grid(True)

    fig.tight_layout()
    out_file = TASK_DIR / "io_vergleiche_hoehe_plot.png"
    fig.savefig(out_file, dpi=150)
    plt.close(fig)
    return out_file


def estimate_optimal_m(block_size_bytes: int = 4096, key_bytes: int = 8, ptr_bytes: int = 8) -> int:
    """
    Per node storage model:
    - max keys: 2m - 1
    - max child pointers: 2m

    Memory: (2m - 1) * key_bytes + (2m) * ptr_bytes <= block_size_bytes
    """
    numerator = block_size_bytes + key_bytes
    denominator = 2 * (key_bytes + ptr_bytes)
    return numerator // denominator


def main() -> None:
    orders = [2, 3, 5, 10, 20]
    rnd = random.Random(20260515)
    values = rnd.sample(range(-50_000, 50_000), 500)

    rows = run_experiment(values, orders)
    plot_file = save_plot(rows)

    n = len(values)
    optimal_m = estimate_optimal_m()

    answer_lines = [
        "Praktikum 5 - Aufgabe 3: Disk-I/O und Parameter m",
        f"Zufallssequenz: n = {n} (ohne Duplikate, Seed = 20260515)",
        "",
        "Messwerte:",
    ]

    for row in rows:
        answer_lines.append(
            f"m={int(row['m'])}: hoehe={int(row['height'])}, vergleiche={int(row['comparisons'])}, "
            f"loads={int(row['loaded'])}, saves={int(row['saved'])}"
        )

    answer_lines.extend(
        [
            "",
            "Warum sinkt die Zahl der Plattenzugriffe bei groesserem m?",
            "Mit groesserem m sinkt die Baumhoehe ungefaehr wie log_m(n).",
            "Eine Einfuegung besucht weniger Ebenen und damit weniger Knoten auf dem Speicher.",
            "Daher nehmen load/save-Zugriffe insgesamt ab.",
            "",
            "Warum steigen interne Vergleiche trotz sinkender Hoehe?",
            "In dieser Implementierung wird innerhalb eines Knotens linear gesucht.",
            "Pro Ebene fallen damit bis zu O(m) Vergleiche an.",
            "Mit Hoehe O(log_m n) ergibt sich pro Einfuegung asymptotisch:",
            "T_insert(n, m) = O(m * log_m n) = O((m / ln m) * ln n).",
            "Damit sinkt die Ebenenzahl, aber die Arbeit pro Ebene steigt mit m.",
            "",
            "4KB-Blockgroesse: optimale Ordnung m",
            "Speichermodell je Knoten:",
            "(2m-1)*8 Byte fuer Schluessel + (2m)*8 Byte fuer Kindzeiger <= 4096 Byte",
            "=> 8*(4m-1) <= 4096",
            "=> 32m - 8 <= 4096",
            "=> m <= 128.",
            f"Theoretisch optimale (maximale passende) Ordnung: m = {optimal_m}",
            "(Metadaten wie leaf-Flag oder n koennen in der Praxis einen minimal kleineren Wert noetig machen.)",
            "",
            f"Plot-Datei: {plot_file.name}",
        ]
    )

    (TASK_DIR / "antworten.txt").write_text("\n".join(answer_lines) + "\n", encoding="utf-8")

    print("Aufgabe 3 abgeschlossen")
    print(f"Plot: {plot_file}")
    for row in rows:
        print(
            f"m={int(row['m'])}: h={int(row['height'])}, cmp={int(row['comparisons'])}, "
            f"load={int(row['loaded'])}, save={int(row['saved'])}"
        )


if __name__ == "__main__":
    main()
