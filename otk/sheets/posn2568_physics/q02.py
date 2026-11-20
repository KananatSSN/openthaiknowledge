"""Short2 figure: equal smooth spheres, elastic; B leaves along the line of centres, 30 deg below u. A keeps the component of u perpendicular to that line: |v_A| = u sin 30 = u/2. Adapted: any line angle by its sine."""

from math import asin, cos, sin, sqrt


def solve(speed=10, sine=0.5):
    return speed * sine


def check(speed=10, sine=0.5):
    # Equal-mass elastic impulse along the unit normal n = (cos p, -sin p).
    p = asin(sine)
    n = (cos(p), -sin(p))
    j = speed * n[0]  # normal component handed to B
    va = (speed - j * n[0], -j * n[1])
    vb = (j * n[0], j * n[1])
    assert abs(va[0] ** 2 + va[1] ** 2 + vb[0] ** 2 + vb[1] ** 2 - speed**2) < 1e-9
    return sqrt(va[0] ** 2 + va[1] ** 2)


PARAMS = {"speed": 10, "sine": 0.5}
VARIANTS = [{"sine": 0.6}, {"speed": 13, "sine": 5 / 13}, {"sine": 0.8}]
ANSWER = 5.0
