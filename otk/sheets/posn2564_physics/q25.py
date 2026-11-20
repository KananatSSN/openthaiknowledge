"""MC25 figure: a slab of index mu2 separates medium mu1 from vacuum. Light from mu1 at theta1 to the normal crosses the slab and is just totally reflected at the slab-vacuum face. mu1 sin theta1 = mu2 sin theta2 = 1, so sin theta1 = 1/mu1 (answer 1)."""

from math import asin, sin


def solve(mu1=1.5, mu2=2):
    return 1 / mu1


def check(mu1=1.5, mu2=2):
    # Bisect on theta1 for the angle at which the vacuum-side sine reaches 1,
    # tracing Snell's law across both faces.
    def vacuum_sine(theta1):
        theta2 = asin(mu1 * sin(theta1) / mu2)
        return mu2 * sin(theta2)

    lo, hi = 0.0, asin(min(1.0, mu2 / mu1)) if mu2 < mu1 else 1.5707963267948966
    for _ in range(200):
        mid = (lo + hi) / 2
        if vacuum_sine(mid) < 1:
            lo = mid
        else:
            hi = mid
    return sin((lo + hi) / 2)


PARAMS = {"mu1": 1.5, "mu2": 2}
VARIANTS = [{"mu1": 4 / 3, "mu2": 1.5}, {"mu1": 2, "mu2": 2.4}, {"mu1": 1.25, "mu2": 5 / 3}]
ANSWER = 0.6666666666666666
