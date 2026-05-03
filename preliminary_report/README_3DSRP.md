# 3D Symbolic Region Puzzle (3DSRP) - ASP Models

This directory contains the Answer Set Programming (ASP) models for the 3D-Symbolic Region Puzzle (3DSRP), compatible with Clingo, as described in the preliminary report.

## Files
- `generator.lp`: Clingo program to generate random puzzle instances subject to parameters $c, n, m, k, w$. Includes an embedded solver check to guarantee that generated instances are actually solvable.
- `solver.lp`: Clingo program to solve a given 3DSRP instance.

## Execution

Ensure you have [Clingo](https://potassco.org/clingo/) installed on your system.

### 1. Generating a Puzzle Instance
The generator accepts parameters representing the board constraints. For example, to generate a puzzle with 12 cubes, bounding box size 4, 3 regions, 2 symbol types, and 4 walls:
```bash
clingo generator.lp -c c=12 -c n=4 -c m=3 -c k=2 -c w=4 --sign-def=rnd --seed=42 -V0 0
```
*Note: Due to the NP nature of the problem, generating large instances may require significant configuration adjustments to the time limits depending on your machine.*

You can capture the output to a text file (an instance file):
```bash
clingo generator.lp -c c=12 -c n=4 -c m=3 -c k=2 -c w=4 --sign-def=rnd -V0 --outf=0 > instance.lp
```

### 2. Solving a Puzzle Instance
Once you have an instance (which contains `cube/3`, `symbol/4`, `wall/6`, `regions/1`, `symbol_type/1` facts), you can solve it by passing the instance and the solver to clingo:
```bash
clingo solver.lp instance.lp 0
```
Clingo will search for all valid regions satisfying all five rules (Coverage, Connectivity, Non-planarity, Symbol Completeness, Wall separation).

## Authors
- Abdelouahad Alla
- Odan Lafrance
