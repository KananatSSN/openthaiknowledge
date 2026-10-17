"""Part 1,13 figure: four parallel branches between a,b: X,15ohm,6ohm,10ohm. Total2ohm. No series resistor hidden in rectangle outline."""

from fractions import Fraction


def solve(total=2, resistors=(15, 6, 10)):
    conductance = 1 / Fraction(total) - sum(1 / Fraction(r) for r in resistors)
    if conductance <= 0:
        raise ValueError("no positive unknown resistor")
    return 1 / conductance


def check(total=2, resistors=(15, 6, 10)):
    # Apply 1V and match the measured current by bisection in X.
    current = 1 / total
    lo, hi = 1e-12, 1.0
    while sum(1 / r for r in resistors) + 1 / hi > current:
        hi *= 2
    for _ in range(120):
        x = (lo + hi) / 2
        if sum(1 / r for r in resistors) + 1 / x > current:
            lo = x
        else:
            hi = x
    return (lo + hi) / 2


PARAMS = {"total": 2, "resistors": (15, 6, 10)}
VARIANTS = [{"total": 1}, {"resistors": (12, 6, 12)}, {"total": 3, "resistors": (30, 12, 20)}]
ANSWER = Fraction(6, 1)
