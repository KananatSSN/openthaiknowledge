"""Lab part 3 b): measuring the perpendicular field on the plane through the magnet's middle in rings 1 cm wide centred at x = 1, 2, ... 10 cm, each ring of area 2 pi x dx carries B times its area; the solution's readings add to 8.90e-5 Wb. Adapted: the readings vary; returns 1e-5 Wb."""

from math import pi

RINGS = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0)
FIELDS = (41.04, 18.30, 7.25, 3.14, 1.75, 1.06, 0.66, 0.46, 0.36, 0.30)


def solve(rings=RINGS, fields=FIELDS, width=1.0):
    return sum(b * 1e-3 * 2 * pi * x * 1e-2 * width * 1e-2 for x, b in zip(rings, fields)) / 1e-5


def check(rings=RINGS, fields=FIELDS, width=1.0):
    # each ring as the difference of two discs
    total = 0.0
    for x, b in zip(rings, fields):
        outer, inner = (x + width / 2) * 1e-2, (x - width / 2) * 1e-2
        total += b * 1e-3 * pi * (outer**2 - inner**2)
    return total / 1e-5


PARAMS = {"rings": RINGS, "fields": FIELDS, "width": 1.0}
VARIANTS = [
    {"fields": (40.0, 19.1, 7.6, 3.3, 1.8, 1.1, 0.7, 0.5, 0.4, 0.3)},
    {"rings": RINGS[:6], "fields": FIELDS[:6]},
    {"width": 0.5, "rings": (0.5, 1.0, 1.5, 2.0, 2.5), "fields": (60.0, 41.0, 27.0, 18.3, 11.0)},
]
ANSWER = 8.896990394966293
TOL = 1e-9
