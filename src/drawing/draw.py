import matplotlib.pyplot as plt
import numpy as np


def draw_map(warehouses: np.ndarray, customers: np.ndarray):
    """Draw the map with warehouses and customers"""
    assert len(warehouses.shape) == 2
    assert len(customers.shape) == 2

    # Extract x and y for each
    cust_x, cust_y = customers[:, 0], customers[:, 1]
    ware_x, ware_y = warehouses[:, 0], warehouses[:, 1]

    plt.figure(figsize=(8, 6))

    # Plot customers: blue circles
    plt.scatter(cust_x, cust_y, color="blue", marker="o", s=100, label="Customers")

    # Plot warehouses: red squares
    plt.scatter(ware_x, ware_y, color="red", marker="s", s=150, label="Warehouses")

    # Add titles and labels
    plt.title("Customers and Warehouses Map")
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")

    # Add legend
    plt.legend()
    plt.grid(True)
    plt.axis("equal")  # Keep aspect ratio square
    plt.show()
