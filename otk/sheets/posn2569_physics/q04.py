"""MC4 figure: Q at 0 and -beta Q at a (0 < beta < 1); the field vanishes beyond the smaller charge at x = a/(1 - sqrt(beta)) (answer 3)."""

from math import sqrt


def solve(beta=0.25, gap=3):
    return gap / (1 - sqrt(beta))


def check(beta=0.25, gap=3):
    # Bisect the net field (k = Q = 1) for x > a.
    field = lambda x: 1 / x**2 - beta / (x - gap) ** 2
    lo, hi = gap * (1 + 1e-9), gap * 1e6
    for _ in range(300):
        mid = (lo + hi) / 2
        if field(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"beta": 0.25, "gap": 3}
VARIANTS = [{"beta": 1 / 9}, {"beta": 4 / 9, "gap": 2}, {"beta": 0.0625, "gap": 6}]
TOL = 1e-9
ANSWER = 6.0
