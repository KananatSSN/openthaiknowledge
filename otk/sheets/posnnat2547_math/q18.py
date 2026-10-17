"""ข้อ 18 — a, b, c ที่ทำให้ abc สูงสุดเมื่อ b(a² + 2) + c(a + 2) = 12

For fixed a, AM–GM on the two terms gives b(a² + 2) = c(a + 2) = S/2 at the
maximum, so abc ≤ (S/2)²·a/((a² + 2)(a + 2)). The derivative of
a/((a² + 2)(a + 2)) vanishes at a³ + a² − 2 = 0, i.e. a = 1. Hence
(a, b, c) = (1, S/6, S/6) = (1, 2, 2).

``check`` maximises abc numerically: a ternary search over a with the optimal
split, then b and c from the split.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"total": 12}
ANSWER = (1, 2, 2)
TOL = 1e-7
VARIANTS = [{"total": 6}, {"total": 18}, {"total": 33}, {"total": 1}]


def solve(total=12):
    return (1, Fraction(total, 6), Fraction(total, 6))


def check(total=12):
    def g(a):
        return a / ((a * a + 2) * (a + 2))

    lo, hi = 1e-6, 10.0
    for _ in range(300):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if g(m1) < g(m2):
            lo = m1
        else:
            hi = m2
    a = (lo + hi) / 2
    return (a, total / 2 / (a * a + 2), total / 2 / (a + 2))
