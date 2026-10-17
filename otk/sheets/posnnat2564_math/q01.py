"""ข้อ 1 — M เป็นจุดกึ่งกลางของ BC  (พิสูจน์)

Reflection in the axis AH swaps the tangent pairs from B and from C, so the
line through a tangent point from B and the non-mirror tangent point from C is
symmetric about AH's foot and meets BC at H, the midpoint. The solver returns
BM = BH = √(AB² − AH²) (5, 4: 3).

``check`` places H at the origin, finds both tangent points from B and from C
to the circle of radius r about A, and for every pairing whose line is not
parallel to BC confirms it meets BC at H; it returns BM.
"""

from __future__ import annotations

from math import hypot, isqrt, sqrt

PARAMS = {"leg": 5, "altitude": 4, "radius": 2}
ANSWER = 3
VARIANTS = [{"leg": 13, "altitude": 12, "radius": 5}, {"leg": 13, "altitude": 5, "radius": 3},
            {"leg": 17, "altitude": 8, "radius": 6}]
TOL = 1e-9


def solve(leg=5, altitude=4, radius=2):
    half = isqrt(leg * leg - altitude * altitude)
    assert half * half == leg * leg - altitude * altitude
    return half


def _tangent_points(p, centre, r):
    dx, dy = p[0] - centre[0], p[1] - centre[1]
    d2 = dx * dx + dy * dy
    a = r * r / d2
    b = r * sqrt(d2 - r * r) / d2
    return [(centre[0] + a * dx - s * b * dy, centre[1] + a * dy + s * b * dx) for s in (1, -1)]


def check(leg=5, altitude=4, radius=2):
    half = sqrt(leg * leg - altitude * altitude)
    A, B, C = (0.0, float(altitude)), (-half, 0.0), (half, 0.0)
    hits = []
    for P in _tangent_points(B, A, radius):
        for Q in _tangent_points(C, A, radius):
            if abs(P[1] - Q[1]) < 1e-12:
                continue  # the mirror pair is parallel to BC
            t = -P[1] / (Q[1] - P[1])
            hits.append(P[0] + t * (Q[0] - P[0]))
    assert hits and all(abs(x) < 1e-9 for x in hits)
    return hypot(B[0] - hits[0], B[1])
