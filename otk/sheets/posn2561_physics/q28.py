"""Written8 figure: uniform thinrodL60cm pivoted at dry upperend, submerged bottom20cm, floating in water at a nonvertical angle. Weightcentroid30cm; buoyancycentroid50cm frompivot. rho_water/rho_rod=9/5. Pivot exerts no torque."""

from fractions import Fraction
from math import cos, pi


def solve(length=60, submerged=20):
    return Fraction(length * length, submerged * (2 * length - submerged))


def check(length=60, submerged=20):
    # Integrate distributed gravity/buoyancy torques, rod density normalized1.
    steps = 1000
    lever = cos(pi / 4)
    dx = length / steps
    weight = sum((i + 0.5) * dx * dx * lever for i in range(steps))
    dx = submerged / steps
    buoyancy_per_ratio = sum(
        (length - submerged + (i + 0.5) * dx) * dx * lever for i in range(steps)
    )
    lo, hi = 0.0, 100.0
    for _ in range(100):
        ratio = (lo + hi) / 2
        if ratio * buoyancy_per_ratio < weight:
            lo = ratio
        else:
            hi = ratio
    return (lo + hi) / 2


PARAMS = {"length": 60, "submerged": 20}
VARIANTS = [{"submerged": 30}, {"length": 80}, {"submerged": 15}]
ANSWER = Fraction(9, 5)
