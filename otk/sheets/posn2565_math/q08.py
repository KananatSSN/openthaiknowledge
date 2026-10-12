"""ข้อ 8 — ความน่าจะเป็นที่มีลูกเต๋าอย่างน้อย 1 ลูกขึ้นแต้มที่เป็นจำนวนเฉพาะ

นายเพชรทำการโยนลูกเต๋า 2 ลูก 1 ครั้ง จงหาความน่าจะเป็นที่มีลูกเต๋าอย่างน้อย 1 ลูก
ขึ้นแต้มที่เป็นจำนวนเฉพาะ

"At least one" is the complement of "none":

    P = 1 - ((f - p)/f)^n

where f is the number of faces, p how many of 1..f are prime and n the number of
dice. A die has three primes among its six faces — 2, 3 and 5, but **not 1** —
so with two dice

    P = 1 - (3/6)² = **3/4**.

Counting 1 as prime turns the answer into 1 - (2/6)² = 8/9, and that is the
mistake the item is built to catch; the generator offers it as a distractor.
"""

from __future__ import annotations

import itertools
from fractions import Fraction
from math import isqrt

#: `dice` dice, each with faces 1..`faces`.
PARAMS = {"faces": 6, "dice": 2}
ANSWER = Fraction(3, 4)
VARIANTS = [
    {"faces": 6, "dice": 3},
    {"faces": 8, "dice": 2},
    {"faces": 4, "dice": 4},
    {"faces": 12, "dice": 2},
    {"faces": 1, "dice": 3},          # a one-faced die shows 1: never prime
    {"faces": 6, "dice": 0},          # no throw at all
]


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    return all(n % f for f in range(2, isqrt(n) + 1))


def solve(faces=6, dice=2):
    """1 - (non-prime faces / faces)^dice."""
    if faces < 1 or dice < 1:
        return None
    primes = sum(1 for v in range(1, faces + 1) if _is_prime(v))
    return 1 - Fraction(faces - primes, faces) ** dice


def check(faces=6, dice=2):
    """Independent: enumerate every throw and test it for a prime face."""
    if faces < 1 or dice < 1:
        return None
    if faces ** dice > 2 * 10 ** 6:
        return None
    good = sum(1 for throw in itertools.product(range(1, faces + 1), repeat=dice)
               if any(_is_prime(v) for v in throw))
    return Fraction(good, faces ** dice)
