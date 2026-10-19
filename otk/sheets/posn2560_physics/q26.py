"""Part2,6: far-apart conducting spheres initially +Q each, wire connected. Final charge a is fraction s of initial Q. Source s1/3 =>b/a5. Neglect mutual capacitance as uniform-charge assumption requires."""

from fractions import Fraction
import numpy as np


def solve(num=1, den=3):
    return Fraction(2 * den - num, num)


def check(num=1, den=3):
    # For a trial b/a, solve conservation and equal surface potentials.
    lo, hi = 0.0, 100.0
    for _ in range(100):
        ratio = (lo + hi) / 2
        qa, qb = np.linalg.solve([[1, 1], [1, -1 / ratio]], [2, 0])
        assert abs(qa + qb - 2) < 1e-10
        if qa > num / den:
            lo = ratio
        else:
            hi = ratio
    return (lo + hi) / 2


PARAMS = {"num": 1, "den": 3}
VARIANTS = [{"den": 4}, {"num": 2, "den": 3}, {"num": 1, "den": 2}]
ANSWER = Fraction(5, 1)
