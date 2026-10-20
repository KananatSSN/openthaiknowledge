"""Theory 1.1 (a) figure: rays from the Sun's two edges cross at the pinhole of diameter a, so the image on a screen L behind it has diameter A = a + L theta for the Sun's angular size theta. Adapted: a (mm), L (cm) and theta vary; returns A in mm."""


def solve(hole=0.5, depth=20.0, angle=0.0093):
    return hole + depth * 10 * angle


def check(hole=0.5, depth=20.0, angle=0.0093):
    # Trace the extreme rays: from the top edge of the Sun through the
    # bottom of the hole and from the bottom edge through the top.
    from math import tan

    top = hole / 2 + depth * 10 * tan(angle / 2)
    return 2 * top


PARAMS = {"hole": 0.5, "depth": 20.0, "angle": 0.0093}
VARIANTS = [{"hole": 1.0}, {"depth": 50.0}, {"angle": 0.0045, "hole": 0.3}]
ANSWER = 2.36
TOL = 1e-4
