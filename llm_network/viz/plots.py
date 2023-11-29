# %%

import matplotlib.pyplot as plt
import numpy as np
import json


# %%
def plot_3d(x, y, Z, ax):
    """
    Plot a 3d surface

    :param x: x coordinates
    :param y: y coordinates
    :param z: z coordinates
    :param ax: axis
    """
    X, Y = np.meshgrid(x, y)
    Z = row_normalization(Z)
    ax.plot_surface(X, Y, Z, cmap="viridis")
    ax.set_xlabel("Actual status")
    ax.set_ylabel("Estimated status")
    ax.set_zlabel("Probability")
    ax.set_xticks(range(1, 11))
    ax.set_yticks(range(1, 11))


def row_normalization(Z):
    """
    Normalize a matrix by rows

    :param Z: matrix
    :return: normalized matrix
    """
    return Z / Z.sum(axis=1, keepdims=True)


# %%

x = range(1, 11)
y = range(1, 11)

Z = np.zeros((len(x), len(y)))

with open("../../sample_data/results_theory_of_mind.jsonl") as f:
    f.readline()
    for line in f:
        data = json.loads(line)
        Z[data["actual_status"] - 1, data["estimated_status"] - 1] += 1


ax = plt.axes(projection="3d")
plot_3d(x, y, Z, ax)

plt.show()

# %%
