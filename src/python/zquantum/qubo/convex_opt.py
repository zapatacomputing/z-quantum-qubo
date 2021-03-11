import dimod
import numpy as np
import cvxpy as cp
from zquantum.core.interfaces.optimizer import Optimizer
from scipy.optimize import LinearConstraint


def solve_qp_relaxation_of_qubo(
    qubo: dimod.BQM, optimizer: Optimizer, number_of_trials: int = 1
) -> (np.ndarray, float):
    qubo_matrix = qubo.to_numpy_matrix().astype(float)
    if is_matrix_semi_positive_definite(qubo_matrix):
        return solve_qp_relaxation_of_spd_qubo(qubo)
    else:
        return solve_qp_relaxation_of_non_spd_qubo(qubo, optimizer, number_of_trials)


def solve_qp_relaxation_of_spd_qubo(qubo: dimod.BQM) -> (np.ndarray, float):
    if qubo.vartype != dimod.BINARY:
        raise TypeError("Qubo needs to have vartype BINARY.")

    qubo_matrix = qubo.to_numpy_matrix().astype(float)
    qubo_matrix = (qubo_matrix + qubo_matrix.T) / 2

    size = len(qubo.variables)
    P = qubo_matrix
    G = np.vstack([np.eye(size), -np.eye(size)])
    h = np.hstack([np.ones(size), np.zeros(size)])

    x = cp.Variable(size)
    problem = cp.Problem(cp.Minimize((1 / 2) * cp.quad_form(x, P)), [G @ x <= h])

    problem.solve()
    return x.value, problem.value


def solve_qp_relaxation_of_non_spd_qubo(
    qubo: dimod.BQM, optimizer: Optimizer, number_of_trials: int = 1
) -> (np.ndarray, float):
    # Use an optimizer to solve non-convex QP relaxations
    if not hasattr(optimizer, "constraints"):
        raise ValueError("Optimizer needs to support constraints.")
    size = len(qubo.variables)
    A = np.eye(size)
    lower_bound = np.zeros(size)
    upper_bound = np.ones(size)
    linear_constraint = LinearConstraint(A, lower_bound, upper_bound)

    optimizer.constraints = linear_constraint

    qubo_matrix = qubo.to_numpy_matrix().astype(float)

    cost_function = lambda x: x.T @ qubo_matrix @ x
    final_value = None
    final_params = None

    for _ in range(number_of_trials):
        initial_params = np.random.uniform(0.0, 1.0, size=size)
        optimization_results = optimizer.minimize(
            cost_function, initial_params, constraints=[linear_constraint]
        )
        if final_value is None or final_value < optimization_results.opt_value:
            final_value = optimization_results.opt_value
            final_params = optimization_results.opt_params

    return final_params, final_value


def is_matrix_semi_positive_definite(
    matrix: np.ndarray, epsilon: float = 1e-15
) -> bool:
    eigenvalues, _ = np.linalg.eig(matrix)
    return np.min(eigenvalues) >= epsilon


def regularize_relaxed_solution(
    relaxed_solution: np.ndarray, epsilon: int = 0.5
) -> np.ndarray:
    regularized_solution = []
    for value in relaxed_solution:
        if value > epsilon and value < 1 - epsilon:
            regularized_value = 2 * np.arcsin(np.sqrt(value))
        elif value <= epsilon:
            regularized_value = 2 * np.arcsin(np.sqrt(epsilon))
        else:
            regularized_value = 2 * np.arcsin(np.sqrt(1 - epsilon))
        regularized_solution.append(regularized_value)
    return np.array(regularized_solution)