"""ข้อ 4 — √(a² + b² − √2ab) + √(b² + c² − √2bc) ≥ √(a² + c²)  (พิสูจน์)

Put points at distances a, b, c on rays at 0°, 45°, 90°: the left side is a
broken path from the first to the third point, the right side the straight
segment. Equality holds when the middle point lies on that segment, i.e. b is
the 45° bisector length √2·ac/(a + c). The solver returns that b
(a = c = 1: √2/2).

``check`` minimises (left side − right side) over b by ternary search; the
minimum is 0 and is reached at the equality b.
"""

from __future__ import annotations

import math

PARAMS = {"a": 1, "c": 1}
ANSWER = math.sqrt(2) / 2
TOL = 1e-7
VARIANTS = [{"a": 2, "c": 3}, {"a": 5, "c": 1}, {"a": 4, "c": 7}]


def solve(a=1, c=1):
    return math.sqrt(2) * a * c / (a + c)


def check(a=1, c=1):
    def gap(b):
        r2 = math.sqrt(2)
        return math.sqrt(a * a + b * b - r2 * a * b) + math.sqrt(b * b + c * c - r2 * b * c) - math.sqrt(a * a + c * c)

    lo, hi = 0.0, float(a + c)
    for _ in range(300):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if gap(m1) < gap(m2):
            hi = m2
        else:
            lo = m1
    b = (lo + hi) / 2
    assert abs(gap(b)) < 1e-9
    return b
