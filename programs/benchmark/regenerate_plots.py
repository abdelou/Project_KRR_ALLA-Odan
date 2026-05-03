import matplotlib.pyplot as plt
import pandas as pd

sizes = [8, 10, 12, 14, 16]
gen_mean = [0.03, 0.15, 0.90, 5.20, 28.5]
solver_mean = [0.0007, 0.0010, 0.0016, 0.0015, 0.0012]

plt.rcParams.update({'font.size': 11})

# Generator Figure
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(sizes, gen_mean, 'o-', color='C0', label='Generator Runtime')
ax.set_yscale('log')
for s, m in zip(sizes, gen_mean):
    ax.annotate(str(s), xy=(s, m), xytext=(0, 5), textcoords='offset points', ha='center', fontsize=9)
ax.set_xlabel("Problem size (c = total cubes)")
ax.set_ylabel("Mean runtime (s, log-scale)")
ax.grid(True, which="both", linestyle=":", linewidth=0.5)
ax.legend()
fig.tight_layout()
fig.savefig("gen_log.pdf", format="pdf")

# Solver Figure
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(sizes, solver_mean, 'o-', color='C1', label='Solver Runtime')
for s, m in zip(sizes, solver_mean):
    ax.annotate(str(s), xy=(s, m), xytext=(0, 5), textcoords='offset points', ha='center', fontsize=9)
ax.set_xlabel("Problem size (c = total cubes)")
ax.set_ylabel("Mean runtime (s)")
ax.grid(True, which="both", linestyle=":", linewidth=0.5)
ax.legend()
fig.tight_layout()
fig.savefig("solver_linear.pdf", format="pdf")
