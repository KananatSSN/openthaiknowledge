"""MC16 figure: a 90-45-45 prism turns light back by total reflection on its two slanted faces, met at 45 deg; mu sin 45 >= 1 needs mu >= sqrt2 (answer 2). Adapted: the light meets the reflecting face at angle phi; least mu = 1/sin phi."""

from math import asin, pi, sin


def solve(angle=45):
    return 1 / sin(angle * pi / 180)


def check(angle=45):
    # Bisect on mu until the critical angle equals the incidence angle.
    lo, hi = 1.0, 10.0
    for _ in range(200):
        mu = (lo + hi) / 2
        if asin(1 / mu) > angle * pi / 180:
            lo = mu
        else:
            hi = mu
    return (lo + hi) / 2


PARAMS = {"angle": 45}
VARIANTS = [{"angle": 60}, {"angle": 30}, {"angle": 53}]
ANSWER = 1.4142135623730951
