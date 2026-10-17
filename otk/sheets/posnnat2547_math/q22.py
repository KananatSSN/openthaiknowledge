"""วันที่สอง ข้อ 1 — มุม B เมื่อ A = 70° และ CA + AI = BC

Take D on BC with CD = CA. CI bisects ∠C, so triangles CAI and CDI are
congruent: DI = AI and ∠CDI = A/2. Then DB = BC − CA = AI = DI, so DBI is
isosceles with ∠DBI = ∠DIB = B/2, and the exterior angle ∠CDI = B. Hence
B = A/2 = 35°.

``check`` solves CA + AI − BC = 0 for B numerically (bisection, unit
circumradius, AI = r/sin(A/2)).
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"angle_a": 70}
ANSWER = 35
TOL = 1e-9
VARIANTS = [{"angle_a": 40}, {"angle_a": 60}, {"angle_a": 100}, {"angle_a": 118}]


def solve(angle_a=70):
    return Fraction(angle_a, 2)


def check(angle_a=70):
    a_ = math.radians(angle_a)

    def gap(b_deg):
        b_ = math.radians(b_deg)
        c_ = math.pi - a_ - b_
        a, b, c = math.sin(a_), math.sin(b_), math.sin(c_)
        s = (a + b + c) / 2
        r = math.sqrt((s - a) * (s - b) * (s - c) / s)
        return b + r / math.sin(a_ / 2) - a

    lo, hi = 1e-6, 180 - angle_a - 1e-6
    for _ in range(200):
        mid = (lo + hi) / 2
        if gap(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
