"""Theory II.a figure: a hoop (mass M, radius R) rolls on a fixed rod (radius r); with zero potential at the rod's top contact, PE = -M g (r + (R - r) cos theta). Joules."""

from math import cos, radians, sin


def solve(mass=2, hoop=0.5, rod=0.1, angle=60, g=10):
    return -mass * g * (rod + (hoop - rod) * cos(radians(angle)))


def check(mass=2, hoop=0.5, rod=0.1, angle=60, g=10):
    # Rolling-contact geometry: the contact point is on the rod at angle
    # theta from its top; the hoop's centre lies on the same radial line, a
    # distance R from the contact point, beyond the rod's centre. Heights are
    # measured from A, the rod's top (r above the rod's centre).
    t = radians(angle)
    contact = (rod * sin(t), rod * cos(t))  # rod centre at the origin
    centre = (contact[0] - hoop * sin(t), contact[1] - hoop * cos(t))
    return mass * g * (centre[1] - rod)

PARAMS = {"mass": 2, "hoop": 0.5, "rod": 0.1, "angle": 60, "g": 10}
VARIANTS = [{"angle": 0}, {"mass": 5, "hoop": 1.0}, {"angle": 90, "rod": 0.2}]
ANSWER = -6.000000000000001
