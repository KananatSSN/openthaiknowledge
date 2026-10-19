"""Theory II.c: d/dt of M(R - r)^2 theta'^2 - M g (R - r) cos theta = const gives theta'' = -g sin theta/(2(R - r)). rad/s^2 at a given angle."""

from math import cos, radians, sin


def solve(hoop=0.5, rod=0.1, angle=30, g=10):
    return -g * sin(radians(angle)) / (2 * (hoop - rod))


def check(hoop=0.5, rod=0.1, angle=30, g=10, mass=1.0):
    # Differentiate the energy numerically: E(theta, w) = M(R-r)^2 w^2
    # + PE(theta); along a path dE/dt = 0 gives 2M(R-r)^2 w a = -dPE/dtheta w.
    h = 1e-6
    pe = lambda t: -mass * g * (rod + (hoop - rod) * cos(t))
    t = radians(angle)
    dpe = (pe(t + h) - pe(t - h)) / (2 * h)
    return -dpe / (2 * mass * (hoop - rod) ** 2)


PARAMS = {"hoop": 0.5, "rod": 0.1, "angle": 30, "g": 10}
VARIANTS = [{"angle": 90}, {"hoop": 1.0, "rod": 0.2}, {"angle": 10, "rod": 0.0}]
TOL = 1e-7
ANSWER = -6.249999999999998
