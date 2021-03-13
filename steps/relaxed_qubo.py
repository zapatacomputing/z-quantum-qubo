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
    solve_qp_relaxation_of_spd_qubo,
    solve_qp_relaxation_of_non_spd_qubo,
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

    qubo_matrix = qubo.to_numpy_matrix().astype(float)
    if is_matrix_semi_positive_definite(qubo_matrix):
        solution, optimal_value = solve_qp_relaxation_of_spd_qubo(qubo)
    else:
        if optimizer_specs is None:
            raise ValueError(
                "For qubo with semipositive definite matrix, an optimizer must be provided."
            )
        optimizer = create_object(optimizer_specs)
        solution, optimal_value = solve_qp_relaxation_of_non_spd_qubo(
            qubo, optimizer, number_of_trials
        )

    if regularize_solution:
        solution = regularize_solution()

    save_list(solution.tolist(), "solution.json")
    save_value_estimate(ValueEstimate(optimal_value), "energy.json")
