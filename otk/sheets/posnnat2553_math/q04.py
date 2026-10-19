"""ข้อ 4 — ∠AOB เมื่อ ABC ด้านเท่า, AN = BM, 3MB = AB, O = CM ∩ BN

Triangles ABN and BCM are congruent (AN = BM), so ∠OBC + ∠OCB = 60° and
∠BOC = 120°. For BM = AB/3, O lies on the circle with diameter AC, so AO ⟂ OC
and ∠AOB = 150°. ``solve`` intersects the cevians in coordinates with A at the
origin and AB on the x-axis.

``check`` repeats the construction in a rotated, translated frame with complex
numbers, so nothing aligns with an axis.
"""

from __future__ import annotations

import cmath
import math
from fractions import Fraction

PARAMS = {"t": Fraction(1, 3)}
ANSWER = 150.0
TOL = 1e-9
VARIANTS = [{"t": Fraction(1, 2)}, {"t": Fraction(2, 3)}, {"t": Fraction(1, 4)}]


def _intersect(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    s = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    return (p1[0] + s * (p2[0] - p1[0]), p1[1] + s * (p2[1] - p1[1]))


def solve(t=Fraction(1, 3)):
    t = float(t)
    a, b, c = (0.0, 0.0), (1.0, 0.0), (0.5, math.sqrt(3) / 2)
    m = (1 - t, 0.0)  # BM = t
    n = (c[0] * t, c[1] * t)  # AN = t
    o = _intersect(c, m, b, n)
    u, v = (a[0] - o[0], a[1] - o[1]), (b[0] - o[0], b[1] - o[1])
    return math.degrees(math.acos((u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))))


def check(t=Fraction(1, 3)):
    t = float(t)
    rot, shift, side = cmath.exp(0.7j), complex(3.1, -2.4), 2.6
    a = shift
    b = a + side * rot
    c = a + side * rot * cmath.exp(1j * math.pi / 3)
    m = b + (a - b) * t
    n = a + (c - a) * t
    # O = C + s(M − C) = B + u(N − B)
    d1, d2, r = m - c, n - b, b - c
    det = d1.real * (-d2.imag) - (-d2.real) * d1.imag
    s = (r.real * (-d2.imag) - (-d2.real) * r.imag) / det
    o = c + s * d1
    return math.degrees(abs(cmath.phase((a - o) / (b - o))))
