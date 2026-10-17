"""ข้อ 4 — EG : GF เมื่อ AC = 16, BC = 12, CE = 3CF และ G = EF ∩ CM

With C the origin, E = (CE/AC)·a, F = (CF/BC)·b and G a multiple of a + b:
EG : GF = k·BC : AC = 36 : 16 = 9 : 4. The answer is the reduced pair.

``check`` builds a triangle in coordinates, intersects EF with the median CM
and measures the two pieces (with a fixed CF).
"""

from __future__ import annotations

import math
from fractions import Fraction
from math import gcd

PARAMS = {"ac": 16, "bc": 12, "k": 3}
ANSWER = (9, 4)
TOL = 1e-9
VARIANTS = [{"ac": 9, "bc": 23, "k": 2}, {"ac": 30, "bc": 5, "k": 4}, {"ac": 10, "bc": 10, "k": 5}]


def solve(ac=16, bc=12, k=3):
    p, q = k * bc, ac
    g = gcd(p, q)
    return (p // g, q // g)


def check(ac=16, bc=12, k=3):
    angle = 1.1
    a = (float(ac), 0.0)
    b = (bc * math.cos(angle), bc * math.sin(angle))
    cf = min(bc, ac / k) / 2
    e = (a[0] * k * cf / ac, 0.0)
    f = (b[0] * cf / bc, b[1] * cf / bc)
    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    # E + s(F − E) = t·M
    d1, d2 = (f[0] - e[0], f[1] - e[1]), m
    det = d1[0] * (-d2[1]) - (-d2[0]) * d1[1]
    s = ((-e[0]) * (-d2[1]) - (-d2[0]) * (-e[1])) / det
    ratio = Fraction(s / (1 - s)).limit_denominator(1000)
    return (ratio.numerator, ratio.denominator)
