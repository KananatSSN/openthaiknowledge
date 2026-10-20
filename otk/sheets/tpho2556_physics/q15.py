"""Theory 3 (b)-(d) figure: d(alpha) = 2(N + 1) d(phi) - 2 d(theta) vanishes for the brightest light, so d(phi)/d(theta) = 1/(N + 1); with Snell's law this gives cos^2 theta = (n^2 - 1)/((N + 1)^2 - 1). Adapted: n and N vary; returns theta in degrees."""

from math import acos, degrees, sqrt


def solve(index=1.33, reflections=1):
    return degrees(acos(sqrt((index**2 - 1) / ((reflections + 1) ** 2 - 1))))


def check(index=1.33, reflections=1):
    from otk.sheets.tpho2556_physics._bow import stationary

    return degrees(stationary(index, reflections))


PARAMS = {"index": 1.33, "reflections": 1}
VARIANTS = [{"reflections": 2}, {"index": 1.343}, {"index": 1.331, "reflections": 2}]
ANSWER = 59.58491694941694
TOL = 1e-5
