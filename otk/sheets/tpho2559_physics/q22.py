"""Lab part 3: the first-order line of a grating with spacing d = 1.6 um leaves at d sin(theta) = lambda; 21 degrees gives 573 nm. Adapted: the angle (degrees) and spacing (um) vary; returns lambda in nm."""

from math import radians, sin


def solve(angle=21.0, spacing=1.6):
    return spacing * 1e3 * sin(radians(angle))


def check(angle=21.0, spacing=1.6):
    # Bisect the wavelength whose first-order path difference across one
    # groove is one wavelength.
    from otk.sheets.tpho2559_physics._shared import bisect

    return bisect(lambda lam: spacing * 1e3 * sin(radians(angle)) / lam - 1, 1.0, 1e4)


PARAMS = {"angle": 21.0, "spacing": 1.6}
VARIANTS = [{"angle": 15.0}, {"angle": 28.0}, {"spacing": 1.5, "angle": 25.0}]
ANSWER = 573.3887192724804
TOL = 1e-9
