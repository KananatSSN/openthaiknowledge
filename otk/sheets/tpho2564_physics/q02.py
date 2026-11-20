"""Theory 1.1 b), d): rolling at phi to the steepest slope needs friction f1 = (m'g/2) sin(theta) cos(phi) along the motion and f2 = m'g sin(theta) sin(phi) across it, so mu >= (1/2) tan(theta) sqrt(1 + 3 sin^2(phi)) (phi = 0 gives tan(theta)/2). Adapted: theta and phi (degrees) vary."""

from math import radians, sin, sqrt, tan


def solve(incline=30.0, slant=40.0):
    return 0.5 * tan(radians(incline)) * sqrt(1 + 3 * sin(radians(slant)) ** 2)


def check(incline=30.0, slant=40.0, mass=1.0):
    from math import cos, hypot

    t, p = radians(incline), radians(slant)
    along = mass * 9.81 * sin(t) * cos(p) / 2  # torque friction from 1.1 c)
    across = mass * 9.81 * sin(t) * sin(p)  # no sideways motion
    return hypot(along, across) / (mass * 9.81 * cos(t))


PARAMS = {"incline": 30.0, "slant": 40.0}
VARIANTS = [{"slant": 0.0}, {"incline": 15.0}, {"slant": 70.0}]
ANSWER = 0.43200383230356526
TOL = 1e-9
