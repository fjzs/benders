import numpy as np


class Problem:
    def __init__(
        self,
        warehouses: np.ndarray,  # (m,2) locations
        customers: np.ndarray,  # (n,2) location
        fixed_cost: np.ndarray,  # (m,)
        shipping_cost: np.ndarray,  # (m,n)
        demand: np.ndarray,  # (n,)
        capacity: np.ndarray,  # (m,)
    ):
        self.warehouses = warehouses
        self.customers = customers
        self.fixed_cost = fixed_cost
        self.shipping_cost = shipping_cost
        self.demand = demand
        self.capacity = capacity
