"""Worked28 figure: uniform plate M, length L, width b, hung by a string at A, the midpoint of its top edge; m hangs from corner B at the lower end. The plate tilts theta, B side down. Balance of moments about A: M (b/2) sin = m ((L/2) cos - b sin), so tan theta = m L / (b (M + 2m))."""

from math import cos, sin


def solve(plate=4, hung=1, length=60, width=10):
    return hung * length / (width * (plate + 2 * hung))


def check(plate=4, hung=1, length=60, width=10):
    # Bisect on theta until the net torque about A of both weights vanishes.
    def torque(theta):
        # Along-edge unit (cos, sin) pointing right and up; into-plate unit
        # (sin, -cos). Horizontal coordinate of plate point (x, y): x cos + y sin.
        centre = (width / 2) * sin(theta)
        corner = (-length / 2) * cos(theta) + width * sin(theta)
        return plate * centre + hung * corner

    lo, hi = 0.0, 1.5707
    for _ in range(200):
        mid = (lo + hi) / 2
        if torque(mid) < 0:
            lo = mid
        else:
            hi = mid
    theta = (lo + hi) / 2
    return sin(theta) / cos(theta)


PARAMS = {"plate": 4, "hung": 1, "length": 60, "width": 10}
VARIANTS = [{"hung": 2}, {"plate": 1, "hung": 3, "length": 40, "width": 20}, {"width": 30}]
TOL = 1e-9
ANSWER = 1.0
