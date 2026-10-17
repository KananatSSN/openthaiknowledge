"""ข้อ 10 — จำนวนสามเหลี่ยมมากที่สุดจากจุด 17 จุดบนด้านรวมจุดยอด (20 จุด)

With kᵢ points on side i (vertices counted on both of their sides,
Σkᵢ = N + 6), only collinear triples on a side are lost; C(k, 3) is convex, so
the sides should be as equal as possible. For N = 17 the sides carry 8, 8, 7
points: C(20, 3) − 2·C(8, 3) − C(7, 3) = 1140 − 112 − 35 = 993.

``check`` tries every split of the N extra points among the three sides.
"""

from __future__ import annotations

from math import comb

PARAMS = {"extra": 17}
ANSWER = 993
VARIANTS = [{"extra": 1}, {"extra": 5}, {"extra": 30}]


def solve(extra=17):
    base, rem = divmod(extra + 6, 3)
    sides = [base + 1] * rem + [base] * (3 - rem)
    return comb(extra + 3, 3) - sum(comb(k, 3) for k in sides)


def check(extra=17):
    best = 0
    for x in range(extra + 1):
        for y in range(extra - x + 1):
            z = extra - x - y
            lost = sum(comb(k + 2, 3) for k in (x, y, z))
            best = max(best, comb(extra + 3, 3) - lost)
    return best
