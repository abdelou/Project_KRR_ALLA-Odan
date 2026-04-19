import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

csv_path = Path("results/solver_3dsrp.csv")
svg_path = Path("results/solver_3dsrp.svg")

df = pd.read_csv(csv_path)
grp = df.groupby("size").agg(mean_seconds=("seconds", "mean")).reset_index()
grp.sort_values("size", inplace=True)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(grp["size"], grp["mean_seconds"], 'o-')

for _, row in grp.iterrows():
    ax.annotate(
        f"{int(row['size'])}",
        xy=(float(row["size"]), float(row["mean_seconds"])),
        textcoords="offset points",
        xytext=(0, 5),
        ha="center",
    )

ax.set_xlabel("Problem size (c = number of cubes)")
ax.set_ylabel("Mean runtime (s)")
ax.set_title("Clingo runtime vs. problem size (3DSRP)")
ax.grid(True, which="both", linestyle=":", linewidth=0.5)
fig.tight_layout()
fig.savefig(svg_path, format="svg")
print(f"Saved plot to {svg_path}")
