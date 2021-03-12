from scipy.optimize import minimize, LinearConstraint
from zquantum.core.utils import (
    save_list,
    save_value_estimate,
    ValueEstimate,
    create_object,
)
from zquantum.qubo import load_qubo
from zquantum.qubo.convex_opt import (
    is_matrix_semi_positive_definite,
    solve_qp_relaxation_of_qubo,
    regularize_relaxed_solution,
)


def solve_relaxed_qubo(
    qubo,
    regularize_solution=False,
    epsilon=0.5,
    optimizer_specs=None,
    number_of_trials=10,
):
    qubo = load_qubo(qubo)
    optimizer = create_object(optimizer_specs)
    solution, optimal_value = solve_qp_relaxation_of_qubo(
        qubo, optimizer, number_of_trials
    )

    if regularize_solution:
        solution = regularize_solution()

    save_list(solution.tolist(), "solution.json")
    save_value_estimate(ValueEstimate(optimal_value), "energy.json")
