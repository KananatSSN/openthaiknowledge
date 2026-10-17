"""Part2,3: nonuniform horizontal rod length3L. Initially vertical end strings, left tensionT; then support at L replaces left string, right tensionT. Return W/T=5/2."""

from fractions import Fraction
import numpy as np


def solve(length=3, pivot=1):
    return Fraction(2 * length - pivot, length - pivot)


def check(length=3, pivot=1):
    # Unknown W and moment of weight W*x, set T=1. Two independent torques.
    weight, moment = np.linalg.solve([[length, -1], [-pivot, 1]], [length, length - pivot])
    assert pivot < moment / weight < length
    return float(weight)


PARAMS = {"length": 3, "pivot": 1}
VARIANTS = [{"length": 4}, {"pivot": 2}, {"length": 5, "pivot": 2}]
ANSWER = Fraction(5, 2)
