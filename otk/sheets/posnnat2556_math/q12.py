"""ข้อ 12 — [ABR] = [PQMN]  (พิสูจน์)

P is the antipode of D on ω, so A, P, M are collinear with BM = CD = s − c
(the homothety at A taking ω to the A-excircle); CN = AE = s − a puts N at the
B-extouch point, so R = AM ∩ BN is the Nagel point (s − a : s − b : s − c) and
[ABR] = [ABC]·(s − c)/s. The solver returns that area (13, 14, 15: 24).

``check`` builds the figure in coordinates: incircle, P as the second
intersection of the perpendicular at D, M = AP ∩ BC, N with CN = AE, Q as the
intersection of BN with ω nearer B, R = AM ∩ BN; it measures [ABR] and the
quadrilateral PQMN by shoelace and asserts they are equal.
"""

from __future__ import annotations

from math import sqrt

PARAMS = {"a": 13, "b": 14, "c": 15}
ANSWER = 24.0
VARIANTS = [{"a": 7, "b": 8, "c": 9}, {"a": 5, "b": 6, "c": 7}, {"a": 9, "b": 10, "c": 12}]
TOL = 1e-9


def solve(a=13, b=14, c=15):
    s = (a + b + c) / 2
    area = sqrt(s * (s - a) * (s - b) * (s - c))
    return area * (s - c) / s


def _meet(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


def _shoelace(*pts):
    return abs(sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1] for i in range(len(pts)))) / 2


def check(a=13, b=14, c=15):
    B, C = (0.0, 0.0), (float(a), 0.0)
    ax = (a * a + c * c - b * b) / (2 * a)
    A = (ax, sqrt(c * c - ax * ax))
    per = a + b + c
    inc = ((a * A[0] + b * B[0] + c * C[0]) / per, (a * A[1] + b * B[1] + c * C[1]) / per)
    r = inc[1]
    P = (inc[0], 2 * r)  # the perpendicular at D (below inc) meets ω again at the top
    M = _meet(A, P, B, C)
    # E is the touch point on CA; AE = distance from A to its foot
    ux, uy = (C[0] - A[0]) / b, (C[1] - A[1]) / b
    ae = (inc[0] - A[0]) * ux + (inc[1] - A[1]) * uy
    N = (C[0] - ae * ux, C[1] - ae * uy)
    # BN against ω: B + t(N − B), |X − I| = r
    dx, dy = N[0] - B[0], N[1] - B[1]
    fx, fy = B[0] - inc[0], B[1] - inc[1]
    qa, qb, qc = dx * dx + dy * dy, 2 * (fx * dx + fy * dy), fx * fx + fy * fy - r * r
    t = (-qb - sqrt(qb * qb - 4 * qa * qc)) / (2 * qa)
    Q = (B[0] + t * dx, B[1] + t * dy)
    R = _meet(A, M, B, N)
    abr = _shoelace(A, B, R)
    assert abs(abr - _shoelace(P, Q, M, N)) < 1e-9 * max(1.0, abr)
    return abr
