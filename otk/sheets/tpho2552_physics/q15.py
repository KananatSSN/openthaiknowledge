"""Lab 1: a disc magnet (radius r, thickness t) has on its axis B(y) = B0 sqrt(1 + (r/t)^2) [(y + t)/sqrt((y + t)^2 + r^2) - y/sqrt(y^2 + r^2)], so a field read at distance y gives B0. Adapted: synthetic r, t, y (cm) and B(y) (G); gauss."""

from math import sqrt


def solve(radius=1.0, thickness=0.3, distance=1.0, reading=200.0):
    shape = sqrt(1 + (radius / thickness) ** 2) * (
        (distance + thickness) / sqrt((distance + thickness) ** 2 + radius**2) - distance / sqrt(distance**2 + radius**2)
    )
    return reading / shape


def check(radius=1.0, thickness=0.3, distance=1.0, reading=200.0):
    # At y = 0 the formula must return B0: bisect on B0 so that a model
    # through the surface value predicts the reading.
    def model(b0, y):
        return b0 * sqrt(1 + (radius / thickness) ** 2) * (
            (y + thickness) / sqrt((y + thickness) ** 2 + radius**2) - y / sqrt(y * y + radius**2)
        )

    assert abs(model(1.0, 0.0) - 1.0) < 1e-12
    lo, hi = 0.0, 1e9
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if model(mid, distance) < reading else (lo, mid)
    return lo


PARAMS = {"radius": 1.0, "thickness": 0.3, "distance": 1.0, "reading": 200.0}
VARIANTS = [{"distance": 0.5}, {"radius": 2.0, "thickness": 0.5}, {"reading": 80.0, "distance": 2.0}]
ANSWER = 672.0235437099356
TOL = 1e-9
