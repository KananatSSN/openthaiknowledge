"""MC3 figure: Earth mass M radius R with a thin atmosphere at its surface; m released from rest at distance x from the centre. Speed on reaching the atmosphere v = sqrt(2 g R (1 - R/x)) with g = GM/R^2 (answer 4). Adapted: x = n R; return v / sqrt(g R)."""

from math import sqrt


def solve(n=4):
    return sqrt(2 * (1 - 1 / n))


def check(n=4):
    # Work done by the inverse-square pull from x down to R, by Simpson's rule
    # (units g = R = m = 1, so the force at r is 1/r^2).
    steps = 2000
    lo, hi = 1.0, float(n)
    h = (hi - lo) / steps
    total = 0.0
    for k in range(steps + 1):
        r = lo + k * h
        weight = 1 if k in (0, steps) else (4 if k % 2 else 2)
        total += weight / (r * r)
    work = total * h / 3
    return sqrt(2 * work)


PARAMS = {"n": 4}
VARIANTS = [{"n": 2}, {"n": 9}, {"n": 1.5}]
ANSWER = 1.224744871391589
