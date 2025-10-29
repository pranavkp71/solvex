from fastapi import FastAPI, HTTPException
from scipy.optimize import linprog
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title='Solvex',
    version='0.0.1',
    description="Solve linear programming problems easily via API"
)

class LPProblem(BaseModel):
    objective: list[float]
    constraints_matrix: list[list[float]]
    constraints_limits: list[float]
    bounds: list[tuple[Optional[float], Optional[float]]]
    maximize: bool = True

class Solution(BaseModel):
    success: True
    solution: Optional[list[float]] = None
    optimal_value: Optional[float] = None
    message: str
    

@app.get("/")
def read_root():
    return {
        'service': 'Solvex',
        'description': "Solve linear programming problems easily via API",
        'version': '0.0.1'
    }

@app.get('/health')
def health():
    return {'status': 'healthy', 'services': 'Solvex'}

@app.post("/solve/lp")
def solve_lp(problem: LPProblem):
    """
    Solve a linear programming problem using the simple/highs method.

    The goal is to find the optimal values of varibales x_1, x_2, x_3, ........, x_n
    that either maximize or minimize a linear objective function:

        Maximize (or Minimize): c_1*x_1 + c_2*x_2 + c_3*x_3 + ......... + c_n*x_n

        (Here, 'c' represents the coefficients you want to optimize)

    The general constraint form is:

        a_11*x_1 + a_12*x_2 + a_13*x_3 + ....... + a_1n*x_n <= b_1
        a_21*x_1 + a_22*x_2 + a_33*x_3 + ....... + a_2n*x_n <= b_2
        .....
        and variable bounds (eg. x_1 >= 0).

    Example:
        Maximize Z = 3x_1 + 5x_2
        subject to:
            2x_1 + 3x_2 <= 20
            x_1 + 2x_2 <= 10
            x_1, x_2 >= 0
            

    """
    try:
        c = [-x for x in problem.objective] if problem.maximize else problem.objective
        
        result = linprog(
            c = c,
            A_ub = problem.constraints_matrix,
            b_ub = problem.constraints_limits,
            bounds = problem.bounds,
            methods = 'highs',
        )
        if result.success:
            optimal_value = -result.fun if problem.maximize else result.fun
            return {
                "success": True,
                "solution": [round(x, 6) for x in result.x],
                "optimal_value": [round(optimal_value, 6)],
                'message': 'Optimal solution found'
            }
        else:
            return {
                'success': False,
                'message': f"Optimization failed: {result.message}"
            }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
