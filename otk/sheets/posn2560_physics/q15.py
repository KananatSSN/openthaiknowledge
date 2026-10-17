"""Part 1,15: stretch wire by x, conserve volume and resistivity, keep voltage fixed. Return new/old power."""

from fractions import Fraction


def solve(x=2):
    return Fraction(1, x * x)


def check(x=2):
    # Rebuild an arbitrary wire and its electrical powers in SI units.
    rho, length, area, voltage = 2e-8, 3.0, 4e-6, 6.0
    volume = length * area
    before = voltage**2 / (rho * length / area)
    length2 = length * x
    area2 = volume / length2
    after = voltage**2 / (rho * length2 / area2)
    return after / before


PARAMS = {"x": 2}
VARIANTS = [{"x": 3}, {"x": 4}, {"x": 5}]
ANSWER = Fraction(1, 4)
