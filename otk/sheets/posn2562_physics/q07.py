"""MC7 figure: uniform rod lengthl with insulated lateral surface, ends fixed T1>T2, pointx fromhotend. Intended steady state T=T1-(x/l)(T1-T2), source answer4. Source omits the word steady; generator states it."""

from fractions import Fraction
import numpy as np


def solve(hot=100, cold=20, fraction=0.25):
    return Fraction(hot) - Fraction(str(fraction)) * (hot - cold)


def check(hot=100, cold=20, fraction=0.25):
    # Discrete steady conduction, all interior nodes have zero net heat flow.
    count = 20
    matrix = 2 * np.eye(count - 1) - np.eye(count - 1, k=1) - np.eye(count - 1, k=-1)
    rhs = np.zeros(count - 1)
    rhs[0] = hot
    rhs[-1] = cold
    nodes = np.concatenate(([hot], np.linalg.solve(matrix, rhs), [cold]))
    position = float(fraction) * count
    i = int(position)
    if i == count:
        return float(nodes[-1])
    return float(nodes[i] * (i + 1 - position) + nodes[i + 1] * (position - i))


PARAMS = {"hot": 100, "cold": 20, "fraction": 0.25}
VARIANTS = [{"fraction": 0.5}, {"hot": 120}, {"cold": 40}]
ANSWER = Fraction(80, 1)
