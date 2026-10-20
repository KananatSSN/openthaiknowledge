"""Lab 1 figure 1: a square coil (N turns, side a, current i) gives on its axis at distance x the field B = (mu0 a^2 i N/(2 pi)) / ((x^2 + (a/2)^2) sqrt(x^2 + 2(a/2)^2)). Adapted: the 130-turn coil with i = 4.8 V/5.2 ohm; a and x in cm; returns B in gauss."""

from math import pi, sqrt


def solve(side=10.0, distance=5.0, turns=130, current=4.8 / 5.2):
    a, x = side / 100, distance / 100
    b = 4e-7 * pi * a * a * current * turns / (2 * pi) / ((x * x + a * a / 4) * sqrt(x * x + a * a / 2))
    return b * 1e4


def check(side=10.0, distance=5.0, turns=130, current=4.8 / 5.2):
    # Biot-Savart summed over the four sides, field component along the axis.
    a, x = side / 100, distance / 100
    mu = 4e-7 * pi
    total = 0.0
    n = 4000
    half = a / 2
    corners = [(half, half), (-half, half), (-half, -half), (half, -half)]
    for k in range(4):
        (y1, z1), (y2, z2) = corners[k], corners[(k + 1) % 4]
        for i in range(n):
            s = (i + 0.5) / n
            y, z = y1 + (y2 - y1) * s, z1 + (z2 - z1) * s
            dy, dz = (y2 - y1) / n, (z2 - z1) / n
            rx, ry, rz = x, -y, -z
            r3 = (rx * rx + ry * ry + rz * rz) ** 1.5
            # dl x r, x component
            cross_x = dy * rz - dz * ry
            total += mu * turns * current / (4 * pi) * cross_x / r3
    return abs(total) * 1e4


PARAMS = {"side": 10.0, "distance": 5.0, "turns": 130, "current": 4.8 / 5.2}
VARIANTS = [{"distance": 0.0}, {"side": 6.0, "distance": 10.0}, {"distance": 20.0}]
ANSWER = 5.542562584220406
TOL = 1e-5
