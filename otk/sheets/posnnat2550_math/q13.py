"""ข้อ 13 — คู่เซตย่อยไม่ว่างที่ไม่มีสมาชิกร่วมของ {1, …, 8}

Each element goes to A, B or neither (3ⁿ); remove A = ∅ or B = ∅ (2·2ⁿ − 1) and
halve for order: (3ⁿ − 2ⁿ⁺¹ + 1)/2 = 3025.

``check`` lists the non-empty subsets and counts disjoint unordered pairs.
"""

from __future__ import annotations

from itertools import combinations

PARAMS = {"n": 8}
ANSWER = 3025
VARIANTS = [{"n": 1}, {"n": 3}, {"n": 6}]


def solve(n=8):
    return (3**n - 2 ** (n + 1) + 1) // 2


def check(n=8):
    masks = range(1, 1 << n)
    return sum(1 for s, t in combinations(masks, 2) if not s & t)
