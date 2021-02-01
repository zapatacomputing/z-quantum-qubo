import yaml
from zquantum.core.utils import create_object
from zquantum.qubo import load_qubo
from zquantum.core.measurement import Measurements


def solve_qubo(qubo, solver_specs, sample_params):
    """Solves qubo using any sampler implementing either dimod.Sampler or zquantum.qubo.BQMSolver"""
    solver = create_object(solver_specs)
    qubo = load_qubo(qubo)
    sampleset = solver.sample(qubo, **sample_params)
    best_sample_dict = sampleset.first.sample
    solution_bitstring = tuple(best_sample_dict[i] for i in sorted(best_sample_dict))
    Measurements([solution_bitstring]).save("solution.json")
