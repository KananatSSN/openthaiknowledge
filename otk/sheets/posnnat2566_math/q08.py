"""ข้อ 8 — EF = PQ + AB  (พิสูจน์)

With A = (−a, 0), B = (a, 0), C = (u, v) and R² = u² + v² the circumcircle's
centre distance data, the construction gives PQ = 2a(R² − a²)/(R² + a²), and
EF = PQ + AB. The solver returns PQ (a, u, v = 3, 1, 5: 102/35).

``check`` builds the circumcircle, T from the tangents at A and B, D = CT ∩ AB,
the circles CAD and CBD, E and F as their second meetings with TA and TB, and P,
Q on AC, BC; it asserts EF = PQ + AB and returns PQ.
"""

from __future__ import annotations

from fractions import Fraction
from math import hypot

PARAMS = {"a": 3, "u": 1, "v": 5}
ANSWER = Fraction(102, 35)
VARIANTS = [{"a": 2, "u": -1, "v": 4}, {"a": 5, "u": 3, "v": 7}, {"a": 4, "u": 0, "v": 9}]
TOL = 1e-9


def solve(a=3, u=1, v=5):
    r2 = u * u + v * v
    return Fraction(2 * a * (r2 - a * a), r2 + a * a)


def _circumcentre(p, q, r):
    ax, ay = p
    bx, by = q
    cx, cy = r
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return ux, uy


def _meet(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


def _second(on, toward, centre):
    dx, dy = toward[0] - on[0], toward[1] - on[1]
    t = -2 * ((on[0] - centre[0]) * dx + (on[1] - centre[1]) * dy) / (dx * dx + dy * dy)
    return (on[0] + t * dx, on[1] + t * dy)


def check(a=3, u=1, v=5):
    A, B, C = (-float(a), 0.0), (float(a), 0.0), (float(u), float(v))
    centre = _circumcentre(A, B, C)
    tA = (A[0] - (A[1] - centre[1]), A[1] + (A[0] - centre[0]))  # A + perpendicular to OA
    tB = (B[0] - (B[1] - centre[1]), B[1] + (B[0] - centre[0]))
    T = _meet(A, tA, B, tB)
    D = _meet(C, T, A, B)
    E = _second(A, T, _circumcentre(C, A, D))
    F = _second(B, T, _circumcentre(C, B, D))
    P = _meet(E, F, A, C)
    Q = _meet(E, F, B, C)
    ef, pq = hypot(E[0] - F[0], E[1] - F[1]), hypot(P[0] - Q[0], P[1] - Q[1])
    assert abs(ef - (pq + 2 * a)) < 1e-9
    return pq
