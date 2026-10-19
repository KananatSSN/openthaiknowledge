"""วันที่สอง ข้อ 6 — 3/4 + r/sₐ + r/s_b + r/s_c ≤ s²/(12r²)  (พิสูจน์)

r/sₐ = sin(A/2), so the left side is at most 3/4 + 3/2 = 9/4; Heron gives
s²/r² = s³/((s − a)(s − b)(s − c)) ≥ 27, so the right side is at least 9/4. The
solver returns s²/r² for given sides (3, 4, 5: s = 6, r = 1, so 36).

``check`` places the triangle in coordinates, takes the area by the shoelace
formula and r = area/s.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"a": 3, "b": 4, "c": 5}
ANSWER = 36
TOL = 1e-9
VARIANTS = [{"a": 2, "b": 2, "c": 2}, {"a": 3, "b": 14, "c": 14}, {"a": 7, "b": 8, "c": 9}]


def solve(a=3, b=4, c=5):
    s = Fraction(a + b + c, 2)
    return s**3 / ((s - a) * (s - b) * (s - c))


def check(a=3, b=4, c=5):
    x = (b * b + c * c - a * a) / (2 * c)
    pts = [(0.0, 0.0), (float(c), 0.0), (x, math.sqrt(b * b - x * x))]
    area = abs(sum(pts[i][0] * pts[(i + 1) % 3][1] - pts[(i + 1) % 3][0] * pts[i][1] for i in range(3))) / 2
    s = (a + b + c) / 2
    r = area / s
    return s * s / (r * r)
