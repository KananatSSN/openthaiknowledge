"""Theory 1.1-1.2 figure: the ring's total flux pi R^2 B_z + L I stays B0 pi R^2, so at depth z the current is I = pi R^2 alpha B0 z/L, clockwise seen from above. Adapted: B0, alpha and the depth vary; returns |I| in amperes for R = 0.50 cm, L = 1.3e-8 H."""

from math import pi


def solve(B0=0.010, alpha=2.0, radius=0.005, inductance=1.3e-8, depth=0.05):
    return pi * radius**2 * alpha * B0 * depth / inductance


def check(B0=0.010, alpha=2.0, radius=0.005, inductance=1.3e-8, depth=0.05):
    # Faraday step by step: L dI = -d(flux of the magnet) over small falls.
    n = 1000
    current = 0.0
    for i in range(n):
        z0, z1 = depth * i / n, depth * (i + 1) / n
        current -= pi * radius**2 * B0 * alpha * (z1 - z0) / inductance
    return abs(current)


PARAMS = {"B0": 0.010, "alpha": 2.0, "radius": 0.005, "inductance": 1.3e-8, "depth": 0.05}
VARIANTS = [{"depth": 0.1}, {"B0": 0.02, "alpha": 1.5}, {"radius": 0.004}]
ANSWER = 6.041524333826526
TOL = 1e-9
