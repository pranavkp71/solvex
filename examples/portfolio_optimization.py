"""
Portfolio Optimization with Solvex

Problem Statement:
You have $10,000 to invest across 3 assets (stocks). Each asset has:
- Expected annual return (profit percentage)
- Some level of risk

Goal: Maximize expected returns while limiting risk exposure.

Constraints:
- Invest all ₹10,000
- No single asset should exceed 40% of portfolio (diversification)
- All allocations must be non-negative

Real-World Application:
- Investment management
- Retirement planning
- Fund allocation strategies
- Risk management

Mathematical Formulation:
Maximize: 0.12*x1 + 0.15*x2 + 0.10*x3
Subject to:
  x1 + x2 + x3 = 10000  (invest all money)
  x1 <= 4000             (max 40% in asset 1)
  x2 <= 4000             (max 40% in asset 2)
  x3 <= 4000             (max 40% in asset 3)
  x1, x2, x3 >= 0        (no negative investments)

Example Usage:
  python examples/portfolio_optimization.py
"""

import requests

# Configuration
API_URL = "http://127.0.0.1:8000/solve/lp"
BUDGET = 10000

# Assets data
assets = {
    "TMPV": {"return": 0.12, "name": "Tata Motors Passenger Vhcls Ltd."},
    "RELIANCE": {"return": 0.15, "name": "Reliance Industries Ltd."},
    "ADANIENT": {"return": 0.10, "name": "Adani Enterprises Ltd."}
}

print("=" * 60)
print("PORTFOLIO OPTIMIZATION")
print("=" * 60)
print(f"\nBudget: ${BUDGET:,}")
print("\nAssets:")
for symbol, data in assets.items():
    print(f"  {symbol:6} ({data['name']:20}) - Expected Return: {data['return']*100:.1f}%")

# Formulate the optimization problem
# We want to MAXIMIZE returns, so negate the objective for linprog (it minimizes)
objective = [assets[symbol]["return"] for symbol in assets.keys()]

# Constraints
constraints_matrix = [
    [1, 1, 1],        # Total investment = budget
    [1, 0, 0],        # Asset 1 <= 40% of budget
    [0, 1, 0],        # Asset 2 <= 40% of budget
    [0, 0, 1]         # Asset 3 <= 40% of budget
]

constraints_limits = [
    BUDGET,           # Total = ₹10,000
    BUDGET * 0.4,     # Max 40% = ₹4,000
    BUDGET * 0.4,
    BUDGET * 0.4
]

# Variable bounds (non-negative)
bounds = [[0, None], [0, None], [0, None]]

# Build request
problem = {
    "objective": objective,
    "constraints_matrix": constraints_matrix,
    "constraints_limits": constraints_limits,
    "bounds": bounds
}

print("\n" + "-" * 60)
print("Solving optimization problem...")
print("-" * 60)

# Send request to Solvex API
try:
    response = requests.post(API_URL, json=problem)
    response.raise_for_status()
    result = response.json()
    
    if result["success"]:
        print("\n✓ OPTIMAL SOLUTION FOUND.\n")
        
        solution = result["solution"]
        total_investment = sum(solution)
        expected_return = result["optimal_value"]
        
        print("Recommended Allocation:")
        for i, (symbol, data) in enumerate(assets.items()):
            amount = solution[i]
            percentage = (amount / BUDGET) * 100
            annual_return = amount * data["return"]
            
            print(f"\n  {symbol:6} ({data['name']:20})")
            print(f"    Amount:    ₹{amount:,.2f}")
            print(f"    Percentage: {percentage:.1f}%")
            print(f"    Annual Return: ₹{annual_return:,.2f}")
        
        print(f"\n{'─' * 60}")
        print(f"Total Investment:     ₹{total_investment:,.2f}")
        print(f"Expected Annual Return: ₹{expected_return:,.2f}")
        print(f"Return Rate:          {(expected_return/BUDGET)*100:.2f}%")
        print(f"{'─' * 60}")
        
    else:
        print(f"\n✗ Optimization failed: {result.get('message', 'Unknown error')}")
        
except requests.exceptions.ConnectionError:
    print("\n✗ ERROR: Cannot connect to Solvex API")
    print("Make sure the server is running: uvicorn main:app --reload")
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")

print("\n" + "=" * 60)