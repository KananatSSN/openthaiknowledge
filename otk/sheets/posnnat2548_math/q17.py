"""ข้อ 17 — 0 ∗ (1 ∗ (2 ∗ (⋯(2003 ∗ (2004 ∗ 2005))⋯))) เมื่อ a ∗ b = (a + b + 1)/(ab + 12)

12 = 3·(3 + 1), so 3 ∗ w = (w + 4)/(3(w + 4)) = 1/3 for every w ≥ 0, and only
2 ∗ 1/3, 1 ∗ … and 0 ∗ … remain: 23/233.

``check`` evaluates the whole chain from the inside out in exact fractions.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"alpha": 1, "t": 3, "last": 2005}
ANSWER = Fraction(23, 233)
VARIANTS = [{"alpha": 2, "t": 2, "last": 1144}, {"alpha": 4, "t": 5, "last": 40}, {"alpha": 3, "t": 4, "last": 9}]


def solve(alpha=1, t=3, last=2005):
    beta = t * (t + alpha)
    value = Fraction(1, t)
    for a in range(t - 1, -1, -1):
        value = (a + value + alpha) / (a * value + beta)
    return value


def check(alpha=1, t=3, last=2005):
    beta = t * (t + alpha)
    value = Fraction(last)
    for a in range(last - 1, -1, -1):
        value = (a + value + alpha) / (a * value + beta)
    return value
