################################################################################
# © Copyright 2020-2021 Zapata Computing Inc.
################################################################################
from dimod import BinaryQuadraticModel, ExactSolver, generators
from zquantum.core.measurement import Measurements
from zquantum.core.openfermion import load_ising_operator, save_ising_operator
from zquantum.core.utils import SCHEMA_VERSION
from zquantum.qubo import (
    convert_measurements_to_sampleset as _convert_measurements_to_sampleset,
)
from zquantum.qubo import (
    convert_openfermion_ising_to_qubo,
    convert_qubo_to_openfermion_ising,
    load_qubo,
    save_qubo,
    save_sampleset,
)


def generate_random_qubo(size: int, seed: int = None):
    """Generates qubo with random parameters from a uniform distribution.
    Args:
        size: number of variables in qubo
        seed: seed used for RNG
    """
    qubo = generators.uniform(size, "BINARY", low=-1, high=1, seed=seed)
    save_qubo(qubo, "qubo.json")


def qubo_to_ising_hamiltonian(qubo):
    """Converts qubo to Ising Hamiltonian.
    Args:
        qubo: qubo stored as a json
    """
    qubo = load_qubo(qubo)
    hamiltonian = convert_qubo_to_openfermion_ising(qubo)
    save_ising_operator(hamiltonian, "hamiltonian.json")


def ising_hamiltonian_to_qubo(hamiltonian):
    """Converts Ising Hamiltonian to qubo.
    Args:
        hamiltonian: hamiltonian stored as a json
    """
    hamiltonian = load_ising_operator(hamiltonian)
    qubo = convert_openfermion_ising_to_qubo(hamiltonian)
    save_qubo(qubo, "qubo.json")


def convert_measurements_to_sampleset(
    measurements, qubo, change_bitstring_convention=False
):
    qubo = load_qubo(qubo)
    measurements = Measurements.load_from_file(measurements)
    sampleset = _convert_measurements_to_sampleset(
        measurements, qubo, change_bitstring_convention
    )
    save_sampleset(sampleset.aggregate(), "sampleset.json")
