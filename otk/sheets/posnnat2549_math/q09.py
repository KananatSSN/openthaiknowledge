"""ข้อ 9 — จำนวนเต็มมากสุดไม่เกิน 2549³/(2547·2548) − 2547³/(2548·2549)

With n = 2548, d = 1 the difference is ((n + d)⁴ − (n − d)⁴)/((n − d)n(n + d))
= 8d(n² + d²)/(n² − d²) = 8d + 16d³/(n² − d²), so the floor is 8.

``check`` computes the difference as an exact fraction and floors it.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"n": 2548, "d": 1}
ANSWER = 8
VARIANTS = [{"n": 12, "d": 2}, {"n": 2}, {"n": 4, "d": 3}, {"n": 40, "d": 4}]


def solve(n=2548, d=1):
    return 8 * d + (16 * d**3) // (n * n - d * d)


def check(n=2548, d=1):
    v = Fraction((n + d) ** 3, (n - d) * n) - Fraction((n - d) ** 3, n * (n + d))
    return v.numerator // v.denominator
