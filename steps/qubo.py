from dimod import generators, BinaryQuadraticModel, ExactSolver
from zquantum.qubo import save_qubo, load_qubo
from zquantum.core.measurement import Measurements


def generate_random_qubo(size:int, seed:int=None):
    qubo = generators.uniform(size, 'BINARY', low=-1, high=1, seed=seed)
    save_qubo(qubo, "qubo.json")


def get_exact_qubo_solution(qubo_json):
    qubo = load_qubo(qubo_json)
    sampleset = ExactSolver().sample(qubo)
    best_sample_dict = sampleset.first.sample
    solution_bitstring = tuple(best_sample_dict[i] for i in sorted(best_sample_dict))
    Measurements([solution_bitstring]).save("solution.json")