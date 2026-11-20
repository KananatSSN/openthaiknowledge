"""Lab part 1 c): far along a magnet's axis B is proportional to x^n, so log B against log x is a straight line of slope n; the solution's short-magnet readings (x = 17 to 52 mm) give n = -2.90 by least squares (its drawn line, -2.86; a dipole gives -3). Adapted: the readings vary."""

from math import log10

GAPS = (17, 22, 24, 27, 29, 32, 34, 37, 39, 42, 44, 47, 49, 52)
FIELDS = (9.238, 4.398, 3.450, 2.392, 1.929, 1.477, 1.213, 0.959, 0.816, 0.672, 0.573, 0.496, 0.430, 0.364)


def solve(gaps=GAPS, fields=FIELDS):
    from otk.sheets.tpho2565_physics._shared import line

    return line([log10(x) for x in gaps], [log10(b) for b in fields])[0]


def check(gaps=GAPS, fields=FIELDS):
    from math import log

    from otk.sheets.tpho2565_physics._shared import centred_line

    # natural logs give the same slope
    return centred_line([log(x) for x in gaps], [log(b) for b in fields])[0]


PARAMS = {"gaps": GAPS, "fields": FIELDS}
VARIANTS = [
    {"fields": (10.1, 4.70, 3.62, 2.55, 2.06, 1.53, 1.28, 0.99, 0.85, 0.68, 0.59, 0.49, 0.42, 0.36)},
    {"gaps": GAPS[2:], "fields": FIELDS[2:]},
    {"gaps": GAPS[:10], "fields": FIELDS[:10]},
]
ANSWER = -2.899502459974074
TOL = 1e-9
