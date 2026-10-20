"""Theory 1.2 e): the half cylinder slides without turning, so the contact force points through its centre of mass; its flat face settles at beta = theta - arctan[(m'/(2m' + m)) tan(theta)] to the horizontal. Adapted: both masses (kg) and theta (degrees) vary; returns degrees."""

from math import atan, degrees, radians, tan


def solve(tube=1.0, half=0.5, incline=30.0):
    t = radians(incline)
    return degrees(t - atan(tube / (2 * tube + half) * tan(t)))


def check(tube=1.0, half=0.5, incline=30.0):
    from math import cos, sin

    from otk.sheets.tpho2564_physics import q03

    # forces on the half cylinder: mg and N1, which tilts theta - beta from the normal
    t = radians(incline)
    a = q03.check(tube=tube, half=half, incline=incline)
    return degrees(t - atan((9.81 * sin(t) - a) / (9.81 * cos(t))))


PARAMS = {"tube": 1.0, "half": 0.5, "incline": 30.0}
VARIANTS = [{"half": 2.0}, {"incline": 20.0}, {"tube": 0.3}]
ANSWER = 16.996088057177182
TOL = 1e-9
