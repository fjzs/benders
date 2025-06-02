import gurobipy as gp
import numpy as np
from gurobipy import GRB

from business.problem import Problem


def solve(problem: Problem):
    model = __build_model(problem)


def __build_model(problem: Problem):
    model = gp.Model("network_design")
    num_warehouses = len(problem.warehouses)
    num_customers = len(problem.customers)

    # Variables
    x = model.addMVar(
        shape=(num_warehouses, num_customers),
        vtype=GRB.CONTINUOUS,
        lb=0,
        ub=9999,
        name="x",
    )
    y = model.addMVar(shape=(num_warehouses), vtype=GRB.BINARY, name="y")

    # Constraints
    __constraint_satisfy_demand(problem, x, model)
    __constraint_capacity(problem, x, y, model)

    # Objective function
    __set_objective_function(problem, x, y, model)


def __constraint_satisfy_demand(problem: Problem, x: gp.MVar, model: gp.Model):
    """Every customer has to receive all the demand

    Args:
        problem (Problem):
        x (gp.Var):
        model (gp.Model):
    """
    customers = range(len(problem.customers))
    warehouses = range(len(problem.warehouses))

    for j in customers:
        model.addConstr(
            sum(x[i, j] for i in warehouses) >= problem.demand[j], f"demand_{j}"
        )


def __constraint_capacity(problem: Problem, x: gp.MVar, y: gp.MVar, model: gp.Model):
    """Each warehouse can send a maximum if its open

    Args:
        problem (Problem): _description_
        x (gp.MVar): _description_
        y (gp.MVar): _description_
        model (gp.Model): _description_
    """
    customers = range(len(problem.customers))
    warehouses = range(len(problem.warehouses))

    for i in warehouses:
        model.addConstr(
            sum(x[i, j] for j in customers) <= y[i] * problem.capacity[i],
            f"capacity_{i}",
        )
