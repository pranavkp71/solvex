# Solvex Optimization as a Service 

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

⭐ **If you find Solvex useful, give it a star!** ⭐

Solvex is a lightweight REST API that solves Linear Programming problems using SciPy — making optimization accessible to any application, in any language.

---

## Why Solvex?

**Solvex is different:**
- Simple REST API — just send JSON
- No optimization expertise needed
- Works with any programming language
- Production-ready from day one

---

## Features

- Solve Linear Programming problems in seconds  
- Clean, RESTful API design  
- Interactive docs with Swagger (`/docs`)  
- Easy JSON input and output  
- Built with production-ready FastAPI + SciPy  
- Extensible architecture for future optimization methods

---

## Quick Start

### 1. Installation
```bash
git clone https://github.com/pranavkp71/solvex.git
cd solvex
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Server
```bash
cd solvex
uvicorn main:app --reload
```

**Visit your API docs at:**  

  http://127.0.0.1:8000/docs  
  http://127.0.0.1:8000/redoc (ReDoc)

---

## Examples

Check out the [`examples/`](examples/) folder for real-world use cases:
- Portfolio optimization
- Production planning  
- Resource allocation
- Transportation problems

---

## API Usage

### POST `/solve/lp`

Solve a linear programming problem via JSON input.

#### Example Problem

**Maximize:** `Z = 3x + 5y`

**Subject to:**
- `2x + 3y ≤ 20` (Budget constraint)
- `x + 2y ≤ 10` (Time constraint)  
- `x, y ≥ 0` (Non-negativity)

#### cURL Request
```bash
curl -X POST http://127.0.0.1:8000/solve/lp \
  -H "Content-Type: application/json" \
  -d '{
    "objective": [3, 5],
    "constraints_matrix": [[2, 3], [1, 2]],
    "constraints_limits": [20, 10],
    "bounds": [[0, null], [0, null]]
  }'
```

#### Python Example
```python
import requests

problem = {
    "objective": [3, 5],
    "constraints_matrix": [[2, 3], [1, 2]],
    "constraints_limits": [20, 10],
    "bounds": [[0, None], [0, None]]
}

response = requests.post(
    "http://127.0.0.1:8000/solve/lp",
    json=problem
)

result = response.json()
print(f"Optimal solution: x={result['solution'][0]:.2f}, y={result['solution'][1]:.2f}")
print(f"Maximum value: {result['optimal_value']:.2f}")
```

#### Example Response
```json
{
  "success": true,
  "solution": [10.0, 0.0],
  "optimal_value": 30.0,
  "message": "Optimal solution found"
}
```

---

## Use Cases

- **Portfolio optimization** — maximize returns under risk constraints
- **Production planning** — balance costs and output
- **Transportation & logistics** — minimize delivery costs
- **Resource allocation** — assign workloads optimally
- **Scheduling** — optimize time and availability

---

## Tech Stack

| Component | Purpose |
|-----------|---------|
| **FastAPI** | High-performance Python web framework |
| **SciPy** | Optimization and scientific computation |
| **Pydantic** | Data validation and type safety |
| **Uvicorn** | ASGI web server |

---

## Roadmap

- [ ] Support for nonlinear and integer programming
- [ ] Add Knapsack and Assignment solvers
- [ ] Python SDK for developers (`pip install solvex`)
- [ ] Web Playground UI for visual problem solving
- [ ] PostgreSQL integration for problem history
- [ ] Batch processing for multiple problems
- [ ] Authentication and API tokens

---

## Contributing

Contributions are always welcome. If you find a bug or want to add a feature:

1. Fork the repo
2. Create a new branch for your changes
3. Make your changes
4. Format your code using Black:
   ```bash
   black .
   ```
5. Check for style issues with Flake8:
   ```bash
   flake8 .
   ```
6. Run tests:
   ```bash
   pytest
   ```
7. Commit your changes and push to your branch
8. Sumbit a pull request 

---

## Getting Help

- Check the [API Documentation](http://127.0.0.1:8000/docs)
- Found a bug? [Open an issue](https://github.com/pranavkp71/solvex/issues)
- Have questions? [Start a discussion](https://github.com/pranavkp71/solvex/discussions)
- Email: pranavkp170@gmail.com

---

## License

MIT License — see [LICENSE](LICENSE) file for details.

Free and open source. Use it, modify it, share it


