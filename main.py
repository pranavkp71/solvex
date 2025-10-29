from scipy.optimize import linprog
from fastapi import FastAPI
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
    try:
        c = [-x for x in problem.objective]
        
        result = linprog(
            c=c,
            A_ub=problem.constraints_matrix,
            b_ub=problem.constraints_limits,
            bounds=problem.bounds
        )
        if result.success:
            return {
                "success": True,
                "solution": [round(x, 4) for x in result.x],
                "optimal_value": [round(-result.fun, 4)],
                'message': 'Optimal solution found'
            }
        else:
            return {
                'success': False,
                'message': f"Optimization failed: {result.message}"
            }
    
    except Exception as e:
        return {
            'success': False,
            'message': f"Error: {str(e)}"
        }
