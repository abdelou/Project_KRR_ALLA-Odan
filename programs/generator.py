import clingo
import secrets
import time
from pathlib import Path

facts = []

def collect_model(model):
    global facts
    facts = [str(atom) + "." for atom in model.symbols(atoms=True)]

def print_model(model):
    model_str = [str(atom) for atom in model.symbols(atoms=True)]
    print(" ".join(model_str))

def run_generator(c, n, m, k, w, print_out=False):
    global facts
    facts = []
    program = Path(__file__).parent / "generator.lp"
    
    ctl = clingo.Control(["-c", f"c={c}", "-c", f"n={n}", "-c", f"m={m}", "-c", f"k={k}", "-c", f"w={w}", "--sign-def=rnd", f"--seed={secrets.randbelow(2**31)}", "-V0", "0"])
    ctl.load(str(program))
    ctl.ground([("base", [])])
    
    if print_out:
        res = ctl.solve(on_model=print_model)
    else:
        res = ctl.solve(on_model=collect_model)
    
    if res.satisfiable:
        return True
    return False

def run_solver(print_out=False):
    global facts
    program = Path(__file__).parent / "solver.lp"
    
    ctl = clingo.Control(["-t", "11"])
    ctl.load(str(program))
    # We feed the generated facts to the solver
    ctl.add("base", [], "\\n".join(facts))
    ctl.ground([("base", [])])
    
    start = time.perf_counter()
    if print_out:
        ctl.solve(on_model=print_model)
    else:
        ctl.solve()
    return time.perf_counter() - start

def gen_and_solve(c, n, m, k, w):
    run_generator(c, n, m, k, w)
    return run_solver()
