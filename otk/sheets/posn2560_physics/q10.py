"""Part 1, 10: horizontal uniform AB=4m, vertical wall AC=3m, cable BC. Beam weight 200N at midpoint and load300N at B."""

from math import hypot
import numpy as np


def solve(length=4, height=3, weight=200, load=300):
    return (weight / 2 + load) * hypot(length, height) / height


def check(length=4, height=3, weight=200, load=300):
    # Unknowns are hinge Fx,Fy and cable tension; independently solve Fx,Fy,torque.
    norm = hypot(length, height)
    forces = [[1, 0, -length / norm], [0, 1, height / norm], [0, 0, length * height / norm]]
    rhs = [0, weight + load, weight * length / 2 + load * length]
    return float(np.linalg.solve(forces, rhs)[2])


PARAMS = {"length": 4, "height": 3, "weight": 200, "load": 300}
VARIANTS = [{"length": 3, "height": 4}, {"weight": 400}, {"load": 100}]
ANSWER = 666.6666666666666
