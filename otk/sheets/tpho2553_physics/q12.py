"""Lab 1, part 2.1 figure 2: at Brewster's angle the reflected and refracted rays are perpendicular, so tan(theta_B) = n; for water (n = 1.3325) theta_B = 53.1 degrees. Adapted: n varies; degrees."""

from math import asin, atan, degrees, radians, sin


def solve(index=1.3325):
    return degrees(atan(index))


def check(index=1.3325):
    # Bisect on the incidence angle until the reflected and refracted rays
    # make 90 degrees.
    def gap(theta):
        refr = asin(sin(radians(theta)) / index)
        return theta + degrees(refr) - 90

    lo, hi = 1.0, 89.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if gap(mid) < 0 else (lo, mid)
    return lo


PARAMS = {"index": 1.3325}
VARIANTS = [{"index": 1.5}, {"index": 1.40}, {"index": 1.36}]
ANSWER = 53.1129067425735
TOL = 1e-9
