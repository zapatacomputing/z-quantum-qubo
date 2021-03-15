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
    solve_qp_problem_for_spd_matrix,
    solve_qp_problem_with_optimizer,
)


def solve_relaxed_qubo(
    qubo,
    epsilon=0.5,
    optimizer_specs=None,
    number_of_trials=10,
    symmetrize_matrix=True,
):
    qubo = load_qubo(qubo)

    qubo_matrix = qubo.to_numpy_matrix().astype(float)
    if symmetrize_matrix:
        qubo_matrix = (qubo_matrix + qubo_matrix.T) / 2

    if is_matrix_semi_positive_definite(qubo_matrix):
        solution, optimal_value = solve_qp_problem_for_spd_matrix(
            qubo_matrix, symmetrize_matrix
        )
    else:
        if optimizer_specs is None:
            raise ValueError(
                "For qubo with semipositive definite matrix, an optimizer must be provided."
            )
        optimizer = create_object(optimizer_specs)
        solution, optimal_value = solve_qp_problem_with_optimizer(
            qubo_matrix, optimizer, number_of_trials, symmetrize_matrix
        )

    save_list(solution.tolist(), "solution.json")
    save_value_estimate(ValueEstimate(optimal_value), "energy.json")
