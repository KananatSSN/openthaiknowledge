"""ข้อ 5 — โยนลูกเต๋า 6 ครั้งได้แต้มรวม 21

Inclusion–exclusion on x₁ + ⋯ + x₆ = 21 with 1 ≤ xᵢ ≤ 6:
Σⱼ (−1)ʲ C(6, j) C(20 − 6j, 5) = 15504 − 6·2002 + 15·56 = 4332.

``check`` enumerates all 6⁶ rolls.
"""

from __future__ import annotations

from itertools import product
from math import comb

PARAMS = {"dice": 6, "total": 21}
ANSWER = 4332
VARIANTS = [{"dice": 3, "total": 10}, {"dice": 4, "total": 4}, {"dice": 5, "total": 18}, {"total": 36}]


def solve(dice=6, total=21):
    return sum((-1) ** j * comb(dice, j) * comb(total - 6 * j - 1, dice - 1)
               for j in range(dice + 1) if total - 6 * j - 1 >= dice - 1)


def check(dice=6, total=21):
    return sum(1 for roll in product(range(1, 7), repeat=dice) if sum(roll) == total)
