"""Part 1, 9: particle starts at rest on OUTSIDE of smooth hemisphere. Initial cos(theta0)=4/5 (sheet sin37=3/5). Answer is cos(theta) at separation, not theta in degrees."""

from math import acos, cos, pi


def solve(cos_start=0.8):
    return 2 * cos_start / 3


def check(cos_start=0.8):
    # Unit radius and g: at each angle energy gives v², radial forces give N.
    lo, hi = acos(cos_start), pi / 2
    for _ in range(100):
        theta = (lo + hi) / 2
        speed_squared = 2 * (cos_start - cos(theta))
        normal = cos(theta) - speed_squared
        if normal > 0:
            lo = theta
        else:
            hi = theta
    return cos((lo + hi) / 2)


PARAMS = {"cos_start": 0.8}
VARIANTS = [{"cos_start": 1}, {"cos_start": 0.6}, {"cos_start": 0.9}]
ANSWER = 0.5333333333333333
