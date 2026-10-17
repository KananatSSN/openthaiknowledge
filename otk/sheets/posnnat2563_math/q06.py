"""ข้อ 6 — △ALE ∼ △AEB และ FK = FL  (พิสูจน์)

With tangent lengths x = AF, y = BF, the bisector conditions put K and L on AB
with FK = FL = AF·BF/AB = xy/(x + y). The solver returns that length
(x, y = 3, 5: 15/8).

``check`` builds the triangle from the tangent lengths (x, y, z), the touch
points D, E, F, then K by reflecting line DA in DF and L by reflecting EB in
EF, intersecting each with AB; it asserts △ALE ∼ △AEB (AL·AB = AE²) and
FK = FL, and returns FK.
"""

from __future__ import annotations

from fractions import Fraction
from math import hypot, sqrt

PARAMS = {"af": 3, "bf": 5, "cd": 4}
ANSWER = Fraction(15, 8)
VARIANTS = [{"af": 4, "bf": 4, "cd": 3}, {"af": 5, "bf": 3, "cd": 6}, {"af": 6, "bf": 5, "cd": 7}]
TOL = 1e-9


def solve(af=3, bf=5, cd=4):
    return Fraction(af * bf, af + bf)


def _meet(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


def _reflect(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)
    fx, fy = a[0] + t * dx, a[1] + t * dy
    return (2 * fx - p[0], 2 * fy - p[1])


def check(af=3, bf=5, cd=4):
    x, y, z = af, bf, cd
    a, b, c = y + z, x + z, x + y
    assert max(a, b, c) ** 2 < a * a + b * b + c * c - max(a, b, c) ** 2  # acute
    A, B = (0.0, 0.0), (float(c), 0.0)
    cx = (b * b + c * c - a * a) / (2 * c)
    C = (cx, sqrt(b * b - cx * cx))
    F = (float(x), 0.0)
    E = (C[0] * x / b, C[1] * x / b)
    D = (B[0] + (C[0] - B[0]) * y / a, B[1] + (C[1] - B[1]) * y / a)
    K = _meet(D, _reflect(A, D, F), A, B)
    L = _meet(E, _reflect(B, E, F), A, B)
    al, ae = hypot(*L), hypot(*E)
    assert abs(al * c - ae * ae) < 1e-9
    fk, fl = hypot(K[0] - F[0], K[1] - F[1]), hypot(L[0] - F[0], L[1] - F[1])
    assert abs(fk - fl) < 1e-9
    return fk
