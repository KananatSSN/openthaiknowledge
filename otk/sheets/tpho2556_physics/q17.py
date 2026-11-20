"""Theory 3 (i)-(k): for two internal reflections alpha = 6 phi - 2 theta - pi, extreme at cos^2 theta = (n^2 - 1)/8: |alpha| = 50.1 degrees for n = 1.33 (theta = 71.9, phi = 45.6); between 42.5 and 50.1 degrees neither bow sends light, Alexander's dark band. Adapted: n varies; returns |alpha| in degrees."""

from math import acos, asin, degrees, pi, sin, sqrt


def solve(index=1.33):
    theta = acos(sqrt((index**2 - 1) / 8))
    phi = asin(sin(theta) / index)
    return abs(degrees(6 * phi - 2 * theta - pi))


def check(index=1.33):
    # Smallest |deviation| over incidences, by golden section.
    from otk.sheets.tpho2556_physics._bow import deviation

    lo, hi = 0.0, pi / 2
    r = (sqrt(5) - 1) / 2
    for _ in range(200):
        a, b = hi - r * (hi - lo), lo + r * (hi - lo)
        if abs(deviation(a, index, 2)) < abs(deviation(b, index, 2)):
            hi = b
        else:
            lo = a
    return abs(degrees(deviation((lo + hi) / 2, index, 2)))


PARAMS = {"index": 1.33}
VARIANTS = [{"index": 1.331}, {"index": 1.343}, {"index": 1.5}]
ANSWER = 50.10124807838471
TOL = 1e-9
