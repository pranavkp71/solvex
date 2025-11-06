from fastapi import APIRouter, HTTPException

from solvex.linear_solver import solve_lp as lp_solver
from solvex.models import LPProblem

router = APIRouter(prefix="/solve", tags=["Linear Programming"])


@router.post("/lp")
def solve_lp(problem: LPProblem):
    try:
        return lp_solver(problem)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
