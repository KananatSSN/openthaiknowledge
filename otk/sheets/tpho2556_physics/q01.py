"""Theory 1.1 (a) figure: angular momentum of CD about the hinge point C is unchanged by the hinge impulse, so (ml^2/3) w = -(m l u cos theta)/2 and CD's centre moves at v_x = (3/4) u sin theta cos theta, v_y = u (1 - (3/4) cos^2 theta). Adapted: theta (degrees) and u vary; returns v_y in m/s."""

from math import cos, radians


def solve(angle=60.0, speed=2.0):
    return speed * (1 - 0.75 * cos(radians(angle)) ** 2)


def check(angle=60.0, speed=2.0):
    from otk.sheets.tpho2556_physics._rods import hinged_rod

    return hinged_rod(1.0, 1.0, radians(angle), speed)[1]


PARAMS = {"angle": 60.0, "speed": 2.0}
VARIANTS = [{"angle": 30.0}, {"speed": 5.0}, {"angle": 80.0, "speed": 1.0}]
ANSWER = 1.6249999999999998
TOL = 1e-12
