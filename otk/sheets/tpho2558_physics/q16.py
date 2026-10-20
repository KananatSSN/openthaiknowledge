"""Lab part 2.3: the tube (radius R, length L) and the needle resist in series, Q = pi rho g (h - y)/(8 eta_c (l/r^4 + L/R^4)), so eta_c = pi rho g/(8 (slope)(l/r^4 + L/R^4)); 0.0112 cm^2/s with L = 151.0 cm, R = 1.1 mm gives 1.6 mPa s. Adapted: the slope (cm^2/s), the tube length (cm) and the needle radius (mm) vary; returns eta_c in mPa s (rho = 1030 kg/m^3)."""

from math import pi


def solve(slope=0.0112, tube=151.0, radius=0.425, needle=4.0, bore=1.1, rho=1030.0, g=9.8):
    resist = needle * 1e-2 / (radius * 1e-3) ** 4 + tube * 1e-2 / (bore * 1e-3) ** 4
    return pi * rho * g / (8 * slope * 1e-4 * resist) * 1e3


def check(slope=0.0112, tube=151.0, radius=0.425, needle=4.0, bore=1.1, rho=1030.0, g=9.8):
    # The needle-only viscosity scaled by the needle's share of the total
    # flow resistance (the solution's alternative route).
    r, run = radius * 1e-3, needle * 1e-2
    eta = pi * r**4 * rho * g / (8 * slope * 1e-4 * run)
    share = (run / r**4) / (run / r**4 + tube * 1e-2 / (bore * 1e-3) ** 4)
    return eta * share * 1e3


PARAMS = {"slope": 0.0112, "tube": 151.0, "radius": 0.425, "needle": 4.0, "bore": 1.1, "rho": 1030.0, "g": 9.8}
VARIANTS = [{"tube": 120.0}, {"slope": 0.0095}, {"radius": 0.40, "tube": 180.0}]
ANSWER = 1.5678290441605165
TOL = 1e-9
