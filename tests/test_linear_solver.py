from solvex.linear_solver import solve_lp
from solvex.models import LPProblem


def test_solve_lp_maximization():
    problem = LPProblem(
        objective=[3, 5],
        constraints_matrix=[[2, 3], [1, 5]],
        constraints_limits=[20, 10],
        bounds=[[0, None], [0, None]],
        maximize=True,
    )
    result = solve_lp(problem)

    assert result["success"] is True
    assert len(result["solution"]) == 2
    assert result["optimal_value"] > 0


def test_solve_lp_minimization():
    problem = LPProblem(
        objective=[4, 3],
        constraints_matrix=[[2, 3], [1, 2]],
        constraints_limits=[8, 8],
        bounds=[[0, None], [0, None]],
        maximize=False,
    )
    result = solve_lp(problem)

    assert result["success"] is True
    assert isinstance(result["solution"], list)
    assert result["optimal_value"] >= 0


def test_solve_lp_infeasible():
    problem = LPProblem(
        objective=[1, 1],
        constraints_matrix=[[1, 0], [-1, 0]],
        constraints_limits=[1, -2],
        bounds=[[0, None], [0, None]],
    )
    result = solve_lp(problem)

    assert result["success"] is False
    assert "failed" in result["message"].lower()
