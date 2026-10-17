"""Part2,4: smooth circular track, B is rightmost point (vertical velocity). Source release A level circle TOP C, drop to B=R. Radial force2mg and weightmg perpendicular => resultant sqrt5 mg. Return resultant/(mg), variable drop/R."""

from math import sqrt, hypot


def solve(drop_ratio=1):
    return sqrt(1 + 4 * drop_ratio**2)


def check(drop_ratio=1):
    # Construct circular position and acceleration from energy, with m2,R3,g7.
    mass, radius, g = 2.0, 3.0, 7.0
    work = mass * g * (drop_ratio * radius)
    v = sqrt(2 * work / mass)
    fx = -mass * v * v / radius
    fy = -mass * g
    return hypot(fx, fy) / (mass * g)


PARAMS = {"drop_ratio": 1}
VARIANTS = [{"drop_ratio": 2}, {"drop_ratio": 0.5}, {"drop_ratio": 1.5}]
ANSWER = 2.23606797749979
