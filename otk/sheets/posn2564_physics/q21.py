"""MC21 figure: prism with a 90 deg apex, index mu; ray enters the first face at incidence i, refracts, then meets the second face at theta from its normal and is totally reflected. With r + theta = 90 deg, cos theta = sin i / mu (answer 1). Requires total reflection: sin theta >= 1/mu."""

from math import asin, acos, cos, sin


def solve(index=1.5, sine=0.6):
    return sine / index


def check(index=1.5, sine=0.6):
    # Coordinates: apex at origin, faces along the +x and +y axes (90 deg apart).
    # The ray enters through the face on the x axis (outward normal (0, -1)).
    incidence = asin(sine)
    inside = asin(sine / index)
    # Direction inside: rotate the inward normal (0, 1) by the refraction angle.
    d = (sin(inside), cos(inside))
    # It then meets the face on the y axis, whose normal is (1, 0).
    cos_theta = abs(d[0] * 1 + d[1] * 0)
    theta = acos(cos_theta)
    assert sin(theta) >= 1 / index - 1e-12  # total reflection does happen
    assert abs(sin(incidence) - index * sin(inside)) < 1e-12
    return cos(theta)


PARAMS = {"index": 1.5, "sine": 0.6}
VARIANTS = [{"index": 2, "sine": 0.8}, {"index": 5 / 3, "sine": 0.6}, {"index": 1.6, "sine": 5 / 13}]
ANSWER = 0.39999999999999997
