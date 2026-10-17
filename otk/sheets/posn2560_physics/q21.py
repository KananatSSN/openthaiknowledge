"""Part2,1: at fraction f of maximum height on ascent, velocity angle beta; answer tan² launch angle. Source f1/2, beta60deg =>6, launch atan(sqrt6)."""

from math import tan, radians, sqrt


def solve(fraction=0.5, beta=60):
    return tan(radians(beta)) ** 2 / (1 - fraction)


def check(fraction=0.5, beta=60):
    # Set vx=1, g=1. Search initial vy using the ascending height equation.
    measured = tan(radians(beta))
    lo, hi = measured, 1000.0
    for _ in range(100):
        vy0 = (lo + hi) / 2
        target = fraction * vy0 * vy0 / 2
        t = 2 * target / (vy0 + sqrt(vy0 * vy0 - 2 * target))
        if vy0 - t < measured:
            lo = vy0
        else:
            hi = vy0
    return ((lo + hi) / 2) ** 2


PARAMS = {"fraction": 0.5, "beta": 60}
VARIANTS = [{"fraction": 0.25}, {"beta": 45}, {"beta": 30}]
ANSWER = 5.9999999999999964
