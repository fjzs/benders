from business.problem import Problem
from solver.master import MasterProblem
from solver.solver import Solver
from solver.subproblem import SubProblem


class BendersCoordinator(Solver):

    def __init__(self, problem: Problem):
        self.problem = problem
        self.master = MasterProblem(problem)
        self.subproblem = SubProblem(problem)

    def solve(self):
        # Solve the master problem
        self.master.solve()

    def get_solution_flow(self):
        return None

    def get_solution_warehouses(self):
        return None
