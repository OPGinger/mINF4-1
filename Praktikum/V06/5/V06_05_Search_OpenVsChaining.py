"""
Daniel Baer
26.05.2026

mINF4/1, V06, Task 5 "Vergleich Suche: offene Adressierung vs verkettete Listen"

V06_05_Search_OpenVsChaining.py

This script measures ctx.comparisons for successful searches in both strategies.
Tables with sizes [50, 100, 200, 500, 1000] are filled to alpha ~0.7 and alpha ~0.9
using random values generated via Array.random.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Resolve local directories relative to this task folder.
TASK_DIR = Path(__file__).resolve().parent
V06_DIR = TASK_DIR.parent
PRAKTIKUM_DIR = V06_DIR.parent
ALGODAT_DIR = PRAKTIKUM_DIR / "AlgoDatSoSe26"

# Add module paths for shared V06 code and AlgoDat lecture code.
sys.path.insert(0, str(V06_DIR))
sys.path.insert(0, str(ALGODAT_DIR))

from utils.algo_array import Array  # type: ignore[import-not-found]
from utils.algo_context import AlgoContext  # type: ignore[import-not-found]
from utils.algo_int import Int  # type: ignore[import-not-found]
from vorlesung.L07_hashtable.analyze_hashtable import f, h  # type: ignore[import-not-found]
from vorlesung.L07_hashtable.hashtable import HashTableOpenAddressing  # type: ignore[import-not-found]
from V06_hashtable_chaining import HashTableChaining


def fill_tables(m: int, target_alpha: float) -> dict[str, object]:
    """Fill both tables with random data until approximately target_alpha."""
    target_n = max(1, int(round(m * target_alpha)))

    ctx_open = AlgoContext()
    ctx_chain = AlgoContext()
    ctx_gen = AlgoContext()

    open_ht = HashTableOpenAddressing(m, f, ctx_open)
    chain_ht = HashTableChaining(m, h, ctx_chain)

    open_values: list[int] = []

    # Deterministic batch generation keeps experiments reproducible.
    batch_size = 64
    guard = 0
    max_guard = 200000

    while (len(open_values) < target_n or chain_ht.n < target_n) and guard < max_guard:
        batch = Array.random(batch_size, -1_000_000, 1_000_000, ctx_gen)
        for cell in batch:
            value = int(cell)

            if len(open_values) < target_n:
                if open_ht.insert(Int(value, ctx_open)):
                    open_values.append(value)

            if chain_ht.n < target_n:
                chain_ht.insert(Int(value, ctx_chain))

            guard += 1
            if guard >= max_guard:
                break

    chain_values = 0#[int(key) for key in chain_ht.keys()]

    return {
        "m": m,
        "target_alpha": target_alpha,
        "open_ctx": ctx_open,
        "chain_ctx": ctx_chain,
        "open_ht": open_ht,
        "chain_ht": chain_ht,
        "open_values": open_values,
        "chain_values": chain_values,
    }


def measure_search_comparisons(exp: dict[str, object]) -> dict[str, float | int]:
    """Measure comparisons for searching all inserted keys once."""
    ctx_open = exp["open_ctx"]
    ctx_chain = exp["chain_ctx"]
    open_ht = exp["open_ht"]
    chain_ht = exp["chain_ht"]
    open_values = exp["open_values"]
    chain_values = exp["chain_values"]

    assert isinstance(ctx_open, AlgoContext)
    assert isinstance(ctx_chain, AlgoContext)
    assert isinstance(open_ht, HashTableOpenAddressing)
    assert isinstance(chain_ht, HashTableChaining)
    assert isinstance(open_values, list)
    assert isinstance(chain_values, list)

    ctx_open.reset()
    for value in open_values:
        open_ht.search(Int(value, ctx_open))
    open_comp = ctx_open.comparisons

    ctx_chain.reset()
    for value in chain_values:
        chain_ht.search(Int(value, ctx_chain))
    chain_comp = ctx_chain.comparisons

    return {
        "m": int(exp["m"]),
        "target_alpha": float(exp["target_alpha"]),
        "open_n": len(open_values),
        "chain_n": len(chain_values),
        "open_alpha": open_ht.alpha(),
        "chain_alpha": chain_ht.alpha(),
        "open_comp_total": open_comp,
        "chain_comp_total": chain_comp,
        "open_comp_avg": open_comp / len(open_values) if open_values else 0.0,
        "chain_comp_avg": chain_comp / len(chain_values) if chain_values else 0.0,
    }


def run_experiment(sizes: list[int], target_alpha: float) -> list[dict[str, float | int]]:
    """Run one alpha-level experiment for all requested table sizes."""
    rows: list[dict[str, float | int]] = []
    for m in sizes:
        exp = fill_tables(m, target_alpha)
        rows.append(measure_search_comparisons(exp))
    return rows


def save_csv(rows_07: list[dict[str, float | int]], rows_09: list[dict[str, float | int]]) -> Path:
    """Store all measurements in CSV format."""
    lines = [
        "alpha_target,m,open_n,chain_n,open_alpha,chain_alpha,open_comp_total,chain_comp_total,open_comp_avg,chain_comp_avg"
    ]

    for row in rows_07 + rows_09:
        lines.append(
            f"{float(row['target_alpha']):.1f},"
            f"{int(row['m'])},"
            f"{int(row['open_n'])},"
            f"{int(row['chain_n'])},"
            f"{float(row['open_alpha']):.6f},"
            f"{float(row['chain_alpha']):.6f},"
            f"{int(row['open_comp_total'])},"
            f"{int(row['chain_comp_total'])},"
            f"{float(row['open_comp_avg']):.6f},"
            f"{float(row['chain_comp_avg']):.6f}"
        )

    out = TASK_DIR / "messwerte.csv"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def save_plot(rows_07: list[dict[str, float | int]], rows_09: list[dict[str, float | int]]) -> Path:
    """Create a comparison plot for average comparisons per successful search."""
    x_07 = [int(row["m"]) for row in rows_07]
    open_07 = [float(row["open_comp_avg"]) for row in rows_07]
    chain_07 = [float(row["chain_comp_avg"]) for row in rows_07]

    x_09 = [int(row["m"]) for row in rows_09]
    open_09 = [float(row["open_comp_avg"]) for row in rows_09]
    chain_09 = [float(row["chain_comp_avg"]) for row in rows_09]

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(x_07, open_07, marker="o", label="Open Addressing (alpha~0.7)")
    ax.plot(x_07, chain_07, marker="s", label="Chaining (alpha~0.7)")
    ax.plot(x_09, open_09, marker="^", label="Open Addressing (alpha~0.9)")
    ax.plot(x_09, chain_09, marker="d", label="Chaining (alpha~0.9)")

    ax.set_title("Task 5 - Search Comparisons (successful searches)")
    ax.set_xlabel("Table size m")
    ax.set_ylabel("Average comparisons per search")
    ax.grid(True)
    ax.legend()

    out = TASK_DIR / "vergleich_plot.png"
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def save_answers(rows_07: list[dict[str, float | int]], rows_09: list[dict[str, float | int]]) -> Path:
    """Write concise interpretation for questions 5a to 5c."""
    lines: list[str] = [
        "Task 5 - Comparison of Search Comparisons",
        "Measured metric: ctx.comparisons during successful search of all inserted keys",
        "",
        "alpha ~ 0.7:",
    ]

    for row in rows_07:
        lines.append(
            f"m={int(row['m'])}: open_avg={float(row['open_comp_avg']):.4f}, chain_avg={float(row['chain_comp_avg']):.4f}"
        )

    lines.extend([
        "",
        "alpha ~ 0.9:",
    ])

    for row in rows_09:
        lines.append(
            f"m={int(row['m'])}: open_avg={float(row['open_comp_avg']):.4f}, chain_avg={float(row['chain_comp_avg']):.4f}"
        )

    # Aggregate comparison statements over all tested sizes.
    mean_open_07 = sum(float(r["open_comp_avg"]) for r in rows_07) / len(rows_07)
    mean_chain_07 = sum(float(r["chain_comp_avg"]) for r in rows_07) / len(rows_07)
    mean_open_09 = sum(float(r["open_comp_avg"]) for r in rows_09) / len(rows_09)
    mean_chain_09 = sum(float(r["chain_comp_avg"]) for r in rows_09) / len(rows_09)

    lines.extend([
        "",
        "5a) Which strategy needs more comparisons at equal alpha (~0.7)?",
        (
            f"Average over tested sizes: open={mean_open_07:.4f}, chain={mean_chain_07:.4f}. "
            "The larger value indicates the more comparison-heavy strategy at alpha~0.7."
        ),
        "",
        "5b) What changes at alpha~0.9?",
        (
            f"Average over tested sizes: open={mean_open_09:.4f}, chain={mean_chain_09:.4f}. "
            "Compared to alpha~0.7, open addressing usually grows more strongly due to long probe chains."
        ),
        "",
        "5c) One advantage of each strategy:",
        "- Chaining: insertions remain possible beyond alpha=1 and deletion is simple (no tombstones).",
        "- Open addressing: compact memory layout, often cache-friendly due to contiguous table access.",
    ])

    out = TASK_DIR / "antworten.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main() -> None:
    sizes = [50, 100, 200, 500, 1000]

    rows_07 = run_experiment(sizes, 0.7)
    rows_09 = run_experiment(sizes, 0.9)

    csv_file = save_csv(rows_07, rows_09)
    plot_file = save_plot(rows_07, rows_09)
    answers_file = save_answers(rows_07, rows_09)

    print("Task 5 finished.")
    print(f"CSV: {csv_file}")
    print(f"Plot: {plot_file}")
    print(f"Answers: {answers_file}")


if __name__ == "__main__":
    main()
