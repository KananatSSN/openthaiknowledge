"""MC11 figure: square sideL, cyclic charges(+q,-q,+q,-q). Four attractive edge pairs and two repulsive diagonals give U=(-4+sqrt2)kq²/L. Generalize cyclic(+aQ,-bQ,+aQ,-bQ); return U/(kQ²/L)."""

from math import sqrt, hypot


def solve(a=1, b=1):
    return -4 * a * b + (a * a + b * b) / sqrt(2)


def check(a=1, b=1):
    # Independent all-site potential calculation, U=1/2 sum(q_i phi_i).
    charges = (a, -b, a, -b)
    positions = ((0, 1), (1, 1), (1, 0), (0, 0))
    energy = 0.0
    for i, (qi, point) in enumerate(zip(charges, positions)):
        potential = 0.0
        for j, (qj, other) in enumerate(zip(charges, positions)):
            if i != j:
                potential += qj / hypot(point[0] - other[0], point[1] - other[1])
        energy += qi * potential / 2
    return energy


PARAMS = {"a": 1, "b": 1}
VARIANTS = [{"a": 2}, {"b": 3}, {"a": 2, "b": 2}]
ANSWER = -2.585786437626905
