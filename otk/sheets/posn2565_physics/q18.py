"""MC18 figure: F pushes M forward and downward at theta below the horizontal; friction coefficient mu. F cos theta must exceed mu (Mg + F sin theta) for some large F, so cos theta > mu sin theta: theta < arctan(1/mu) (answer 1). Returns tan of the limiting angle."""

from math import cos, sin, tan


def solve(mu=0.5):
    return 1 / mu


def check(mu=0.5, mass=1, g=10):
    # Bisect on theta: below the limit a big enough push moves the block.
    def movable(theta, force=1e9):
        return force * cos(theta) > mu * (mass * g + force * sin(theta))

    lo, hi = 0.0, 1.5707963
    for _ in range(200):
        mid = (lo + hi) / 2
        if movable(mid):
            lo = mid
        else:
            hi = mid
    return tan((lo + hi) / 2)


PARAMS = {"mu": 0.5}
VARIANTS = [{"mu": 0.75}, {"mu": 4 / 3}, {"mu": 0.2}]
TOL = 1e-6
ANSWER = 2.0
