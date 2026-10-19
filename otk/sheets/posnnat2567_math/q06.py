"""ข้อ 6 — n ที่แบ่ง {1, …, 2n + 1} − {n + 1} เป็นสองกลุ่มขนาดเท่าและผลรวมเท่ากัน

Subtracting n + 1 turns the set into ±1, …, ±n with total 0, so a split is a
choice of n of these with sum 0. n = 1 fails ({−1, 1} has no single zero);
n ≥ 2 works (pair ±k and fix the parity with a three-term zero sum when n is
odd). The answer is the tuple of working n up to `limit`.

``check`` runs a count-and-sum subset DP over ±1..±n for each n.
"""

from __future__ import annotations

PARAMS = {"limit": 8}
ANSWER = (2, 3, 4, 5, 6, 7, 8)
VARIANTS = [{"limit": 1}, {"limit": 4}, {"limit": 12}]


def solve(limit=8):
    return tuple(range(2, limit + 1))


def check(limit=8):
    works = []
    for n in range(1, limit + 1):
        reach = {(0, 0)}
        for v in [k for k in range(-n, n + 1) if k]:
            reach |= {(c + 1, s + v) for c, s in reach if c < n}
        if (n, 0) in reach:
            works.append(n)
    return tuple(works)
