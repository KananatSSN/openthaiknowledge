"""MC12: two equal charges on equal strings keep SAME separation and angle when both masses double. Coulomb force must double, so each charge scales sqrt2. Return new/old charge for mass multiplier factor."""

from math import sqrt, sin, cos, pi


def solve(factor=2):
    return sqrt(factor)


def check(factor=2):
    # Construct a real initial equilibrium at angle30deg to vertical.
    theta = pi / 6
    mass, g, length, k = 1.0, 10.0, 2.0, 9e9
    distance = 2 * length * sin(theta)
    q1 = sqrt(mass * g * sin(theta) / cos(theta) * distance**2 / k)
    lo, hi = 0.0, max(2.0, factor + 1.0)
    for _ in range(100):
        ratio = (lo + hi) / 2
        electric = k * (q1 * ratio) ** 2 / distance**2
        required = factor * mass * g * sin(theta) / cos(theta)
        if electric < required:
            lo = ratio
        else:
            hi = ratio
    return (lo + hi) / 2


PARAMS = {"factor": 2}
VARIANTS = [{"factor": 3}, {"factor": 4}, {"factor": 9}]
ANSWER = 1.4142135623730951
