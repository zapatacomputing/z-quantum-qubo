from dimod import generators, BinaryQuadraticModel, ExactSolver
from zquantum.qubo import save_qubo, load_qubo

def generate_random_qubo(size:int, seed:int=None):
    qubo = generators(size, 'BINARY', seed=seed)
    save_qubo(qubo, "qubo.json")


def get_exact_qubo_solution(qubo_json):
    qubo = load_qubo(qubo_json)
    sampleset = ExactSolver().sample_qubo(qubo)
    return sampleset