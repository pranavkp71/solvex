from fastapi import APIRouter, HTTPException
from solvex.models import LPProblem
from solvex.solvers import solve_lp as lp_solver

router = APIRouter(prefix="/solve", tags=["Linear Programming"])

@router.post("/lp")
def solve_lp(problem: LPProblem):
    try:
        return lp_solver(problem)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
