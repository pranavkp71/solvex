"""
Resource Allocation Optimization with Solvex

Problem Statement:
A company needs to assign 3 workers to 3 tasks. Each worker has different
efficiency for each task (measured in hours to complete).

Goal: Minimize total hours while ensuring each task is completed by exactly one worker.

Assignment costs (hours):
         Task1  Task2  Task3
Worker1:   5      8      7
Worker2:   6      4      9
Worker3:   7      6      5

Real-World Application:
- Employee scheduling
- Project task assignment
- Resource management
- Workload balancing

Mathematical Formulation:
Minimize: 5*x11 + 8*x12 + 7*x13 + 6*x21 + 4*x22 + 9*x23 + 7*x31 + 6*x32 + 5*x33
Subject to:
  x11 + x12 + x13 = 1  (Worker 1 does exactly 1 task)
  x21 + x22 + x23 = 1  (Worker 2 does exactly 1 task)
  x31 + x32 + x33 = 1  (Worker 3 does exactly 1 task)
  x11 + x21 + x31 = 1  (Task 1 assigned to exactly 1 worker)
  x12 + x22 + x32 = 1  (Task 2 assigned to exactly 1 worker)
  x13 + x23 + x33 = 1  (Task 3 assigned to exactly 1 worker)
  All xij in {0, 1}

Note: This is simplified as LP (relaxed integer constraint).
For true assignment problem, use integer programming.

Example Usage:
  python examples/resource_allocation.py
"""

import requests

API_URL = "http://127.0.0.1:8000/solve/lp"

# Cost matrix (hours to complete)
workers = ["Worker 1", "Worker 2", "Worker 3"]
tasks = ["Task 1", "Task 2", "Task 3"]

cost_matrix = [
    [5, 8, 7],  # Worker 1's efficiency for each task
    [6, 4, 9],  # Worker 2's efficiency for each task
    [7, 6, 5]   # Worker 3's efficiency for each task
]

print("=" * 60)
print("RESOURCE ALLOCATION OPTIMIZATION")
print("=" * 60)

print("\nTime Required (hours):")
print(f"\n{'':12}", end="")
for task in tasks:
    print(f"{task:12}", end="")
print()

for i, worker in enumerate(workers):
    print(f"{worker:12}", end="")
    for j in range(len(tasks)):
        print(f"{cost_matrix[i][j]:12}", end="")
    print()

# Flatten cost matrix for objective
objective = [cost for row in cost_matrix for cost in row]

# Build constraints
n = len(workers)  # 3x3 problem

# Each worker does exactly one task
worker_constraints = []
for i in range(n):
    row = [0] * (n * n)
    for j in range(n):
        row[i * n + j] = 1
    worker_constraints.append(row)

# Each task assigned to exactly one worker
task_constraints = []
for j in range(n):
    row = [0] * (n * n)
    for i in range(n):
        row[i * n + j] = 1
    task_constraints.append(row)

constraints_matrix = worker_constraints + task_constraints
constraints_limits = [1] * (n + n)  # All equal to 1

# Variable bounds (0 to 1 for LP relaxation)
bounds = [[0, 1]] * (n * n)

problem = {
    "objective": objective,
    "constraints_matrix": constraints_matrix,
    "constraints_limits": constraints_limits,
    "bounds": bounds
}

print("\n" + "-" * 60)
print("Solving optimization problem...")
print("-" * 60)

try:
    response = requests.post(API_URL, json=problem)
    response.raise_for_status()
    result = response.json()
    
    if result["success"]:
        print("\n✓ OPTIMAL ASSIGNMENT FOUND!\n")
        
        solution = result["solution"]
        total_hours = result["optimal_value"]
        
        print("Assignment Plan:")
        for i in range(n):
            for j in range(n):
                idx = i * n + j
                if solution[idx] > 0.5:  # If assigned (>0.5 for LP relaxation)
                    print(f"  {workers[i]} → {tasks[j]} ({cost_matrix[i][j]} hours)")
        
        print(f"\n{'─' * 60}")
        print(f"Total Time: {total_hours:.2f} hours")
        print(f"{'─' * 60}")
        
    else:
        print(f"\n✗ Optimization failed: {result.get('message', 'Unknown error')}")
        
except requests.exceptions.ConnectionError:
    print("\n✗ ERROR: Cannot connect to Solvex API")
    print("Make sure the server is running: uvicorn main:app --reload")
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")

print("\n" + "=" * 60)