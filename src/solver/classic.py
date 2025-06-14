import gurobipy as gp
import numpy as np
from gurobipy import GRB

from business.problem import Problem
from solver.solver import Solver


class FullModel(Solver):

    def __init__(self, problem: Problem):
        self.problem = problem
        self.model = gp.Model("network_design")
        # Variables
        self.x = self.__set_transportation_variable()
        self.y = self.__set_warehouse_opening_variable()
        # Objective function elements
        self.z_cost_transport = self.__set_cost_transport()
        self.z_cost_location = self.__set_cost_location()
        # Business constraints
        self.__constraint_satisfy_demand()
        self.__constraint_warehouse_capacity()
        # Objective constraints
        self.__constraint_cost_transport()
        self.__constraint_cost_location()
        # Objective function
        self.__set_objective_function()
        # Update the model in the end to add everything
        self.model.update()

        ## Now print the constraints
        # for c in self.model.getConstrs():
        #     print(f"{c.ConstrName}: {self.model.getRow(c)} {c.Sense} {c.RHS}")

    def solve(self):
        self.model.optimize()
        if self.model.Status == gp.GRB.INFEASIBLE:
            self.model.computeIIS()
            self.model.write("model.ilp")

    def __set_transportation_variable(self):
        var = self.model.addMVar(
            shape=(self.problem.get_num_warehouses(), self.problem.get_num_customers()),
            vtype=GRB.CONTINUOUS,
            lb=0,
            ub=np.inf,
            name="x",
        )
        return var

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

    def __constraint_satisfy_demand(self):
        """Every customer has to receive all the demand"""
        customers = self.problem.get_customer_ids()
        warehouses = self.problem.get_warehouse_ids()
        for j in customers:
            self.model.addConstr(
                sum(self.x[i, j] for i in warehouses) >= self.problem.demand[j],
                name=f"demand_{j}",
            )

    def __constraint_warehouse_capacity(self):
        """Each warehouse can send its capacity as maximum if its open"""
        customers = self.problem.get_customer_ids()
        warehouses = self.problem.get_warehouse_ids()
        for i in warehouses:
            self.model.addConstr(
                sum(self.x[i, j] for j in customers)
                <= self.y[i] * self.problem.capacity[i],
                f"capacity_{i}",
            )

    def __constraint_cost_transport(self):
        warehouses = self.problem.get_warehouse_ids()
        customers = self.problem.get_customer_ids()
        self.model.addConstr(
            self.z_cost_transport
            == gp.quicksum(
                self.x[i, j] * self.problem.shipping_cost[i, j]
                for i in warehouses
                for j in customers
            ),
            name="constraint_cost_transportation",
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

    def get_solution_flow(self) -> np.ndarray:
        """Gets the flow used in the solution

        Returns:
            np.ndarray: [Warehouses, Customers]
        """
        return np.array(self.x.X)

    def get_solution_warehouses(self) -> np.ndarray:
        """Gets the warehouses opened

        Returns:
            np.ndarray: [Warehouses]
        """
        return np.array(self.y.X).astype(bool)
