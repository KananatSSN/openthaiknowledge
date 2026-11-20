"""Lab part 1 d): the fitted line log B = log(mu0 m/(2 pi)) + n log x (SI units) gives the moment m, and M = m/(pi R^2 L) for the short magnet (R = 5.00 mm, L = 4.00 mm): least squares on the solution's readings gives m = 0.34 A m^2 and M = 1.08e6 A/m (its drawn line, 0.38 A m^2 and 1.2e6 A/m). Adapted: the readings vary; returns 1e6 A/m."""

from math import log10, pi

from otk.sheets.tpho2565_physics.q18 import FIELDS, GAPS


def solve(gaps=GAPS, fields=FIELDS, radius=5.0, length=4.0):
    from otk.sheets.tpho2565_physics._shared import MU0, line

    slope, intercept = line([log10(x * 1e-3) for x in gaps], [log10(b * 1e-3) for b in fields])
    moment = 2 * pi / MU0 * 10**intercept
    return moment / (pi * (radius * 1e-3) ** 2 * length * 1e-3) / 1e6


def check(gaps=GAPS, fields=FIELDS, radius=5.0, length=4.0):
    from math import exp, log

    from otk.sheets.tpho2565_physics._shared import MU0, centred_line

    # fit in mm and mT with natural logs, then convert the prefactor to SI
    slope, intercept = centred_line([log(x) for x in gaps], [log(b) for b in fields])
    prefactor = exp(intercept) * 1e-3 * (1e3) ** slope  # T m^-n
    moment = 2 * pi * prefactor / MU0
    return moment / (pi * (radius * 1e-3) ** 2 * length * 1e-3) / 1e6


PARAMS = {"gaps": GAPS, "fields": FIELDS, "radius": 5.0, "length": 4.0}
VARIANTS = [
    {"fields": (10.1, 4.70, 3.62, 2.55, 2.06, 1.53, 1.28, 0.99, 0.85, 0.68, 0.59, 0.49, 0.42, 0.36)},
    {"gaps": GAPS[2:], "fields": FIELDS[2:]},
    {"length": 5.0},
]
ANSWER = 1.0845067721878772
TOL = 1e-9
