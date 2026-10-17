"""Part2,7: three parallel branches L to R. Top source +3V right then1ohm,I1=2A right. Middle source +6V left then2ohm,I2 left. Bottom unknown source +right then4ohm,I3 right. V_R-V_L=1V,I2=3.5A,I3=1.5A."""

from fractions import Fraction
import numpy as np


def solve(e1=3, r1=1, e2=6, r2=2, i1=2):
    return Fraction(e1 - i1 * r1 + e2, r2) - i1


def check(e1=3, r1=1, e2=6, r2=2, i1=2):
    # Unknown potential V_R-V_L, middle leftward I2, bottom rightward I3.
    v, i2, i3 = np.linalg.solve([[1, 0, 0], [1, -r2, 0], [0, 1, -1]], [e1 - i1 * r1, -e2, i1])
    assert abs(v - (e1 - i1 * r1)) < 1e-10
    return float(i3)


PARAMS = {"e1": 3, "r1": 1, "e2": 6, "r2": 2, "i1": 2}
VARIANTS = [{"e2": 8}, {"i1": 1}, {"e1": 5}]
ANSWER = Fraction(3, 2)
