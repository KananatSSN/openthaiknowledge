"""ข้อ 9 — AD ∥ BC ⇔ AB/CD = MP/NQ  (พิสูจน์)

MP·CD = [ACD] + [BCD] and NQ·AB = [ABC] + [ABD] (M, N midpoints); since
[ABC] + [ACD] = [ABD] + [BCD], the two agree iff [ABC] = [BCD], that is iff
AD ∥ BC. The solver returns NQ = MP·CD/AB for a trapezoid (6, 4, 3: 2).

``check`` builds a trapezoid with AD, BC horizontal at height 1 and the given
legs, bisects on the length of BC until the distance from M to line CD is MP,
then measures the distance from N to line AB.
"""

from __future__ import annotations

from fractions import Fraction
from math import hypot, sqrt

PARAMS = {"ab": 6, "cd": 4, "mp": 3}
ANSWER = 2
VARIANTS = [{"ab": 5, "cd": 3, "mp": 4}, {"ab": 8, "cd": 7, "mp": 5}, {"ab": 10, "cd": 4, "mp": 6}]
TOL = 1e-9


def solve(ab=6, cd=4, mp=3):
    return Fraction(mp * cd, ab)


def _distance(point, p, q):
    return abs((q[0] - p[0]) * (point[1] - p[1]) - (point[0] - p[0]) * (q[1] - p[1])) / hypot(q[0] - p[0], q[1] - p[1])


def _figure(ab, cd, t, h=1.0):
    A = (0.0, 0.0)
    B = (sqrt(ab * ab - h * h), h)
    C = (B[0] + t, h)
    D = (C[0] + sqrt(cd * cd - h * h), 0.0)
    return A, B, C, D


def _mp(ab, cd, t):
    A, B, C, D = _figure(ab, cd, t)
    M = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    return _distance(M, C, D)


def check(ab=6, cd=4, mp=3):
    lo, hi = 0.0, 1000.0
    assert _mp(ab, cd, lo) < mp < _mp(ab, cd, hi)
    for _ in range(200):
        mid = (lo + hi) / 2
        if _mp(ab, cd, mid) < mp:
            lo = mid
        else:
            hi = mid
    A, B, C, D = _figure(ab, cd, (lo + hi) / 2)
    N = ((C[0] + D[0]) / 2, (C[1] + D[1]) / 2)
    return _distance(N, A, B)
