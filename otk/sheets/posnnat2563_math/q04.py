"""ข้อ 4 — XY ผ่านจุดกึ่งกลางของ DP  (พิสูจน์)

With D = (0, 0), A = (0, h), B = (−u, 0), C = (v, 0) (acute: h² > uv), the
foot of the altitudes gives P = AD ∩ EF at height 2huv/(h² + uv), and the two
tangents at D meet AB, AC at X, Y whose line crosses AD at half that. The
solver returns DM = huv/(h² + uv) (3, 4, 6: 3/2).

``check`` builds E, F, P, the two circumcircles, their tangents at D, X and Y,
and M = XY ∩ AD; it asserts M is the midpoint of DP and returns DM.
"""

from __future__ import annotations

from fractions import Fraction
from math import hypot

PARAMS = {"left": 3, "right": 4, "height": 6}
ANSWER = Fraction(3, 2)
VARIANTS = [{"left": 2, "right": 9, "height": 5}, {"left": 5, "right": 5, "height": 6},
            {"left": 7, "right": 3, "height": 12}]
TOL = 1e-9


def solve(left=3, right=4, height=6):
    return Fraction(height * left * right, height * height + left * right)


def _meet(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


def _foot(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)
    return (a[0] + t * dx, a[1] + t * dy)


def _circumcentre(p, q, r):
    ax, ay = p
    bx, by = q
    cx, cy = r
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return ux, uy


def check(left=3, right=4, height=6):
    D, A = (0.0, 0.0), (0.0, float(height))
    B, C = (-float(left), 0.0), (float(right), 0.0)
    E = _foot(B, A, C)
    F = _foot(C, A, B)
    P = _meet(A, D, E, F)
    tangents = []
    for tri, side in (((A, D, C), (A, B)), ((A, D, B), (A, C))):
        o = _circumcentre(*tri)
        direction = (-(o[1] - D[1]), o[0] - D[0])  # perpendicular to the radius at D
        tangents.append(_meet(D, (D[0] + direction[0], D[1] + direction[1]), *side))
    X, Y = tangents
    M = _meet(X, Y, A, D)
    assert abs(M[1] - P[1] / 2) < 1e-9 and abs(M[0]) < 1e-9
    return hypot(*M)
