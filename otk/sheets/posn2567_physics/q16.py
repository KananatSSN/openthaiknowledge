"""Worked16 figure: (a) C1 in series with C2 || C equals C when C^2 + C2 C - C1 C2 = 0, C = (sqrt(C2^2 + 4 C1 C2) - C2)/2. (b) a ladder of series C1 = 4 uF and shunts C2 = 2 uF ends in a 4 uF = C2 + C shunt, so every node looks into C = 2 uF and each stage halves the voltage: V5 = E/32. Adapted: (C1, C2) with rational C; returns V at node `node` as a fraction of E."""

from math import sqrt


def solve(series=4, shunt=2, node=5):
    c = (sqrt(shunt * shunt + 4 * series * shunt) - shunt) / 2
    return (series / (series + shunt + c)) ** node


def check(series=4, shunt=2, node=5):
    # Build the ladder (node shunts C2, last node shunt C2 + C) and solve the
    # node voltages from charge balance by Gauss-Seidel, E = 1.
    c = (sqrt(shunt * shunt + 4 * series * shunt) - shunt) / 2
    count = node
    shunts = [shunt] * (count - 1) + [shunt + c]
    v = [0.0] * (count + 1)
    v[0] = 1.0
    for _ in range(20000):
        for k in range(1, count + 1):
            right = v[k + 1] if k < count else None
            num = series * v[k - 1] + (series * right if right is not None else 0.0)
            den = series + shunts[k - 1] + (series if right is not None else 0.0)
            v[k] = num / den
    return v[count]


PARAMS = {"series": 4, "shunt": 2, "node": 5}
VARIANTS = [{"series": 6, "shunt": 1, "node": 3}, {"series": 2, "shunt": 1, "node": 4}, {"series": 6, "shunt": 3, "node": 2}]
TOL = 1e-9
ANSWER = 0.03125
