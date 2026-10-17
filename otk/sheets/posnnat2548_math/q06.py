"""ข้อ 6 — ผลเฉลยจำนวนเต็มบวกของ (x₁ + x₂ + x₃)²(y₁ + y₂) = 2548

2548 = 2²·7²·13. With s = x₁ + x₂ + x₃ ≥ 3 and s² | 2548: s = 7 (y-sum 52,
C(6, 2)·51 = 765) or s = 14 (y-sum 13, C(13, 2)·12 = 936). Total 1701.

``check`` enumerates the x-triples directly and counts y-pairs for each.
"""

from __future__ import annotations

from itertools import product
from math import comb, isqrt

PARAMS = {"total": 2548}
ANSWER = 1701
VARIANTS = [{"total": 1134}, {"total": 288}, {"total": 900}, {"total": 2549}]


def solve(total=2548):
    return sum(comb(s - 1, 2) * (total // (s * s) - 1) for s in range(3, isqrt(total) + 1) if total % (s * s) == 0)


def check(total=2548):
    count = 0
    for xs in product(range(1, isqrt(total) + 1), repeat=3):
        s = sum(xs)
        if total % (s * s) == 0:
            count += max(total // (s * s) - 1, 0)
    return count
