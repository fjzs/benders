import numpy as np

from business.problem import Problem
from drawing.draw import draw_map
from solver.classic import FullModel


def main():
    print("Starting...")

    # Build and draw problem 1
    problem = build_problem_0()
    problem.print()
    draw_map(problem.warehouses_location, problem.customers_location)

    # Solve with classic method
    fullModel = FullModel(problem)
    fullModel.solve()


def build_problem_0():
    warehouses = np.array([[0, 0]])
    customers = np.array([[1, 0], [0, 1]])
    fixed_costs = np.array([10])
    shipping_cost = np.zeros((len(warehouses), len(customers)))
    for i in range(len(warehouses)):
        wi = warehouses[i]
        for j in range(len(customers)):
            cj = customers[j]
            shipping_cost[i, j] = np.round(np.sqrt(np.sum((wi - cj) ** 2)), decimals=1)
    demand = np.arange(1, len(customers) + 1)
    capacity = np.ones(len(warehouses)) * ((np.sum(demand) / len(warehouses)) + 1)
    # Create the problem instance
    return Problem(
        warehouses_location=warehouses,
        customers_location=customers,
        fixed_cost=fixed_costs,
        shipping_cost=shipping_cost,
        demand=demand,
        capacity=capacity,
    )


def build_problem_1():
    warehouses = np.array([[0, 0], [2, 2], [4, 4]])
    customers = np.array([[1, 0], [0, 1], [1, 3], [3, 1], [5, 2], [2, 5]])
    fixed_costs = np.array([1, 1, 1])
    shipping_cost = np.zeros((len(warehouses), len(customers)))
    for i in range(len(warehouses)):
        wi = warehouses[i]
        for j in range(len(customers)):
            cj = customers[j]
            shipping_cost[i, j] = np.round(np.sqrt(np.sum((wi - cj) ** 2)), decimals=1)
    demand = np.arange(1, len(customers) + 1)
    capacity = np.ones(len(warehouses)) * ((np.sum(demand) / len(warehouses)) + 1)

    # Create the problem instance
    return Problem(
        warehouses_location=warehouses,
        customers_location=customers,
        fixed_cost=fixed_costs,
        shipping_cost=shipping_cost,
        demand=demand,
        capacity=capacity,
    )


if __name__ == "__main__":
    main()
