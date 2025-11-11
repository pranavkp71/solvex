from fastapi import APIRouter, HTTPException

from solvex.linear_solver import solve_lp as lp_solver
from solvex.models import LPProblem, LPSolution

router = APIRouter(prefix="/solve", tags=["Linear Programming"])


@router.post("/lp", response_model=LPSolution)
def solve_lp(problem: LPProblem):
    try:
        result = lp_solver(problem)
        return LPSolution(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
