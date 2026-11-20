"""Theory 3 C.2 figure 3.6: four wires at distance R (like currents opposite each other) give B_y = 2 mu0 I x/(pi R^2) on the x axis near the centre, so a = b = 2 mu0 I/(pi R^2). Adapted: I (A) and R (cm) vary; returns b in T/m."""

from math import pi

MU0 = 4e-7 * pi


def solve(current=100.0, radius=2.0):
    return 2 * MU0 * current / (pi * (radius * 1e-2) ** 2)


def check(current=100.0, radius=2.0):
    # Sum the four wires' fields at a small offset x on the axis and divide.
    R = radius * 1e-2
    x = R * 1e-4
    wires = [((R, 0.0), 1), ((-R, 0.0), 1), ((0.0, R), -1), ((0.0, -R), -1)]
    by = 0.0
    for (wx, wy), sign in wires:
        dx, dy = x - wx, 0.0 - wy
        r2 = dx * dx + dy * dy
        # field of a +z current: (mu0 I/2 pi r^2)(-dy, dx)
        by += sign * MU0 * current / (2 * pi * r2) * dx
    return abs(by / x)


PARAMS = {"current": 100.0, "radius": 2.0}
VARIANTS = [{"current": 500.0}, {"radius": 5.0}, {"current": 50.0, "radius": 1.0}]
ANSWER = 0.20000000000000004
TOL = 1e-6
