"""Part2,5 graph vertices (0,0),(1,2),(4,2),(4,-2),(5,0). Vertical jump at x4 contributes no work. Signed area6J."""

from fractions import Fraction


def solve(ramp=1, plateau=3, tail=1, positive=2, negative=2):
    return Fraction(positive * ramp - negative * tail, 2) + positive * plateau


def check(ramp=1, plateau=3, tail=1, positive=2, negative=2):
    # Independent midpoint integral on each segment; exact for linear F(x).
    total = 0.0
    for j in range(1000):
        f = (j + 0.5) / 1000
        total += positive * f * ramp / 1000
        total += positive * plateau / 1000
        total -= negative * (1 - f) * tail / 1000
    return total


PARAMS = {"ramp": 1, "plateau": 3, "tail": 1, "positive": 2, "negative": 2}
VARIANTS = [{"plateau": 4}, {"negative": 4}, {"ramp": 2}]
ANSWER = Fraction(6, 1)
