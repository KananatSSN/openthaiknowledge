"""ข้อ 4 — x = √(x − 1/x) + √(1 − 1/x)

Move one root across and square twice: (x² + x − k)² = 4x(x² − k), which is
(x² − x − k)² = 0 (here k = 1). The positive root x = (1 + √(1 + 4k))/2 lies in
the domain (x ≥ 1, x ≥ √k) and satisfies the equation: (1 + √5)/2.

``check`` scans the domain for the minimum of |x − √(x − k/x) − √(k − k/x)|
and refines it by ternary search; the function touches zero there.
"""

from __future__ import annotations

import math

PARAMS = {"k": 1}
ANSWER = (1 + math.sqrt(5)) / 2
TOL = 1e-7
VARIANTS = [{"k": 2}, {"k": 3}, {"k": 6}, {"k": 11}]


def solve(k=1):
    return (1 + math.sqrt(1 + 4 * k)) / 2


def check(k=1):
    def gap(x):
        return abs(x - math.sqrt(max(x - k / x, 0)) - math.sqrt(max(k - k / x, 0)))

    lo_bound = max(1.0, math.sqrt(k))
    grid = [lo_bound + i * 0.001 for i in range(20000)]
    x0 = min(grid, key=gap)
    lo, hi = max(lo_bound, x0 - 0.002), x0 + 0.002
    for _ in range(200):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if gap(m1) < gap(m2):
            hi = m2
        else:
            lo = m1
    return (lo + hi) / 2
