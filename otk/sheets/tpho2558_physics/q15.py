"""Lab part 2.1-2.2: through the needle alone Q = pi r^4 rho g (h - y)/(8 eta l), so the slope of Q against h gives eta = pi r^4 rho g/(8 (slope) l); 0.0112 cm^2/s with r = 0.425 mm and l = 4.0 cm gives 2.9 mPa s. Adapted with synthetic heights h (cm) and flows Q (ml/s) and the needle radius (mm); returns eta in mPa s (rho = 1030 kg/m^3)."""

from math import pi


def solve(heights=(41.2, 46.1, 51.0, 56.2, 63.2, 69.5), flows=(0.44, 0.51, 0.56, 0.62, 0.68, 0.77), radius=0.425, needle=4.0, rho=1030.0, g=9.8):
    n = len(heights)
    mx, my = sum(heights) / n, sum(flows) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(heights, flows)) / sum((x - mx) ** 2 for x in heights)
    slope_si = slope * 1e-6 / 1e-2
    return pi * (radius * 1e-3) ** 4 * rho * g / (8 * slope_si * needle * 1e-2) * 1e3


def check(heights=(41.2, 46.1, 51.0, 56.2, 63.2, 69.5), flows=(0.44, 0.51, 0.56, 0.62, 0.68, 0.77), radius=0.425, needle=4.0, rho=1030.0, g=9.8):
    # Fit by Cramer's rule, then bisect the viscosity whose Poiseuille slope matches.
    from otk.sheets.tpho2558_physics._shared import bisect, line

    slope, _ = line([h * 1e-2 for h in heights], [q * 1e-6 for q in flows])
    r, run = radius * 1e-3, needle * 1e-2
    return bisect(lambda eta: pi * r**4 * rho * g / (8 * eta * run) - slope, 1e-6, 1.0) * 1e3


PARAMS = {"heights": (41.2, 46.1, 51.0, 56.2, 63.2, 69.5), "flows": (0.44, 0.51, 0.56, 0.62, 0.68, 0.77), "radius": 0.425, "needle": 4.0, "rho": 1030.0, "g": 9.8}
VARIANTS = [{"radius": 0.40}, {"flows": (0.40, 0.46, 0.52, 0.60, 0.64, 0.71)}, {"needle": 3.0}]
ANSWER = 2.888523972550306
TOL = 1e-9
