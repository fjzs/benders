import gurobipy as gp
import numpy as np
from business.problem import Problem
from gurobipy import GRB


class MasterProblem:
    def __init__(self, problem: Problem):
        self.problem = problem
        self.model = gp.Model("master")
        # Variables
        self.y = self.__set_warehouse_opening_variable()
        # Objective function elements
        self.z_cost_transport = self.__set_cost_transport()
        self.z_cost_location = self.__set_cost_location()
        # Business Constraints
        self.__constraint_supply_gte_demand()
        # Objective constraints
        self.__constraint_cost_location()
        # Objective function
        self.__set_objective_function()
        # Update the model in the end to add everything
        self.model.update()

    def __set_warehouse_opening_variable(self):
        return self.model.addMVar(
            shape=self.problem.get_num_warehouses(), vtype=GRB.BINARY, name="y"
        )

    def __set_cost_transport(self):
        return self.model.addVar(
            vtype=GRB.CONTINUOUS, lb=0, ub=np.inf, name="cost_transport"
        )

    def __set_cost_location(self):
        return self.model.addVar(
            vtype=GRB.CONTINUOUS, lb=0, ub=np.inf, name="cost_location"
        )

    def __constraint_supply_gte_demand(self):
        """
        The supply must be greater than or equal than the demand:
        ∑{i ∈ M} y_i*cap_i >= ∑{j ∈ N} d_j
        """
        customers = self.problem.get_customer_ids()
        warehouses = self.problem.get_warehouse_ids()
        self.model.addConstr(
            gp.quicksum(
                self.y[i] * self.problem.capacity[i] for i in warehouses  # supply
            )
            >= np.sum(self.problem.demand),  # demand
            name="constraint_supply_gte_demand",
        )

    def __constraint_cost_location(self):
        warehouses = self.problem.get_warehouse_ids()
        self.model.addConstr(
            self.z_cost_location
            == gp.quicksum(self.y[i] * self.problem.fixed_cost[i] for i in warehouses),
            name="constraint_cost_location",
        )

    def __set_objective_function(self):
        self.model.setObjective(
            self.z_cost_location + self.z_cost_transport, GRB.MINIMIZE
        )

    def solve(self):
        self.model.optimize()
        if self.model.Status == GRB.INFEASIBLE:
            self.model.computeIIS()
            self.model.write("master_model.ilp")
