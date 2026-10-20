"""Lab part 1 figure 1: a heap of height h on a base of radius r stands at tan(alpha2) = h/r. Adapted: h and r (cm) vary; returns alpha2 in degrees."""

from math import atan, degrees


def solve(height=5.0, radius=9.0):
    return degrees(atan(height / radius))


def check(height=5.0, radius=9.0):
    # Bisect the angle whose cone of base r reaches height h.
    from math import radians, tan

    from otk.sheets.tpho2561_physics._shared import bisect

    return bisect(lambda a: radius * tan(radians(a)) - height, 0.0, 89.0)


PARAMS = {"height": 5.0, "radius": 9.0}
VARIANTS = [{"height": 7.0}, {"radius": 12.0}, {"height": 3.5, "radius": 6.0}]
ANSWER = 29.054604099077146
TOL = 1e-9
