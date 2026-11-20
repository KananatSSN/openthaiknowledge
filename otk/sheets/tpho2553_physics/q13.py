"""Lab 1, part 3: measuring the Brewster angle of a syrup gives its index n = tan(theta_B). Adapted: a synthetic Brewster angle (degrees); the index."""

from math import radians, tan


def solve(angle=55.0):
    return tan(radians(angle))


def check(angle=55.0):
    # Fresnel: the p-polarised reflection coefficient vanishes; bisect on n.
    from math import asin, cos, sin

    theta = radians(angle)

    def rp(n):
        t = asin(sin(theta) / n)
        return (n * cos(theta) - cos(t)) / (n * cos(theta) + cos(t))

    lo, hi = 1.0001, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if rp(mid) < 0 else (lo, mid)
    return lo


PARAMS = {"angle": 55.0}
VARIANTS = [{"angle": 53.1}, {"angle": 56.5}, {"angle": 60.0}]
ANSWER = 1.4281480067421144
TOL = 1e-9
