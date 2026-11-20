"""Theory 1.3 b)-c): end C falls at 6g cos^2(theta)/(1 + 3 cos^2 theta); every string stays slack only while the rod's points fall no faster than the free masses (g), which fails first at C unless cos^2(theta) <= 1/3, theta >= 54.7 degrees. Adapted: theta (degrees) varies; returns a_C/g."""

from math import cos, radians


def solve(angle=30.0):
    c2 = cos(radians(angle)) ** 2
    return 6 * c2 / (1 + 3 * c2)


def check(angle=30.0):
    # C's acceleration from the rod's linear system: a_C = a_cm + (L/2) cos(theta) alpha.
    from otk.sheets.tpho2561_physics._shared import falling_rod

    a, alpha, _ = falling_rod(radians(angle))
    return (a + 0.5 * cos(radians(angle)) * alpha) / 9.8


PARAMS = {"angle": 30.0}
VARIANTS = [{"angle": 60.0}, {"angle": 10.0}, {"angle": 54.7356103172}]
ANSWER = 1.3846153846153848
TOL = 1e-9
