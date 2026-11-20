"""Short27 figure: inside ice of index mu a ray meets a parallel-sided air gap (mu ~ 1) of width D at theta to the face normal, crosses it and continues parallel to its first direction. x is the perpendicular distance between the leaving ray and the incident line extended. sin phi = mu sin theta (needs mu sin theta < 1); x = D sin(phi - theta)/cos phi = D sin theta (mu cos theta / sqrt(1 - mu^2 sin^2 theta) - 1)."""

from math import asin, cos, sin, sqrt


def solve(width=15, index=4 / 3, sine=0.6):
    cosine = sqrt(1 - sine * sine)
    return width * sine * (index * cosine / sqrt(1 - (index * sine) ** 2) - 1)


def check(width=15, index=4 / 3, sine=0.6):
    # Coordinates: gap faces are x = 0 and x = D; ray hits (0, 0) going at theta.
    theta = asin(sine)
    phi = asin(index * sine)
    exit_point = (width, width * sin(phi) / cos(phi))
    # Distance from exit_point to the incident line through the origin.
    direction = (cos(theta), sin(theta))
    return abs(exit_point[1] * direction[0] - exit_point[0] * direction[1])


PARAMS = {"width": 15, "index": 4 / 3, "sine": 0.6}
VARIANTS = [{"index": 1.2, "sine": 0.6}, {"width": 13, "index": 1.3, "sine": 5 / 13}, {"index": 1.5, "sine": 0.5}]
ANSWER = 6.999999999999997
