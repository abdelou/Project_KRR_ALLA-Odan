import clingo
import secrets
import time
from pathlib import Path
import json

c_values = [8, 9, 10, 11, 12, 13, 14, 15]

gen_times = []
solve_times = []
valid_sizes = []

def run_gen(c):
    n = 4 if c <= 16 else 5
    m = max(1, c // 4)
    k = 2
    w = max(1, m - 1)
    
    facts = []
    def collect_model(model):
        facts.extend([str(atom) + "." for atom in model.symbols(atoms=True)])

    program = Path(__file__).parent / "../generator.lp"
    ctl = clingo.Control(["-c", f"c={c}", "-c", f"n={n}", "-c", f"m={m}", "-c", f"k={k}", "-c", f"w={w}", "--sign-def=rnd", f"--seed={secrets.randbelow(2**31)}"])
    ctl.load(str(program))
    
    start = time.perf_counter()
    ctl.ground([("base", [])])
    res = ctl.solve(on_model=collect_model)
    t = time.perf_counter() - start
    
    if res.satisfiable:
        return t, facts
    return None, None

def run_sol(facts):
    program = Path(__file__).parent / "../solver.lp"
    ctl = clingo.Control(["-t", "4"]) # Use 4 threads
    ctl.load(str(program))
    ctl.add("base", [], "\n".join(facts))
    
    start = time.perf_counter()
    ctl.ground([("base", [])])
    ctl.solve()
    t = time.perf_counter() - start
    return t

print("Running 3DSRP Benchmarks...")
for c in c_values:
    # Run 3 times and take average to smooth out noise
    gt_sum = 0
    st_sum = 0
    runs = 3
    success_runs = 0
    for _ in range(runs):
        print(f"Testing c={c} (run {_ + 1}/{runs})...")
        t_gen, facts = run_gen(c)
        if t_gen is not None:
            t_sol = run_sol(facts)
            gt_sum += t_gen
            st_sum += t_sol
            success_runs += 1
            
    if success_runs > 0:
        valid_sizes.append(c)
        gen_times.append(gt_sum / success_runs)
        solve_times.append(st_sum / success_runs)

results = {"sizes": valid_sizes, "gen": gen_times, "sol": solve_times}
print("Results:", results)

with open(Path(__file__).parent / "benchmark_real.json", "w") as f:
    json.dump(results, f)
