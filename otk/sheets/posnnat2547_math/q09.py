"""ข้อ 9 — Σₖ₌₀ⁿ (2n)!/((k!)²((n − k)!)²)

Each term is C(2n, n)·C(n, k)², and Σ C(n, k)² = C(2n, n), so the sum is
C(2n, n)². The sheet states a general n; PARAMS fixes n = 10.

``check`` adds the terms as exact fractions.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb, factorial

PARAMS = {"n": 10}
ANSWER = 34134779536
VARIANTS = [{"n": 1}, {"n": 4}, {"n": 13}, {"n": 25}]


def solve(n=10):
    return comb(2 * n, n) ** 2


def check(n=10):
    return sum(Fraction(factorial(2 * n), factorial(k) ** 2 * factorial(n - k) ** 2) for k in range(n + 1))
