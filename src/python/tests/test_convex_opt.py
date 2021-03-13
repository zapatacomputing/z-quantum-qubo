import pytest
import dimod
import numpy as np
import cvxpy
from zquantum.core.interfaces.mock_objects import MockOptimizer
from zquantum.qubo.convex_opt import (
    solve_qp_relaxation_of_spd_qubo,
    solve_qp_relaxation_of_non_spd_qubo,
    is_matrix_semi_positive_definite,
    regularize_relaxed_solution,
)


@pytest.fixture
def optimizer():
    optimizer = MockOptimizer()
    optimizer.constraints = None
    return optimizer


@pytest.fixture
def qubo(request):
    if request.param:
        return dimod.BinaryQuadraticModel(
            {0: 5, 1: 6, 2: 7},
            {(1, 2): 1, (1, 0): 2, (0, 2): 3},
            0,
            vartype=dimod.BINARY,
        )
    else:
        return dimod.BinaryQuadraticModel(
            {0: -10, 1: -12, 2: -14},
            {(1, 2): 1, (1, 0): 2, (0, 2): 3},
            0,
            vartype=dimod.BINARY,
        )


@pytest.mark.parametrize("qubo", [True], indirect=True)
def test_solve_qp_relaxation_of_spd_qubo(qubo):
    target_solution = np.array([0, 0, 0])
    solution, optimal_value = solve_qp_relaxation_of_spd_qubo(qubo)

    assert pytest.approx(optimal_value) == 0
    assert np.allclose(solution, target_solution)


@pytest.mark.parametrize("qubo", [False], indirect=True)
def test_solve_qp_relaxation_of_spd_qubo_fails_for_non_spd_matrix(qubo):
    target_solution = np.array([0, 0, 0])
    with pytest.raises(cvxpy.error.DCPError):
        solution, optimal_value = solve_qp_relaxation_of_spd_qubo(qubo)


def test_solve_qp_relaxation_of_non_spd_qubo(optimizer):
    qubo = dimod.BinaryQuadraticModel(
        {0: -10, 1: 2, 2: 3},
        {(1, 2): -1, (1, 0): 2, (0, 2): 3},
        0,
        vartype=dimod.BINARY,
    )
    solution, optimal_value = solve_qp_relaxation_of_non_spd_qubo(qubo, optimizer)

    assert isinstance(optimal_value, float)
    assert len(solution == 3)


def test_solve_qp_relaxation_of_non_spd_qubo_throws_error_when_optimizer_does_not_support_constraints():
    qubo = dimod.BinaryQuadraticModel(
        {0: -10, 1: 2, 2: 3},
        {(1, 2): -1, (1, 0): 2, (0, 2): 3},
        0,
        vartype=dimod.BINARY,
    )
    optimizer = MockOptimizer()
    with pytest.raises(ValueError):
        solution, optimal_value = solve_qp_relaxation_of_non_spd_qubo(qubo, optimizer)


@pytest.mark.parametrize(
    "matrix,expected",
    [(np.array([[1, 2], [1, 3]]), True), (np.array([[-100, 1], [1, 1]]), False)],
)
def test_is_matrix_semi_positive_definite(matrix, expected):
    assert is_matrix_semi_positive_definite(matrix) == expected


def test_regularize_relaxed_solution():
    relaxed_solution = np.array([0, 0.5, 1])
    epsilon = 0.1
    target_regularized_solution = np.array(
        [
            2 * np.arcsin(np.sqrt(epsilon)),
            2 * np.arcsin(np.sqrt(0.5)),
            2 * np.arcsin(np.sqrt(1 - epsilon)),
        ]
    )
    regularized_solution = regularize_relaxed_solution(relaxed_solution, epsilon=0.1)
    assert np.allclose(regularized_solution, target_regularized_solution)