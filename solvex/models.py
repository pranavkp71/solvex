from pydantic import BaseModel
from typing import Optional

class LPProblem(BaseModel):
    objective: list[float]
    constraints_matrix: list[list[float]]
    constraints_limits: list[float]
    bounds: list[tuple[Optional[float], Optional[float]]]
    maximize: bool = True

class Solution(BaseModel):
    success: bool
    solution: Optional[list[float]] = None
    optimal_value: Optional[float] = None
    message: str
