from typing import Optional

import matplotlib.pyplot as plt
import numpy as np


def draw_map(
    warehouses: np.ndarray,
    customers: np.ndarray,
    flow: Optional[np.ndarray] = None,
    facilities: Optional[np.ndarray] = None,
):
    """Draw the map with warehouses and customers"""
    assert len(warehouses.shape) == 2
    assert len(customers.shape) == 2

    # Extract x and y for each
    cust_x, cust_y = customers[:, 0], customers[:, 1]
    ware_x, ware_y = warehouses[:, 0], warehouses[:, 1]

    plt.figure(figsize=(8, 6))

    # Plot customers: blue circles
    plt.scatter(cust_x, cust_y, color="blue", marker="o", s=50, label="Customers")

    # Plot warehouses: red squares
    selected = np.array([0] * len(warehouses))
    if facilities is not None:
        selected = facilities
    # Plot all warehouses with fill color red and no edge
    plt.scatter(
        ware_x,
        ware_y,
        color="red",
        marker="s",
        s=150,
        label="Warehouses",
        edgecolors="none",
    )
    # Overlay selected warehouses with no fill and a thick blue border
    plt.scatter(
        ware_x[selected],
        ware_y[selected],
        facecolors="none",
        edgecolors="black",
        marker="s",
        s=150,
        linewidths=4,
    )

    # Add titles and labels
    plt.title("Customers and Warehouses Map")
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")

    # Draw flows if they are provided
    if flow is not None:
        # Draw arcs with flow > 0
        for w_id in range(flow.shape[0]):
            for c_id in range(flow.shape[1]):
                f = flow[w_id, c_id]
                if f == 0:
                    continue  # skip zero flow

                x0, y0 = warehouses[w_id]
                x1, y1 = customers[c_id]

                plt.arrow(
                    x0,
                    y0,
                    x1 - x0,
                    y1 - y0,
                    length_includes_head=True,
                    head_width=0.1,
                    fc="black",
                    ec="black",
                    alpha=1,
                )

                # Label flow at midpoint
                # xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
                # plt.text(
                #     xm,
                #     ym,
                #     f"{f:.1f}",
                #     color="black",
                #     fontsize=10,
                #     ha="center",
                #     va="center",
                # )

    # Add legend
    plt.legend(loc="upper right", bbox_to_anchor=(1.05, 1), borderaxespad=0.0)
    plt.grid(True)
    ax = plt.gca()  # get current axes
    ax.set_axisbelow(True)  # put grid behind plot elements
    plt.axis("equal")  # Keep aspect ratio square
    plt.savefig("map.svg")
