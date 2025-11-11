from typing import Optional

from pydantic import BaseModel


class LPProblem(BaseModel):
    objective: list[float]
    constraints_matrix: list[list[float]]
    constraints_limits: list[float]
    bounds: list[tuple[Optional[float], Optional[float]]]
    maximize: bool = True


class LPSolution(BaseModel):
    success: bool
    solution: Optional[list[float]] = None
    optimal_value: Optional[float] = None
    message: str
