from scipy.optimize import linprog
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title='Solvex',
    version='0.0.1',
    description="Your optimizer"
)

class LPProblem(BaseModel):
    objective: list[float]
    constraints_matrix: list[list[float]]
    constraints_limits: list[float]
    bounds: list[tuple]

@app.get("/")
def read_root():
    return {"message": "Welcome to SolveX"}

@app.post("/solve/lp")
def solve_lp(problem: LPProblem):
    c = [-x for x in problem.objective]
    
    result = linprog(
        c=c,
        A_ub=problem.constraints_matrix,
        b_ub=problem.constraints_limits,
        bounds=problem.bounds
    )
    
    return {
        "success": result.success,
        "solution": result.x.tolist() if result.success else None,
        "optimal_value": -result.fun if result.success else None
    }