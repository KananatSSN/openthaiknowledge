"""Theory 1.3 figure: an electron enters an equilateral triangle (side a) of field B (into the page) at the middle of the base, moving along +y; to leave moving along +x it turns a quarter circle of radius r = sqrt(3) a/(2(1 + sqrt 3)) ~ 0.317a, so v = eBr/m. Adapted: B and a given with e/m = 1.76e11 C/kg; m/s."""

from math import sqrt


def solve(field=0.01, side=0.1, charge_mass=1.76e11):
    radius = sqrt(3) * side / (2 * (1 + sqrt(3)))
    return charge_mass * field * radius


def check(field=0.01, side=0.1, charge_mass=1.76e11):
    # Bisect on the radius: the quarter-circle exit point (r, r) from the base
    # midpoint must lie on the triangle's right side.
    def outside(r):
        return r / (side / 2) + r / (side * sqrt(3) / 2) - 1

    lo, hi = 0.0, side
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if outside(mid) < 0 else (lo, mid)
    return charge_mass * field * lo


PARAMS = {"field": 0.01, "side": 0.1, "charge_mass": 1.76e11}
VARIANTS = [{"field": 0.002}, {"side": 0.05}, {"field": 0.05, "side": 0.2}]
ANSWER = 55789764.46696941
TOL = 1e-9
