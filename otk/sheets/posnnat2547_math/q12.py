"""ข้อ 12 — จำนวนฟังก์ชันไม่เพิ่ม f : Aₙ → Aₙ

A non-increasing f is fixed by the multiset of its n values chosen from n kinds:
C(2n − 1, n). The sheet states a general n; PARAMS fixes n = 6.

``check`` enumerates every map and keeps the non-increasing ones.
"""

from __future__ import annotations

from itertools import product
from math import comb

PARAMS = {"n": 6}
ANSWER = 462
VARIANTS = [{"n": 1}, {"n": 2}, {"n": 4}, {"n": 7}]


def solve(n=6):
    return comb(2 * n - 1, n)


def check(n=6):
    return sum(1 for f in product(range(n), repeat=n) if all(a >= b for a, b in zip(f, f[1:])))
