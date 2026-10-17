"""MC14 figure: two parallel branches across48V. Upper: (5uF||4uF) series3uF. Lower:6uF series(2uF||3uF||7uF). Asked charge on6uF is192uC. Floating midpoint initially neutral. Upper branch cannot change lower branch voltage."""

from fractions import Fraction
import numpy as np


def solve(voltage=48, cap=6, parallel=(2, 3, 7), upper=(5, 4, 3)):
    other = sum(parallel)
    return Fraction(voltage * cap * other, cap + other)


def check(voltage=48, cap=6, parallel=(2, 3, 7), upper=(5, 4, 3)):
    # Solve neutrality at both floating midpoints, potentials right0,leftV.
    a, b, c = upper
    lower_node, upper_node = np.linalg.solve(
        [[cap + sum(parallel), 0], [0, a + b + c]], [cap * voltage, (a + b) * voltage]
    )
    assert abs((a + b) * (voltage - upper_node) - c * upper_node) < 1e-9
    return float(cap * (voltage - lower_node))


PARAMS = {"voltage": 48, "cap": 6, "parallel": (2, 3, 7), "upper": (5, 4, 3)}
VARIANTS = [{"voltage": 24}, {"cap": 3}, {"upper": (10, 20, 30)}]
ANSWER = Fraction(192, 1)
