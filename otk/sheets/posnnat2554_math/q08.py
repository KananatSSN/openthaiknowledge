"""ข้อ 8 — AC สัมผัสวงกลมล้อม ABG ⇒ AB + BC ≤ 2AC  (พิสูจน์)

The B-median meets AC at its midpoint K; tangency gives KA² = KG·KB, i.e.
b²/4 = m_b²/3, which with m_b² = (2a² + 2c² − b²)/4 becomes a² + c² = 2b²; then
(a + c)² ≤ 2(a² + c²) = 4b². The solver returns b = AC for a = BC, c = AB
(7, 17: 13).

``check`` searches b for the tangency itself: the distance from the
circumcentre of ABG to line AC equals its radius.
"""

from __future__ import annotations

import math

PARAMS = {"a": 7, "c": 17}
ANSWER = 13.0
TOL = 1e-7
VARIANTS = [{"a": 17, "c": 31}, {"a": 23, "c": 47}, {"a": 31, "c": 49}]


def solve(a=7, c=17):
    return math.sqrt((a * a + c * c) / 2)


def check(a=7, c=17):
    def gap(b):
        ap, cp = (0.0, 0.0), (b, 0.0)
        x = (b * b + c * c - a * a) / (2 * b)
        bp = (x, math.sqrt(max(c * c - x * x, 0.0)))
        g = ((ap[0] + bp[0] + cp[0]) / 3, (ap[1] + bp[1] + cp[1]) / 3)
        # circumcentre of A, B, G
        d = 2 * (ap[0] * (bp[1] - g[1]) + bp[0] * (g[1] - ap[1]) + g[0] * (ap[1] - bp[1]))
        ux = ((bp[0] ** 2 + bp[1] ** 2) * (g[1] - ap[1]) + (g[0] ** 2 + g[1] ** 2) * (ap[1] - bp[1])) / d
        uy = ((bp[0] ** 2 + bp[1] ** 2) * (ap[0] - g[0]) + (g[0] ** 2 + g[1] ** 2) * (bp[0] - ap[0])) / d
        radius = math.hypot(ux, uy)
        return abs(uy) - radius  # line AC is y = 0

    # the circle always passes through A on line AC, so the gap is ≤ 0 and
    # reaches 0 exactly at tangency: maximise it
    lo, hi = abs(c - a) + 1e-9, a + c - 1e-9
    xs = [lo + (hi - lo) * i / 4000 for i in range(4001)]
    i = max(range(4001), key=lambda j: gap(xs[j]))
    lo, hi = xs[max(i - 1, 0)], xs[min(i + 1, 4000)]
    for _ in range(300):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if gap(m1) < gap(m2):
            lo = m1
        else:
            hi = m2
    b = (lo + hi) / 2
    assert abs(gap(b)) < 1e-6
    return b
