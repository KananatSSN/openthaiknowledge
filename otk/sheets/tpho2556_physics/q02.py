"""Theory 1.1 (b): about the hinge C, (ml^2/12) w + m (l/2)^2 w + m (l/2) u cos theta = 0, so CD turns at w = 3u cos theta/(2l). Adapted: theta (degrees), u and l vary; returns w in rad/s."""

from math import cos, radians


def solve(angle=60.0, speed=2.0, length=0.5):
    return 3 * speed * cos(radians(angle)) / (2 * length)


def check(angle=60.0, speed=2.0, length=0.5):
    from otk.sheets.tpho2556_physics._rods import hinged_rod

    return abs(hinged_rod(1.0, length, radians(angle), speed)[2])


PARAMS = {"angle": 60.0, "speed": 2.0, "length": 0.5}
VARIANTS = [{"angle": 30.0}, {"length": 1.2}, {"speed": 4.0, "angle": 10.0}]
ANSWER = 3.000000000000001
TOL = 1e-12
