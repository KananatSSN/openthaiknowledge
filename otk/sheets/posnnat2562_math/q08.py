"""ข้อ 8 — K, D, M อยู่บนเส้นตรงเดียวกัน  (พิสูจน์)

K, D, M lie on one chord of ω, so KD·DM is D's power BD·DC = (s − b)(s − c).
The solver returns that product (13, 14, 15: 42).

``check`` builds the figure: the circumcircle, I and D, K as the second
intersection of ω with the circle on diameter AI (the reflection of A in the
line of centres), M as the second intersection of AI with ω. It asserts K, D, M
are collinear and returns KD·DM.
"""

from __future__ import annotations

from fractions import Fraction
from math import hypot, sqrt

PARAMS = {"a": 13, "b": 14, "c": 15}
ANSWER = 42
VARIANTS = [{"a": 7, "b": 8, "c": 9}, {"a": 6, "b": 5, "c": 9}, {"a": 10, "b": 12, "c": 8}]
TOL = 1e-9


def solve(a=13, b=14, c=15):
    s = Fraction(a + b + c, 2)
    return (s - b) * (s - c)


def _reflect(p, u, v):
    dx, dy = v[0] - u[0], v[1] - u[1]
    t = ((p[0] - u[0]) * dx + (p[1] - u[1]) * dy) / (dx * dx + dy * dy)
    fx, fy = u[0] + t * dx, u[1] + t * dy
    return (2 * fx - p[0], 2 * fy - p[1])


def check(a=13, b=14, c=15):
    B, C = (0.0, 0.0), (float(a), 0.0)
    ax = (a * a + c * c - b * b) / (2 * a)
    A = (ax, sqrt(c * c - ax * ax))
    per = a + b + c
    inc = ((a * A[0] + b * B[0] + c * C[0]) / per, (a * A[1] + b * B[1] + c * C[1]) / per)
    D = (inc[0], 0.0)
    oy = (A[0] ** 2 + A[1] ** 2 - a * A[0]) / (2 * A[1])
    centre = (a / 2, oy)
    R = hypot(centre[0], centre[1])
    mid = ((A[0] + inc[0]) / 2, (A[1] + inc[1]) / 2)
    K = _reflect(A, centre, mid)
    # M: A + t(I − A) on ω, t ≠ 0
    dx, dy = inc[0] - A[0], inc[1] - A[1]
    t = -2 * ((A[0] - centre[0]) * dx + (A[1] - centre[1]) * dy) / (dx * dx + dy * dy)
    M = (A[0] + t * dx, A[1] + t * dy)
    assert abs(hypot(M[0] - centre[0], M[1] - centre[1]) - R) < 1e-9
    assert abs(hypot(K[0] - centre[0], K[1] - centre[1]) - R) < 1e-9
    cross = (K[0] - D[0]) * (M[1] - D[1]) - (K[1] - D[1]) * (M[0] - D[0])
    assert abs(cross) < 1e-9
    return hypot(K[0] - D[0], K[1] - D[1]) * hypot(M[0] - D[0], M[1] - D[1])
