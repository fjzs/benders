from abc import ABC, abstractmethod

import numpy as np

from business.problem import Problem


class Solver(ABC):
    @abstractmethod
    def solve(self):
        pass

    @abstractmethod
    def get_solution_flow(self) -> np.ndarray:
        """Gets the flow used in the solution

        Returns:
            np.ndarray: [Warehouses, Customers]
        """
        pass

    @abstractmethod
    def get_solution_warehouses(self) -> np.ndarray:
        """Gets the warehouses opened

        Returns:
            np.ndarray: [Warehouses]
        """
        pass
