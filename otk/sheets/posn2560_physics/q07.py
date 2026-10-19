"""Part 1, 7: Hookean bow drawn from zero extension, final force F. All stored energy goes into the arrow."""

from math import sqrt


def solve(force=120, extension=0.6, mass=0.02):
    return sqrt(force * extension / mass)


def check(force=120, extension=0.6, mass=0.02):
    # Midpoint quadrature of the force-extension graph, then solve K(v)=work.
    work = sum(force * (j + 0.5) / 1000 * extension / 1000 for j in range(1000))
    lo, hi = 0.0, 1 + 2 * work / mass
    for _ in range(100):
        v = (lo + hi) / 2
        if mass * v * v / 2 < work:
            lo = v
        else:
            hi = v
    return (lo + hi) / 2


PARAMS = {"force": 120, "extension": 0.6, "mass": 0.02}
VARIANTS = [{"force": 180}, {"extension": 0.4}, {"mass": 0.08}]
ANSWER = 60.0
