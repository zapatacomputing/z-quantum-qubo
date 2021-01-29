import yaml
from zquantum.core.utils import create_object
from zquantum.qubo import load_qubo


def solve_qubo(qubo, solver_specs, sample_params):
    """Solves qubo using any sampler implementing either dimod.Sampler or zquantum.qubo.BQMSolver"""
    solver_specs_dict = yaml.load(solver_specs, Loader=yaml.SafeLoader)["solver_specs"]
    sample_params_dict = yaml.load(sample_params, Loader=yaml.SafeLoader)[
        "sample_params"
    ]
    solver = create_object(solver_specs_dict)
    qubo = load_qubo(qubo)
    sampleset = solver.sample(qubo, **sample_params_dict)
    best_sample_dict = sampleset.first.sample
    solution_bitstring = tuple(best_sample_dict[i] for i in sorted(best_sample_dict))
    Measurements([solution_bitstring]).save("solution.json")
