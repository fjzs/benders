import numpy as np


class Problem:
    def __init__(
        self,
        warehouses: int,
        customers: int,
        fixed_cost: np.ndarray,
        shipping_cost: np.ndarray,
        demand: np.ndarray,
        capacity: np.ndarray,
    ):
        self.warehouses = warehouses
        self.customers = customers
        self.fixed_cost = fixed_cost
        self.shipping_cost = shipping_cost
        self.demand = demand
        self.capacity = capacity
