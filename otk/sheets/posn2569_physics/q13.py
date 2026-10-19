"""Part2 item 3 figure: a smooth wedge (slope beta, falling away from the push) is pushed horizontally; m stays put on it when a = g tan(beta). Input tan beta; m/s^2, g = 10."""

from math import atan, cos, sin


def solve(tangent=0.75, g=10):
    return g * tangent


def check(tangent=0.75, g=10):
    # Bisect on a for zero acceleration of m along the slope in the wedge frame:
    # g sin(beta) down the slope against a cos(beta) up it.
    beta = atan(tangent)
    lo, hi = 0.0, 1e4
    for _ in range(200):
        a = (lo + hi) / 2
        if g * sin(beta) > a * cos(beta):
            lo = a
        else:
            hi = a
    return (lo + hi) / 2


PARAMS = {"tangent": 0.75, "g": 10}
VARIANTS = [{"tangent": 4 / 3}, {"tangent": 5 / 12}, {"tangent": 1}]
ANSWER = 7.5
