"""Theory 3 (a), (e), (g), (h): for one internal reflection alpha = 4 phi - 2 theta, largest at the bright incidence cos^2 theta = (n^2 - 1)/3: 42.5 degrees for n = 1.33 (theta = 59.6, phi = 40.4), so primary-bow light leaves at 0 to 42.5 degrees and the sky inside the bow is brighter. Adapted: n varies; returns alpha in degrees."""

from math import acos, asin, degrees, sin, sqrt


def solve(index=1.33):
    theta = acos(sqrt((index**2 - 1) / 3))
    phi = asin(sin(theta) / index)
    return degrees(4 * phi - 2 * theta)


def check(index=1.33):
    # Largest deviation over a fine scan of incidences, refined by golden section.
    from math import pi

    from otk.sheets.tpho2556_physics._bow import deviation

    lo, hi = 0.0, pi / 2
    r = (sqrt(5) - 1) / 2
    for _ in range(200):
        a, b = hi - r * (hi - lo), lo + r * (hi - lo)
        if deviation(a, index, 1) > deviation(b, index, 1):
            hi = b
        else:
            lo = a
    return degrees(deviation((lo + hi) / 2, index, 1))


PARAMS = {"index": 1.33}
VARIANTS = [{"index": 1.331}, {"index": 1.343}, {"index": 1.5}]
ANSWER = 42.516381721084485
TOL = 1e-9
