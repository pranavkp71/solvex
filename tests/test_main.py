from fastapi.testclient import TestClient

from api.main import app
from solvex.models import LPSolution

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Solvex"
    assert data["version"] == "0.0.1"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["services"] == "Solvex"


def test_solve_lp_success():
    problem = {
        "objective": [3, 5],
        "constraints_matrix": [[2, 3], [1, 2]],
        "constraints_limits": [20, 10],
        "bounds": [[0, None], [0, None]],
        "maximize": True,
    }
    response = client.post("/solve/lp", json=problem)
    assert response.status_code == 200

    result = LPSolution(**response.json())

    assert result.success is True
    assert isinstance(result.solution, list)
    assert result.optimal_value > 0
    assert result.message == "Optimal solution found"


def test_infeasible_problem():
    problem = {
        "objective": [1, 1],
        "constraints_matrix": [[1, 0], [-1, 0]],
        "constraints_limits": [1, -2],
        "bounds": [[0, None], [0, None]],
    }
    response = client.post("/solve/lp", json=problem)
    assert response.status_code == 200

    result = LPSolution(**response.json())

    assert result.success is False
    assert "failed" in result.message.lower()


def test_invalid_payload():
    """Check Pydantic validation for missing fields."""
    invalid_data = {"objective": [1, 2]}
    response = client.post("/solve/lp", json=invalid_data)
    assert response.status_code == 422
