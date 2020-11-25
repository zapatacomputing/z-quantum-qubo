import numpy as np
from openfermion import IsingOperator
from zquantum.qubo.conversions import convert_qubo_to_openfermion_ising, convert_openfermion_ising_to_qubo
import dimod


def test_qubo_with_binary_fractions():
    qubo = dimod.BinaryQuadraticModel(
        {0: 1, 1: 2, 2: 3},
        {(1, 2): 0.5, (1, 0): -0.25, (0, 2): 2.125},
        -1,
        vartype=dimod.BINARY
    )
    ising = convert_qubo_to_openfermion_ising(qubo)
    new_qubo = convert_openfermion_ising_to_qubo(ising)
    assert qubo == new_qubo


def test_qubo_with_non_binary_fractions():
    qubo = dimod.BinaryQuadraticModel(
        {0: 1.01, 1: -2.03, 2: 3},
        {(1, 2): 0.51, (1, 0): -0.9, (0, 2): 2.125},
        -1,
        vartype=dimod.BINARY
    )
    ising = convert_qubo_to_openfermion_ising(qubo)
    new_qubo = convert_openfermion_ising_to_qubo(ising)
    
    assert len(qubo.linear) == len(new_qubo.linear)
    assert len(qubo.quadratic) == len(new_qubo.quadratic)

    assert np.isclose(qubo.offset, new_qubo.offset)
    assert qubo.vartype == new_qubo.vartype

    for key in qubo.linear.keys():
        assert np.isclose(qubo.linear[key], new_qubo.linear[key])

    for key in qubo.quadratic.keys():
        assert np.isclose(qubo.quadratic[key], new_qubo.quadratic[key])


