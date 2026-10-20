"""Lab part 6: the field's vertical and horizontal parts make tan(gamma) = B_v/B_h; 0.133 G and 0.41 G give gamma = 0.312 rad = 17.9 degrees. Adapted: B_v and B_h (G) vary; returns gamma in degrees."""

from math import atan, degrees


def solve(vertical=0.133, horizontal=0.41):
    return degrees(atan(vertical / horizontal))


def check(vertical=0.133, horizontal=0.41):
    # Angle of the total field vector below the horizontal via its sine.
    from math import asin, hypot

    return degrees(asin(vertical / hypot(vertical, horizontal)))


PARAMS = {"vertical": 0.133, "horizontal": 0.41}
VARIANTS = [{"vertical": 0.25}, {"horizontal": 0.30}, {"vertical": 0.45, "horizontal": 0.2}]
ANSWER = 17.972557119343772
TOL = 1e-9
