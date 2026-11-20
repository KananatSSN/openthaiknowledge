"""Lab part 2 c): in an iron loop with an air gap 2d the field at the gap's centre is B_g = 2 B0 (1 - d/sqrt(d^2 + R^2)), so the slope of B_g against (1 - d/sqrt(d^2 + R^2)) is 2 B0: the solution's readings (R = 5.0 mm) give 53.9 mT, B0 = 26.9 mT and B0/B_pole = 0.048 for B_pole = 560 mT. Adapted: the readings vary; returns mT."""

from math import sqrt

GAPS = (6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0)
FIELDS = (28.5, 21.2, 16.8, 14.0, 12.2, 10.0, 8.5, 7.0, 6.5, 6.0)


def solve(gaps=GAPS, fields=FIELDS, radius=5.0):
    from otk.sheets.tpho2565_physics._shared import line

    shape = [1 - (g / 2) / sqrt((g / 2) ** 2 + radius**2) for g in gaps]
    return line(shape, fields)[0] / 2


def check(gaps=GAPS, fields=FIELDS, radius=5.0):
    from math import atan, cos

    from otk.sheets.tpho2565_physics._shared import centred_line

    # d/sqrt(d^2 + R^2) is the cosine of arctan(R/d)
    shape = [1 - cos(atan(radius / (g / 2))) for g in gaps]
    return centred_line(shape, fields)[0] / 2


PARAMS = {"gaps": GAPS, "fields": FIELDS, "radius": 5.0}
VARIANTS = [
    {"fields": (31.0, 23.5, 18.4, 15.1, 12.8, 10.9, 9.2, 7.9, 7.0, 6.2)},
    {"radius": 4.0},
    {"gaps": GAPS[:7], "fields": FIELDS[:7]},
]
ANSWER = 26.947593882895948
TOL = 1e-9
