"""ข้อ 3 — รัศมีวงกลมวงที่สองในมุม A เมื่อ ∠B = 90°, AB = √3, BC = 3

tan A = BC/AB = √3, so A = 60°. The first circle touches AB at B and AC:
radius AB·tan 30° = 1. Circles in an angle of half-width 30° have consecutive
radii in ratio (1 − sin 30°)/(1 + sin 30°) = 1/3, so the second radius is 1/3
(AB = k√3, BC = 3k gives k/3).

``check`` places the first circle and bisects along the bisector of A for the
circle that touches it externally.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"k": 1}
ANSWER = Fraction(1, 3)
TOL = 1e-9
VARIANTS = [{"k": 2}, {"k": 5}, {"k": 12}]


def solve(k=1):
    return Fraction(k, 3)


def check(k=1):
    ab, bc = k * math.sqrt(3), 3 * k
    half = math.atan2(bc, ab) / 2
    r1 = ab * math.tan(half)
    u = (math.cos(half), math.sin(half))

    def gap(t):
        return math.dist((t * u[0], t * u[1]), (ab, r1)) - (r1 + t * math.sin(half))

    lo, hi = 1e-12, math.hypot(ab, r1) * 0.999
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if gap(mid) > 0 else (lo, mid)
    return lo * math.sin(half)
