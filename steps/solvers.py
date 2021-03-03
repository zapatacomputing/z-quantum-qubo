import json
from zquantum.core.utils import create_object
from zquantum.qubo import load_qubo, save_sampleset
from zquantum.qubo.utils import evaluate_bitstring_for_qubo
from zquantum.core.measurement import Measurements
from zquantum.core.utils import ValueEstimate, save_value_estimate


def solve_qubo(qubo, solver_specs, solver_params=None):
    """Solves qubo using any sampler implementing either dimod.Sampler or zquantum.qubo.BQMSolver"""
    if solver_params is None:
        solver_params = {}
    solver = create_object(solver_specs)
    qubo = load_qubo(qubo)

    sampleset = solver.sample(qubo, **solver_params)
    best_sample_dict = sampleset.first.sample
    solution_bitstring = tuple(best_sample_dict[i] for i in sorted(best_sample_dict))
    lowest_energy = evaluate_bitstring_for_qubo(solution_bitstring, qubo)

    save_value_estimate(ValueEstimate(lowest_energy), "lowest-energy.json")
    Measurements([solution_bitstring]).save("solution.json")
    save_sampleset(sampleset, "sampleset.json")