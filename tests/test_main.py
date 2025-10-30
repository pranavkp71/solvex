from fastapi.testclient import TestClient
from solvex.main import app

client = TestClient(app)

def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json()["title"] == "Solvex"
    assert response.json()["description"] == "Solve linear programming problems easily via API"
    assert response.json()["version"] == "0.0.1"

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["services"] == "Solvex" 

def test_solve_lp_success():
    problem = {
        "objective": [3, 5],
        "constraints_matrix": [[2, 3], [1, 2]],
        "constraints_limits": [20, 10],
        "bounds": [[0, None], [0, None]]
    }
    response = client.post("/solve/lp", json=problem)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert len(data["solution"]) == 2
    assert data["optimal_value"] > 0

def test_solve_lp_fail():
    problem = {
        "objective": [1, 1],
        "constraints_matrix": [[1, 0], [-1, 0]],
        "constraints_limits": [1, -2],
        "bounds": [[0, None], [0, None]]
    }
    response = client.post("/solve/lp", json=problem)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == False
    



