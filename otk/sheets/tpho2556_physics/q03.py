"""Theory 1.1 (c): the jerk's impulse is the total momentum, m u + 2 m v_y = (3/2) m u (1 + sin^2 theta). Adapted: m, u and theta (degrees) vary; returns the impulse in N s."""

from math import radians, sin


def solve(mass=0.4, speed=2.0, angle=60.0):
    return 1.5 * mass * speed * (1 + sin(radians(angle)) ** 2)


def check(mass=0.4, speed=2.0, angle=60.0):
    # BC is pushed by the jerk and pulled back by both hinges.
    from otk.sheets.tpho2556_physics._rods import hinged_rod

    jy = hinged_rod(mass, 1.0, radians(angle), speed)[4]
    return mass * speed + 2 * jy


PARAMS = {"mass": 0.4, "speed": 2.0, "angle": 60.0}
VARIANTS = [{"angle": 20.0}, {"mass": 1.5}, {"speed": 0.5, "angle": 85.0}]
ANSWER = 2.1000000000000005
TOL = 1e-12
