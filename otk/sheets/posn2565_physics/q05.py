"""MC5 figure: smooth cylinder of mass M rests in a sling whose two straps both make theta with the horizontal (equal tension on a smooth surface forces equal angles). 2T sin theta = Mg, T = Mg/(2 sin theta) (answer 4). Newtons, g = 10."""

from math import asin, sin


def solve(mass=6, sine=0.6, g=10):
    return mass * g / (2 * sine)


def check(mass=6, sine=0.6, g=10):
    # Bisect on T until the vertical forces on the cylinder balance.
    theta = asin(sine)
    lo, hi = 0.0, 1e6
    for _ in range(200):
        t = (lo + hi) / 2
        if 2 * t * sin(theta) < mass * g:
            lo = t
        else:
            hi = t
    t = (lo + hi) / 2
    return t


PARAMS = {"mass": 6, "sine": 0.6, "g": 10}
VARIANTS = [{"sine": 0.8}, {"mass": 13, "sine": 5 / 13}, {"mass": 2, "sine": 0.5}]
ANSWER = 50.0
