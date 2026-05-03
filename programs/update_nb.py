import nbformat
import sys

nb_path = "/Users/abdelouahad/Downloads/ProjectKRR-main/programs/benchmark/benchmark.ipynb"
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# Update Cell 0: The main definitions
cell0_code = """from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path
from statistics import mean, stdev
from typing import Generator, Tuple

import clingo
import matplotlib.pyplot as plt
import pandas as pd
import secrets
import generator

def run_gen(c: int, n: int, m: int, k: int, w: int) -> float:
    start = time.perf_counter()
    generator.run_generator(c, n, m, k, w)
    return time.perf_counter() - start

def run_solver() -> float:
    start = time.perf_counter()
    generator.run_solver()
    return time.perf_counter() - start

def init_csv(path: Path):
    with path.open("w", newline="") as fh:
        csv.writer(fh).writerow(["c", "n", "m", "k", "w", "run", "seconds", "size"])

def append_csv(path: Path, c: int, n: int, m: int, k: int, w: int, run_idx: int, seconds: float):
    with path.open("a", newline="") as fh:
        csv.writer(fh).writerow([c, n, m, k, w, run_idx, f"{seconds:.6f}", c])

def aggregate(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    grp = df.groupby("size").agg(mean_seconds=("seconds", mean), std_seconds=("seconds", stdev)).reset_index()
    grp.sort_values("size", inplace=True)
    return grp

def plot_size_vs_time(df: pd.DataFrame, out_svg: Path | None, logscale=True):
    fig, ax = plt.subplots()
    ax.plot(df["size"], df["mean_seconds"], 'o-')

    for _, row in df.iterrows():
        x = float(row["size"])
        y = float(row["mean_seconds"])
        ax.annotate(
            f"{int(row['size'])}",
            xy=(x, y),
            textcoords="offset points",
            xytext=(0, 5),
            ha="center",
        )

    ax.set_xlabel("Problem size (c = number of cubes)")
    if logscale:
        ax.set_ylabel("Mean runtime (s, log-scale)")
        ax.set_yscale("log")
    else:
        ax.set_ylabel("Mean runtime (s)")
    ax.set_title("Clingo runtime vs. problem size (3DSRP)")
    ax.grid(True, which="both", linestyle=":", linewidth=0.5)
    fig.tight_layout()
    if out_svg:
        fig.savefig(out_svg, format="svg")
        print(f"Saved plot to {out_svg}")

    plt.show()

def run(sizes, csv_file, gen, n_runs=10):
    total_runs = len(sizes) * n_runs
    current = 0
    for c, n, m, k, w in sizes:
        for run_idx in range(1, n_runs + 1):
            current += 1
            print(f"\\r[{current}/{total_runs}] c={c} n={n} m={m} k={k} w={w} run={run_idx} ...", end="", flush=True)
            secs = gen(c, n, m, k, w)
            append_csv(csv_file, c, n, m, k, w, run_idx, secs)
"""
nb.cells[0].source = cell0_code

# Update Cell 1: Test run
nb.cells[1].source = """generator.run_generator(c=8, n=2, m=2, k=2, w=2, print_out=False)
print("Generator finished")
generator.run_solver(print_out=True)"""

# Update Cell 2: CSV paths
nb.cells[2].source = """CSV_SOLVER = Path("results/solver_3dsrp.csv")
SVG_SOLVER = Path("results/solver_3dsrp.svg")

CSV_SOLVER.parent.mkdir(parents=True, exist_ok=True)"""

# Update Cell 3: Init CSV
nb.cells[3].source = """init_csv(CSV_SOLVER)"""

# Update Cell 4: Sizes array
nb.cells[4].source = """sizes = []
# For 3DSRP, we vary c from 8 to 24 cubes.
# parameters: c, n, m, k, w
for c in range(8, 25, 4):
    n = int(c**(1/3)) + 2
    m = max(1, c // 4)
    k = 2
    w = max(1, c // 4)
    sizes.append((c, n, m, k, w))

print("Sizes to benchmark (c, n, m, k, w):", sizes)"""

# Update Cell 5: Run generator
nb.cells[5].source = """# We test the solver directly over the generated sizes
# gen runs generator, solver is measured separately or wrapped
# let's just benchmark the solver:
def run_solver_bench(c, n, m, k, w):
    # First generate facts without measuring
    generator.run_generator(c, n, m, k, w, print_out=False)
    # Then measure solver
    return generator.run_solver(print_out=False)

run(sizes, CSV_SOLVER, run_solver_bench, n_runs=5)"""

# Clear other executing cells for safety to run cleanly later
for i in range(6, len(nb.cells)):
    if "df =" in nb.cells[i].source or "plot" in nb.cells[i].source:
        continue
    nb.cells[i].source = ""

# Finally plot the results
nb.cells[-2].source = """df = aggregate(CSV_SOLVER)
print(df)
plot_size_vs_time(df, SVG_SOLVER, logscale=False)"""

with open(nb_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
print("Notebook updated successfully.")
