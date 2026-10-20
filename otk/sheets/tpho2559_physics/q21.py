"""Lab part 2: with R = c1 E^gamma and R = 1.0e4 ohm at 10 lux, c1 = 1e4/10^gamma; the lamp then gives E = (R/c1)^(1/gamma) at x = 30 cm and a luminous flux E 4 pi x^2 (294 lm for R = 1285 ohm, gamma = -0.63, as in the solution). Adapted: gamma, R (ohm) and x (cm) vary; returns the flux in lumens."""

from math import pi


def solve(gamma=-0.63, resistance=1285.0, distance=30.0):
    c1 = 1e4 / 10**gamma
    illuminance = (resistance / c1) ** (1 / gamma)
    return illuminance * 4 * pi * (distance * 1e-2) ** 2


def check(gamma=-0.63, resistance=1285.0, distance=30.0):
    # Bisect the illuminance whose LDR reading matches, then spread the
    # flux over the sphere by summing rings.
    from math import sin

    from otk.sheets.tpho2559_physics._shared import bisect

    c1 = 1e4 / 10**gamma
    E = bisect(lambda e: c1 * e**gamma - resistance, 1e-3, 1e6)
    x = distance * 1e-2
    n = 4000
    area = sum(2 * pi * x * x * sin((i + 0.5) * pi / n) * pi / n for i in range(n))
    return E * area


PARAMS = {"gamma": -0.63, "resistance": 1285.0, "distance": 30.0}
VARIANTS = [{"resistance": 2000.0}, {"gamma": -0.7}, {"distance": 40.0, "resistance": 1800.0}]
ANSWER = 293.69182187615553
TOL = 1e-6
