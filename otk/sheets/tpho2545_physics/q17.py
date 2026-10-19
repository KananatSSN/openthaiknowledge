"""Experiment 2 figure: the innermost dark ring of an opaque disc of diameter D sits at D sin(theta) = 1.22 lambda; it falls on the holes 0.5 cm off centre when the plate is x away, theta ~ 0.5/x. lambda = D (0.5/x)/1.22. Nanometres for D in 1e-4 cm and x in cm."""

from math import atan, sin


def solve(diameter=30, distance=40, offset=0.5):
    return diameter * 1e-4 * (offset / distance) / 1.22 * 1e7


def check(diameter=30, distance=40, offset=0.5):
    # Exact geometry: tan(theta) = offset / x and D sin(theta) = 1.22 lambda;
    # agrees with the small-angle form to within the tolerance.
    theta = atan(offset / distance)
    return diameter * 1e-4 * sin(theta) / 1.22 * 1e7

PARAMS = {"diameter": 30, "distance": 40, "offset": 0.5}
VARIANTS = [{"distance": 20}, {"diameter": 25, "distance": 30}, {"offset": 1.0, "distance": 80}]
TOL = 1e-3
ANSWER = 307.37704918032796
