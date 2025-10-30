"""
Production Planning Optimization with Solvex

Problem Statement:
A factory produces two products: Product A and Product B.
- Product A: ₹240 profit per unit, requires 2 hours labor + 1 kg material
- Product B: ₹400 profit per unit, requires 3 hours labor + 2 kg material

Resources available:
- 20 hours of labor per day
- 10 kg of material per day

Goal: Maximize daily profit by determining how many of each product to make.

Real-World Application:
- Manufacturing optimization
- Factory scheduling
- Capacity planning
- Supply chain management

Mathematical Formulation:
Maximize: 3*A + 5*B (profit)
Subject to:
  2*A + 3*B <= 20  (labor hours)
  1*A + 2*B <= 10  (material kg)
  A, B >= 0        (can't produce negative)

Example Usage:
  python examples/production_planning.py
"""

import requests

API_URL = "http://127.0.0.1:8000/solve/lp"

# Products data
products = {
    "A": {"profit": 240, "labor_hours": 2, "material_kg": 1, "name": "Product A"},
    "B": {"profit": 400, "labor_hours": 3, "material_kg": 2, "name": "Product B"},
}

# Available resources
resources = {"labor_hours": 20, "material_kg": 10}

print("=" * 60)
print("PRODUCTION PLANNING OPTIMIZATION")
print("=" * 60)

print("\nProducts:")
for name, data in products.items():
    print(f"  {data['name']}:")
    print(f"    Profit: ₹{data['profit']} per unit")
    print(f"    Labor: {data['labor_hours']} hours per unit")
    print(f"    Material: {data['material_kg']} kg per unit")

print("\nAvailable Resources:")
for resource, amount in resources.items():
    print(f"  {resource.replace('_', ' ').title()}: {amount}")

# Formulate problem
objective = [products["A"]["profit"], products["B"]["profit"]]

constraints_matrix = [
    [products["A"]["labor_hours"], products["B"]["labor_hours"]],  # Labor
    [products["A"]["material_kg"], products["B"]["material_kg"]],  # Material
]

constraints_limits = [resources["labor_hours"], resources["material_kg"]]

bounds = [[0, None], [0, None]]

problem = {
    "objective": objective,
    "constraints_matrix": constraints_matrix,
    "constraints_limits": constraints_limits,
    "bounds": bounds,
}

print("\n" + "-" * 60)
print("Solving optimization problem...")
print("-" * 60)

try:
    response = requests.post(API_URL, json=problem)
    response.raise_for_status()
    result = response.json()

    if result["success"]:
        print("\n✓ OPTIMAL PRODUCTION PLAN FOUND.\n")

        product_a_qty = result["solution"][0]
        product_b_qty = result["solution"][1]
        max_profit = result["optimal_value"]

        print("Production Schedule:")
        print(f"  Product A: {product_a_qty:.2f} units")
        print(f"  Product B: {product_b_qty:.2f} units")

        print("\nResource Usage:")
        labor_used = (
            product_a_qty * products["A"]["labor_hours"]
            + product_b_qty * products["B"]["labor_hours"]
        )
        material_used = (
            product_a_qty * products["A"]["material_kg"]
            + product_b_qty * products["B"]["material_kg"]
        )

        print(
            f"  Labor: {labor_used:.2f}/{resources['labor_hours']} hours "
            + f"({(labor_used/resources['labor_hours']*100):.1f}% utilized)"
        )
        print(
            f"  Material: {material_used:.2f}/{resources['material_kg']} kg "
            + f"({(material_used/resources['material_kg']*100):.1f}% utilized)"
        )

        print(f"\n{'─' * 60}")
        print(f"Maximum Daily Profit: ₹{max_profit:.2f}")
        print(f"{'─' * 60}")

    else:
        print(f"\n✗ Optimization failed: {result.get('message', 'Unknown error')}")

except requests.exceptions.ConnectionError:
    print("\n✗ ERROR: Cannot connect to Solvex API")
    print("Make sure the server is running: uvicorn main:app --reload")
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")

print("\n" + "=" * 60)
