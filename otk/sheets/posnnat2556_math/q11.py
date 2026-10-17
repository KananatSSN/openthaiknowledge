"""ข้อ 11 — ญาญ่าเลือก S ให้ได้เหรียญมากกว่าเสมอ  (พิสูจน์)

For a nonempty B, |B ∩ S| is odd for exactly half of all 2ᵐ subsets S and never
for S = ∅, so averaged over the 2ᵐ − 1 nonempty S Yaya gets
total·2^(m−1)/(2ᵐ − 1) > total/2, and some S does at least that well. The
solver returns that average (piles 3, 1, 4, 1, 5 and m = 3: 56/7 = 8).

``check`` plays every nonempty S against the given sets B, averages Yaya's
coins, and confirms her best S beats half the total.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

PARAMS = {"piles": (3, 1, 4, 1, 5), "m": 3, "sets": ((1,), (1, 2), (2, 3), (3,), (1, 2, 3))}
ANSWER = 8
VARIANTS = [
    {"piles": (2, 7), "m": 2, "sets": ((1,), (1, 2))},
    {"piles": (1, 1, 1, 1), "m": 4, "sets": ((1,), (2,), (3, 4), (1, 2, 3, 4))},
    {"piles": (5, 3, 8), "m": 3, "sets": ((1, 2), (2, 3), (1, 3))},
]


def solve(piles=(3, 1, 4, 1, 5), m=3, sets=()):
    return Fraction(sum(piles) * 2 ** (m - 1), 2**m - 1)


def check(piles=(3, 1, 4, 1, 5), m=3, sets=()):
    universe = range(1, m + 1)
    shares = []
    for size in range(1, m + 1):
        for S in combinations(universe, size):
            shares.append(sum(c for c, B in zip(piles, sets) if len(set(B) & set(S)) % 2))
    assert 2 * max(shares) > sum(piles)
    return Fraction(sum(shares), len(shares))
