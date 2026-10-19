"""ข้อ 11 — ผลเฉลยจำนวนเต็มบวกของ (x₁ + x₂ + x₃)(y₁ + ⋯ + y₄) = 91

For each factorisation N = d·e, compositions of d into p parts and of e into q
parts: Σ C(d − 1, p − 1)·C(e − 1, q − 1). For 91 = 7·13 that is
C(6, 2)C(12, 3) + C(12, 2)C(6, 3) = 3300 + 1320 = 4620.

``check`` enumerates the x-tuples and counts the y-compositions of the cofactor
by a small dynamic programme (no binomial formula).
"""

from __future__ import annotations

from itertools import product
from math import comb

PARAMS = {"total": 91, "p": 3, "q": 4}
ANSWER = 4620
VARIANTS = [{"total": 60}, {"total": 30, "p": 2, "q": 2}, {"total": 49, "p": 2, "q": 5}, {"total": 97}]


def solve(total=91, p=3, q=4):
    return sum(comb(d - 1, p - 1) * comb(total // d - 1, q - 1) for d in range(1, total + 1) if total % d == 0)


def check(total=91, p=3, q=4):
    def compositions(n, parts):
        ways = [1] + [0] * n
        for _ in range(parts):
            new = [0] * (n + 1)
            for s, w in enumerate(ways):
                for v in range(1, n - s + 1):
                    new[s + v] += w
            ways = new
        return ways[n]

    count = 0
    for xs in product(range(1, total + 1), repeat=p):
        s = sum(xs)
        if s <= total and total % s == 0:
            count += compositions(total // s, q)
    return count
