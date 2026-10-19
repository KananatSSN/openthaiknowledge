"""Part 1, 11: opposite charges -a at0 and +b at separation d, b>a. Third charge must be to the left. Source a12,b27,d10cm gives x=-20cm."""

from math import sqrt


def solve(a=12, b=27, d=10):
    if not 0 < a < b or d <= 0:
        raise ValueError("requires b>a>0 and d>0")
    return -d * sqrt(a) / (sqrt(b) - sqrt(a))


def check(a=12, b=27, d=10):
    # Find distance to left of origin where signed E=0, without rearranging.
    lo, hi = 1e-12, d
    while a / hi**2 > b / (hi + d) ** 2:
        hi *= 2
    for _ in range(120):
        r = (lo + hi) / 2
        if a / r**2 > b / (r + d) ** 2:
            lo = r
        else:
            hi = r
    return -(lo + hi) / 2


PARAMS = {"a": 12, "b": 27, "d": 10}
VARIANTS = [{"a": 4, "b": 16}, {"d": 20}, {"a": 9, "b": 25}]
ANSWER = -19.999999999999993
