"""Short5: the charged ring of item 4 spun about OZ at omega carries current I = Q omega/(2 pi). Microamps for Q in microcoulombs."""

from math import pi


def solve(charge=4, omega=10):
    return charge * omega / (2 * pi)


def check(charge=4, omega=10):
    # Count the charge crossing a fixed radius line during one period.
    period = 2 * pi / omega
    return charge / period


PARAMS = {"charge": 4, "omega": 10}
VARIANTS = [{"omega": 3}, {"charge": 9, "omega": 20}, {"charge": 1}]
ANSWER = 6.366197723675814
