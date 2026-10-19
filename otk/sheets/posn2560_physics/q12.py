"""Part 1,12: +pQ at(0,0), -nQ at(2a,0), observation(a,h), p>n. Return tan of direction angle. Source p2,n1,a3,h4 gives4/9."""

from fractions import Fraction
from math import hypot


def solve(p=2, n=1, a=3, h=4):
    return Fraction((p - n) * h, (p + n) * a)


def check(p=2, n=1, a=3, h=4):
    ex = ey = 0.0
    for charge, x, y in ((p, 0, 0), (-n, 2 * a, 0)):
        dx, dy = a - x, h - y
        radius = hypot(dx, dy)
        ex += charge * dx / radius**3
        ey += charge * dy / radius**3
    return ey / ex


PARAMS = {"p": 2, "n": 1, "a": 3, "h": 4}
VARIANTS = [{"p": 3}, {"a": 4, "h": 3}, {"p": 4, "n": 2}]
ANSWER = Fraction(4, 9)
