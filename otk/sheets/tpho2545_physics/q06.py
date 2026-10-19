"""Theory I.5 figure: ionosphere index n = sqrt(1 - lambda^2/A) above altitude h; a wave leaves the earth (radius R) at alpha to the vertical and meets the boundary at theta1 with (R + h) sin theta1 = R sin alpha. Total reflection needs sin theta1 >= n, so the shortest reflected wavelength is sqrt(A) sqrt(1 - (R sin alpha/(R + h))^2). Input sin alpha and h/R."""

from math import sqrt


def solve(constant=4, sine=0.6, height=0.25):
    s1 = sine / (1 + height)
    return sqrt(constant) * sqrt(1 - s1 * s1)


def check(constant=4, sine=0.6, height=0.25):
    # Bisect on lambda: reflection happens when the incidence sine at the
    # boundary (law of sines in the triangle earth-centre, launch, boundary)
    # is at least the ionosphere index.
    s1 = sine * 1 / (1 + height)
    reflects = lambda lam: s1 >= sqrt(max(0.0, 1 - lam * lam / constant))
    lo, hi = 0.0, sqrt(constant)
    for _ in range(200):
        mid = (lo + hi) / 2
        if reflects(mid):
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


PARAMS = {"constant": 4, "sine": 0.6, "height": 0.25}
VARIANTS = [{"sine": 0.8}, {"constant": 9, "height": 0.5}, {"sine": 1, "height": 0.25}]
TOL = 1e-9
ANSWER = 1.7545369759569047
