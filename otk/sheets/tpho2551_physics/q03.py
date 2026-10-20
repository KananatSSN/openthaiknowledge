"""Theory 1.2.3: the deviation pi - 4 alpha + 2 phi is least where d(alpha)/d(phi) = 1/2, i.e. n cos(alpha) = 2 cos(phi): cos(phi) = sqrt((n^2 - 1)/3). Adapted: n given; degrees."""

from math import acos, asin, degrees, radians, sin, sqrt


def solve(index=4 / 3):
    return degrees(acos(sqrt((index**2 - 1) / 3)))


def check(index=4 / 3):
    # Golden-section search for the smallest deviation.
    def deviation(phi):
        return 180 - 4 * degrees(asin(sin(radians(phi)) / index)) + 2 * phi

    lo, hi = 0.0, 90.0
    g = (sqrt(5) - 1) / 2
    for _ in range(200):
        x1, x2 = hi - g * (hi - lo), lo + g * (hi - lo)
        lo, hi = (lo, x2) if deviation(x1) < deviation(x2) else (x1, hi)
    return (lo + hi) / 2


PARAMS = {"index": 4 / 3}
VARIANTS = [{"index": 1.5}, {"index": 1.33}, {"index": 1.25}]
ANSWER = 59.391102340290686
TOL = 1e-7
