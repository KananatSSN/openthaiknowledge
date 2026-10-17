"""ข้อ 1 — ลูกบอล 11 ลูกลงกล่อง 5 ใบ (ใหญ่สุด + เล็กสุด ≥ สามใบที่เหลือ)

With s balls in the two named boxes (s ≥ ⌈N/2⌉ so that s ≥ N − s): s − 1 ways
for that pair and C(N − s − 1, 2) for the other three boxes; summing gives 55.

``check`` enumerates every distribution with at least one ball per box.
"""

from __future__ import annotations

from itertools import product
from math import comb

PARAMS = {"balls": 11}
ANSWER = 55
VARIANTS = [{"balls": 5}, {"balls": 8}, {"balls": 15}]


def solve(balls=11):
    return sum((s - 1) * comb(balls - s - 1, 2) for s in range((balls + 1) // 2, balls - 2))


def check(balls=11):
    count = 0
    for small, b2, b3, b4 in product(range(1, balls), repeat=4):
        big = balls - small - b2 - b3 - b4
        if big >= 1 and small + big >= b2 + b3 + b4:
            count += 1
    return count
