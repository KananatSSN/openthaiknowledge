"""Theory II.d: small swings of the hoop on the rod: frequency (1/2 pi) sqrt(g/(2(R - r))). Returns the period 2 pi sqrt(2(R - r)/g) / pi in seconds-per-pi units: T/pi."""

from math import pi, sin, sqrt


def solve(hoop=0.5, rod=0.1, g=10):
    return 2 * sqrt(2 * (hoop - rod) / g)


def check(hoop=0.5, rod=0.1, g=10):
    # Integrate theta'' = -g sin(theta)/(2(R - r)) at tiny amplitude and time
    # successive zero crossings.
    a, w, t, dt = 1e-4, 0.0, 0.0, 1e-5
    crossings = []
    while len(crossings) < 3:
        w -= g * sin(a) / (2 * (hoop - rod)) * dt
        new = a + w * dt
        if (a > 0) != (new > 0):
            crossings.append(t)
        a = new
        t += dt
    return (crossings[2] - crossings[0]) / pi


PARAMS = {"hoop": 0.5, "rod": 0.1, "g": 10}
VARIANTS = [{"rod": 0.3}, {"hoop": 2.0, "rod": 0.0}, {"hoop": 1.3, "rod": 0.5}]
TOL = 1e-3
ANSWER = 0.565685424949238
