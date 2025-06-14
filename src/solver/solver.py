from abc import ABC, abstractmethod

from business.problem import Problem


class Solver(ABC):
    @abstractmethod
    def solve(self):
        pass
