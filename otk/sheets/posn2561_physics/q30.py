"""Written10a,b: Galilean beam expander: diverging f=-4cm then converging f=+12cm. Parallel incident rays emergeparallel, diameter3times, separation8cm. Three-ray construction is independently traced numerically; no intermediate real focus."""

import numpy as np


def solve(diverging=4, converging=12):
    return converging - diverging


def ray_matrix(distance, diverging, converging):
    return (
        np.array([[1.0, 0.0], [-1 / converging, 1.0]])
        @ np.array([[1.0, distance], [0.0, 1.0]])
        @ np.array([[1.0, 0.0], [1 / diverging, 1.0]])
    )


def check(diverging=4, converging=12):
    lo, hi = 0.0, 2.0 * converging
    for _ in range(100):
        distance = (lo + hi) / 2
        matrix = ray_matrix(distance, diverging, converging)
        if matrix[1, 0] > 0:
            lo = distance
        else:
            hi = distance
    distance = (lo + hi) / 2
    for height in (-1.0, 0.0, 1.0):
        out = ray_matrix(distance, diverging, converging) @ np.array([height, 0.0])
        assert abs(out[1]) < 1e-10
        assert abs(out[0] - height * converging / diverging) < 1e-10
    return distance


PARAMS = {"diverging": 4, "converging": 12}
VARIANTS = [
    {"diverging": 3, "converging": 15},
    {"diverging": 5, "converging": 20},
    {"diverging": 6, "converging": 18},
]
ANSWER = 8
