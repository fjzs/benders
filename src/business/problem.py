import numpy as np


class Problem:
    def __init__(
        self,
        warehouses_location: np.ndarray,  # (m,2) locations
        customers_location: np.ndarray,  # (n,2) location
        fixed_cost: np.ndarray,  # (m,)
        shipping_cost: np.ndarray,  # (m,n)
        demand: np.ndarray,  # (n,)
        capacity: np.ndarray,  # (m,)
    ):
        self.warehouses_location = warehouses_location
        self.customers_location = customers_location
        self.fixed_cost = fixed_cost
        self.shipping_cost = shipping_cost
        self.demand = demand
        self.capacity = capacity

    def get_num_warehouses(self) -> int:
        return len(self.warehouses_location)

    def get_num_customers(self) -> int:
        return len(self.customers_location)

    def get_warehouse_ids(self) -> list[int]:
        return [i for i in range(len(self.warehouses_location))]

    def get_customer_ids(self) -> list[int]:
        return [i for i in range(len(self.customers_location))]

    def print(self):
        print(f"warehouses_location:\n{self.warehouses_location}")
        print(f"customers_location:\n{self.customers_location}")
        print(f"fixed_cost:\n{self.fixed_cost}")
        print(f"shipping_cost:\n{self.shipping_cost}")
        print(f"demand:\n{self.demand}")
        print(f"capacity:\n{self.capacity}")
