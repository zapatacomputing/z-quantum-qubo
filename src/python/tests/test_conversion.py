from openfermion import IsingOperator
from zquantum.qubo.conversions import convert_qubo_to_openfermion_ising, convert_openfermion_ising_to_qubo
import dimod

def test_qubo_openfermion_ising_conversion():
    qubo = dimod.BinaryQuadraticModel({0: 1, 1: 2, 2: 3}, {(0,0): 0.5, (0,1): 0.25, (0,2): -0.5}, 2.0, vartype=dimod.BINARY)

    ising = convert_qubo_to_openfermion_ising(qubo)
    new_qubo = convert_openfermion_ising_to_qubo(ising)
    assert qubo == new_qubo

# TODO: test case with tricky numerical operations.
def test_qubo_openfermion_ising_conversion():
    qubo = dimod.BinaryQuadraticModel({0: 1, 1: 2, 2: 3}, {(0,0): 0.5, (0,1): 0.25, (0,2): -0.5}, 2.0, vartype=dimod.BINARY)

    ising = convert_qubo_to_openfermion_ising(qubo)
    new_qubo = convert_openfermion_ising_to_qubo(ising)
    assert qubo == new_qubo
