"""ข้อ 20 — ความสูงจุดตัดของเชือกระหว่างเสาสูง a และ b

Similar triangles give h/a + h/b = 1, so h = ab/(a + b), whatever the distance
between the poles. The sheet states general a, b; PARAMS fixes a = 4, b = 12.

``check`` intersects the two ropes as lines in coordinates, poles d apart.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"a": 4, "b": 12}
ANSWER = 3
VARIANTS = [{"a": 3, "b": 6}, {"a": 5, "b": 5}, {"a": 2, "b": 29}, {"a": 7, "b": 1}]


def solve(a=4, b=12):
    return Fraction(a * b, a + b)


def check(a=4, b=12):
    d = Fraction(17, 3)
    # rope 1: (0, a) → (d, 0); rope 2: (0, 0) → (d, b)
    x = a * d / (a + b)
    return b * x / d
