from dimod import generators, BinaryQuadraticModel, ExactSolver
from zquantum.qubo import save_qubo, load_qubo
from zquantum.core.measurement import Measurements
from zquantum.core.utils import SCHEMA_VERSION


def generate_random_qubo(size: int, seed: int = None):
    """Generates qubo with random parameters from a uniform distribution.
    Args:
        size: number of variables in qubo
        seed: seed used for RNG
    """
    qubo = generators.uniform(size, "BINARY", low=-1, high=1, seed=seed)
    save_qubo(qubo, "qubo.json")