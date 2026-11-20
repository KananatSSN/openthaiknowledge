"""Short22: two bodies a fixed D apart circling their centre of mass: T = 2 pi sqrt(D^3/(G (M + m))). Adapted: scale D by s and the total mass by k; the period scales by sqrt(s^3/k)."""

from math import pi, sqrt


def solve(scale=2, mass_factor=2):
    return sqrt(scale**3 / mass_factor)


def check(scale=2, mass_factor=2):
    # Absolute periods with G(M+m) = 1 and D = 1, then the scaled system.
    period = lambda d, mu: 2 * pi / sqrt(mu / d**3)
    return period(scale, mass_factor) / period(1, 1)


PARAMS = {"scale": 2, "mass_factor": 2}
VARIANTS = [{"scale": 4, "mass_factor": 1}, {"scale": 1, "mass_factor": 9}, {"scale": 3, "mass_factor": 3}]
ANSWER = 2.0
