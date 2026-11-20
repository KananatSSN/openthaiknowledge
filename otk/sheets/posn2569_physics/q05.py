"""MC5 figure: glass slab of thickness L; incidence i, refraction theta; the emergent ray is shifted L sin(i - theta)/cos(theta) (answer 6). Inputs: sin i and sin theta."""

from math import asin, cos, sin


def solve(thickness=10, sin_in=0.8, sin_glass=0.6):
    i, t = asin(sin_in), asin(sin_glass)
    return thickness * sin(i - t) / cos(t)


def check(thickness=10, sin_in=0.8, sin_glass=0.6):
    # Coordinates: faces x = 0 and x = L; entry at the origin; distance from the
    # exit point to the incident line through the origin.
    i, t = asin(sin_in), asin(sin_glass)
    exit_point = (thickness, thickness * sin(t) / cos(t))
    d = (cos(i), sin(i))
    return abs(exit_point[0] * d[1] - exit_point[1] * d[0])


PARAMS = {"thickness": 10, "sin_in": 0.8, "sin_glass": 0.6}
VARIANTS = [{"sin_in": 0.6, "sin_glass": 0.4}, {"thickness": 13, "sin_in": 12 / 13, "sin_glass": 0.6}, {"sin_in": 0.5, "sin_glass": 0.3}]
ANSWER = 3.500000000000001
