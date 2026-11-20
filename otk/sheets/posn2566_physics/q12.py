"""MC12 figure: a charged ring of radius R in the YZ plane; E(x,0,0) is odd in x, zero at the centre, peaks at x = +-R/sqrt2 and decays (answer 1). Adapted quantity: the distance of the peak, R/sqrt2. cm."""

from math import sqrt


def solve(radius=10):
    return radius / sqrt(2)


def check(radius=10):
    # Golden-section search on x/(x^2 + R^2)^(3/2).
    f = lambda x: x / (x * x + radius * radius) ** 1.5
    lo, hi = 0.0, 5.0 * radius
    ratio = (sqrt(5) - 1) / 2
    for _ in range(300):
        a = hi - ratio * (hi - lo)
        c = lo + ratio * (hi - lo)
        if f(a) < f(c):
            lo = a
        else:
            hi = c
    return (lo + hi) / 2


PARAMS = {"radius": 10}
VARIANTS = [{"radius": 6}, {"radius": 1}, {"radius": 25}]
TOL = 1e-7
ANSWER = 7.071067811865475
