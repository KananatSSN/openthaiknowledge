"""Theory 3.2.3: the fringes of two stars at +-alpha wash out when a bright fringe of one falls on a dark fringe of the other: 2 d0 sin(alpha) = (n + 1/2) lambda and 2 d1 sin(alpha) = (n + 3/2) lambda, so 2 alpha ~ lambda/(d1 - d0). Adapted: lambda (nm) and the two slit separations (mm); returns 2 alpha in arcseconds."""

from math import asin, degrees


def solve(wavelength=550, first=10.0, second=30.0):
    return wavelength * 1e-9 / ((second - first) * 1e-3) * 206264.806


def check(wavelength=550, first=10.0, second=30.0):
    # Exact: sin(alpha) = lambda/(2 (d1 - d0)), converted to arcseconds.
    alpha = asin(wavelength * 1e-9 / (2 * (second - first) * 1e-3))
    return 2 * degrees(alpha) * 3600


PARAMS = {"wavelength": 550, "first": 10.0, "second": 30.0}
VARIANTS = [{"second": 15.0}, {"wavelength": 650, "first": 5.0, "second": 25.0}, {"first": 40.0, "second": 120.0}]
ANSWER = 5.672282165
TOL = 1e-6
