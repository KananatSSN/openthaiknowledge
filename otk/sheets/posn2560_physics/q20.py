"""Part 1,20: lens x0, convex mirror x=d=5cm,R15cm, object x=-u=-30cm. Two self-conjugate focal lengths are possible: u*d/(u+d)=30/7 upright; u*(d+R)/(u+d+R)=12 inverted. solve returns INVERTED branch only; generated question explicitly requires inverted image. No unique answer in source."""

from fractions import Fraction
import numpy as np


def solve(u=30, d=5, radius=15):
    image = d + radius
    return Fraction(u * image, u + image)


def round_trip(f, u, d, radius):
    propagation = lambda x: np.array([[1.0, x], [0.0, 1.0]])
    lens = np.array([[1.0, 0.0], [-1 / f, 1.0]])
    mirror = np.array([[1.0, 0.0], [2 / radius, 1.0]])
    return propagation(u) @ lens @ propagation(d) @ mirror @ propagation(d) @ lens @ propagation(u)


def check(u=30, d=5, radius=15):
    # Root of imaging matrix B=0 on inverted branch. Other root has A=+1.
    other = u * d / (u + d)
    lo, hi = other * (1 + 1e-7), float(u)
    sign = round_trip(lo, u, d, radius)[0, 1]
    for _ in range(100):
        f = (lo + hi) / 2
        value = round_trip(f, u, d, radius)[0, 1]
        if value * sign > 0:
            lo = f
        else:
            hi = f
    f = (lo + hi) / 2
    assert abs(round_trip(f, u, d, radius)[0, 0] + 1) < 1e-8
    return f


PARAMS = {"u": 30, "d": 5, "radius": 15}
VARIANTS = [{"u": 40}, {"d": 10}, {"radius": 20}]
ANSWER = Fraction(12, 1)
