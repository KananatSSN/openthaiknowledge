"""ข้อ 10 — เลือกสามจำนวนจาก {1, …, 3n} ให้ผลบวกหารด้วย 3 ลงตัว

The residue classes have n members each; the sum is 0 mod 3 when all three
share a class (3C(n, 3)) or all three classes differ (n³). The sheet states a
general n; PARAMS fixes n = 10.

``check`` enumerates every 3-subset.
"""

from __future__ import annotations

from itertools import combinations
from math import comb

PARAMS = {"n": 10}
ANSWER = 1360
VARIANTS = [{"n": 1}, {"n": 2}, {"n": 5}, {"n": 12}]


def solve(n=10):
    return 3 * comb(n, 3) + n**3


def check(n=10):
    return sum(1 for t in combinations(range(1, 3 * n + 1), 3) if sum(t) % 3 == 0)
