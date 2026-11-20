"""Theory 1.3 b) figure 3: with end A sliding on the smooth floor, the rod (released from rest) obeys M a = Mg - N and (ML^2/12) alpha = N (L/2) cos(theta) with a = (L/2) cos(theta) alpha, so its centre B falls at 3g cos^2(theta)/(1 + 3 cos^2 theta) and end C at twice that; A does not accelerate vertically. Adapted: theta (degrees) varies; returns a_B/g."""

from math import cos, radians


def solve(angle=30.0):
    c2 = cos(radians(angle)) ** 2
    return 3 * c2 / (1 + 3 * c2)


def check(angle=30.0):
    from otk.sheets.tpho2561_physics._shared import falling_rod

    return falling_rod(radians(angle))[0] / 9.8


PARAMS = {"angle": 30.0}
VARIANTS = [{"angle": 60.0}, {"angle": 10.0}, {"angle": 50.0}]
ANSWER = 0.6923076923076924
TOL = 1e-9
