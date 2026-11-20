"""Theory 1.2: for m << M, v ~ [(1 + m/2M)/(1 + (m/2M) sin^2 theta)] sqrt(2gR(1 - cos theta)), so v exceeds the fixed-cylinder speed by the fraction (m/2M) cos^2 theta to first order. Adapted: m/M and theta given; returns that fraction."""

from math import cos, radians, sin, sqrt


def solve(ratio=0.01, angle=60):
    return ratio / 2 * cos(radians(angle)) ** 2


def check(ratio=0.01, angle=60):
    # Slope of the exact v/v0 - 1 in m/M at m/M -> 0, by a central difference.
    s2 = sin(radians(angle)) ** 2

    def excess(e):
        return sqrt((1 + e) / (1 + e * s2)) - 1

    h = 1e-6
    return ratio * (excess(h) - excess(-h)) / (2 * h)


PARAMS = {"ratio": 0.01, "angle": 60}
VARIANTS = [{"angle": 30}, {"ratio": 0.002, "angle": 45}, {"angle": 0}]
ANSWER = 0.0012500000000000007
TOL = 1e-6
