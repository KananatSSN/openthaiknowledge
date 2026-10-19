"""Short13: a soap bubble of radius R has two surfaces of tension gamma; inside is higher by 4 gamma / R. Pascals for gamma in N/m and R in cm."""

from math import pi


def solve(tension=0.025, radius=2):
    return 4 * tension / (radius / 100)


def check(tension=0.025, radius=2):
    # Force balance on a hemisphere: pressure difference times the disc area
    # equals tension along the rim on both films.
    r = radius / 100
    return 2 * (2 * pi * r * tension) / (pi * r * r)


PARAMS = {"tension": 0.025, "radius": 2}
VARIANTS = [{"tension": 0.07, "radius": 1}, {"radius": 5}, {"tension": 0.04, "radius": 0.5}]
ANSWER = 5.0
