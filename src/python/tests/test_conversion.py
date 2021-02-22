import pytest
import numpy as np
from openfermion import IsingOperator
import dimod

from zquantum.qubo.conversions import (
    convert_qubo_to_openfermion_ising,
    convert_openfermion_ising_to_qubo,
    convert_sampleset_to_measurements,
    convert_measurements_to_sampleset,
)
from zquantum.core.measurement import Measurements


def test_qubo_with_binary_fractions():
    qubo = dimod.BinaryQuadraticModel(
        {0: 1, 1: 2, 2: 3},
        {(1, 2): 0.5, (1, 0): -0.25, (0, 2): 2.125},
        -1,
        vartype=dimod.BINARY,
    )
    ising = convert_qubo_to_openfermion_ising(qubo)
    new_qubo = convert_openfermion_ising_to_qubo(ising)
    assert qubo == new_qubo


def test_qubo_with_non_binary_fractions():
    qubo = dimod.BinaryQuadraticModel(
        {0: 1.01, 1: -2.03, 2: 3},
        {(1, 2): 0.51, (1, 0): -0.9, (0, 2): 2.125},
        -1,
        vartype=dimod.BINARY,
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

def test_convert_sampleset_to_measurements():
    bitstrings = [
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (0, 1, 1),
        (1, 0, 0),
        (1, 1, 0),
        (1, 1, 1),
        (1, 0, 1),
        (0, 0, 1),
    ]
    energies = [0 for i in range(len(bitstrings))]
    sampleset = dimod.SampleSet.from_samples(bitstrings, dimod.BINARY, energies)
    target_measurements = Measurements(bitstrings)
    converted_measurements = convert_sampleset_to_measurements(sampleset)

    assert converted_measurements.bitstrings == target_measurements.bitstrings


def test_convert_sampleset_to_measurements_fails_for_non_binary_vartype():
    bitstrings = [
        (0, 0, 0),
    ]
    energies = [0 for _ in range(len(bitstrings))]
    sampleset = dimod.SampleSet.from_samples(bitstrings, dimod.SPIN, energies)
    with pytest.raises(Exception):
        converted_measurements = convert_sampleset_to_measurements(sampleset)


def test_convert_sampleset_to_measurements_fails_for_non_int_variables():
    bitstrings = [
        (0, 0, 0),
    ]
    energies = [0 for _ in range(len(bitstrings))]
    sampleset = dimod.SampleSet.from_samples(bitstrings, dimod.SPIN, energies)
    sampleset = sampleset.relabel_variables({0: 0.0, 1: 0.1, 2: 0.2})
    with pytest.raises(Exception):
        converted_measurements = convert_sampleset_to_measurements(sampleset)


def test_convert_sampleset_to_measurements_fails_for_variables_from_wrong_range():
    bitstrings = [
        (0, 0, 0),
    ]
    energies = [0 for _ in range(len(bitstrings))]
    sampleset = dimod.SampleSet.from_samples(bitstrings, dimod.SPIN, energies)
    sampleset = sampleset.relabel_variables({0: 1, 1: 2, 2: 3})
    with pytest.raises(Exception):
        converted_measurements = convert_sampleset_to_measurements(sampleset)


def test_convert_measurements_to_sampleset_without_qubo():
    bitstrings = [
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (0, 1, 1),
        (1, 0, 0),
        (1, 1, 0),
        (1, 1, 1),
        (1, 0, 1),
        (0, 0, 1),
    ]
    measurements = Measurements(bitstrings)

    target_sampleset = dimod.SampleSet.from_samples(
        bitstrings, dimod.BINARY, [np.nan for _ in bitstrings]
    )
    converted_sampleset = convert_measurements_to_sampleset(measurements)

    # Since energies should be np.nans, using "==" will result in error
    for (target_record, converted_record) in zip(
        target_sampleset.record, converted_sampleset.record
    ):
        for target_element, converted_element in zip(target_record, converted_record):
            np.testing.assert_equal(target_element, converted_element)

    assert converted_sampleset.vartype == target_sampleset.vartype


def test_convert_measurements_to_sampleset_with_qubo():
    bitstrings = [
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (0, 1, 1),
        (1, 0, 0),
        (1, 1, 0),
        (1, 1, 1),
        (1, 0, 1),
        (0, 0, 1),
    ]
    qubo = dimod.BinaryQuadraticModel(
        {0: 1, 1: 2, 2: 3},
        {(1, 2): 0.5, (1, 0): -0.25, (0, 2): 2.125},
        0,
        vartype=dimod.BINARY,
    )
    energies = [0, 3, 2, 5.5, 1, 2.75, 8.375, 6.125, 3]
    measurements = Measurements(bitstrings)

    target_sampleset = dimod.SampleSet.from_samples(bitstrings, dimod.BINARY, energies)
    converted_sampleset = convert_measurements_to_sampleset(measurements, qubo)
    assert target_sampleset == converted_sampleset