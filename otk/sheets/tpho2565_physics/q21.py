"""Lab part 3 b): the flux out of half a long magnet is Phi = mu0 M ((L/2)/sqrt(R^2 + (L/2)^2)) pi R^2, so 9.15e-5 Wb from a magnet with R = 5.0 mm and L = 30.0 mm gives M = 0.98e6 A/m. Adapted: the flux (1e-5 Wb), R and L (mm) vary; returns 1e6 A/m."""

from math import pi, sqrt


def solve(flux=9.15, radius=5.0, length=30.0):
    from otk.sheets.tpho2565_physics._shared import MU0

    r, half = radius * 1e-3, length * 1e-3 / 2
    return flux * 1e-5 * sqrt(r * r + half * half) / (MU0 * half * pi * r * r) / 1e6


def check(flux=9.15, radius=5.0, length=30.0):
    from otk.sheets.tpho2565_physics._shared import MU0, bisect

    r, half = radius * 1e-3, length * 1e-3 / 2
    share = half / sqrt(r * r + half * half)
    return bisect(lambda m: MU0 * m * 1e6 * share * pi * r * r - flux * 1e-5, 0.0, 100.0)


PARAMS = {"flux": 9.15, "radius": 5.0, "length": 30.0}
VARIANTS = [{"flux": 8.90}, {"length": 20.0}, {"radius": 4.0}]
ANSWER = 0.9772374323786468
TOL = 1e-9
