from src.business.problem import Problem
from src.solver.master import MasterProblem
from src.solver.subproblem import SubProblem


class BendersCoordinator:

    def __init__(self, problem: Problem):
        self.problem = problem
        self.master = MasterProblem(problem)
        self.subproblem = SubProblem(problem)

    def solve(self):

        self.master.solve()

    def get_solution_flow(self):
        return None

    def get_solution_warehouses(self):
        return None
