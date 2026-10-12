"""ข้อ 2 — จำนวนส้มในลังจากการหยิบสามวัน

มีส้มอยู่ในลังใบหนึ่ง ในวันที่ 1 หนูปอหยิบส้มไป 3/4 ของส้มทั้งหมดและหยิบเพิ่มอีก 2 ลูก
ในวันที่ 2 หยิบไปอีก 2/3 ของส้มที่เหลือและหยิบเพิ่มอีก 2 ลูก และในวันที่ 3 หยิบไปอีก 1/2
ของส้มที่เหลือและหยิบเพิ่มอีก 2 ลูก ถ้าในวันที่ 4 ส้มที่เหลืออยู่เท่ากับ 1/34 ของส้มทั้งหมด
อยากทราบว่าในลังใบนี้มีส้มทั้งหมดกี่ลูก

Each day leaves ``(1 − take)·(what was there) − extra``, so the three days
compose into one affine map of N:

    R₁ = N/4 − 2
    R₂ = R₁/3 − 2 = N/12 − 8/3
    R₃ = R₂/2 − 2 = N/24 − 10/3

and the last line says R₃ = N/34. Subtracting,

    N(1/24 − 1/34) = 10/3   ⟹   N · 5/408 = 10/3   ⟹   **N = 272**

Reading it forward: 272 → take 204 + 2, leaving 66 → take 44 + 2, leaving 20 →
take 10 + 2, leaving 8 = 272/34. ✓

The fractions are what make it work: 3/4, 2/3, 1/2 leave 1/4, 1/3, 1/2, whose
product is 1/24, and 1/24 is only a little more than 1/34.

``solve`` composes the affine map in exact fractions and inverts it. ``check``
plays the story out one orange at a time, testing every N up to a bound and
insisting the counts stay whole numbers.
"""

from __future__ import annotations

from fractions import Fraction

#: each day removes ``take`` of what is left, then ``extra`` more.
PARAMS = {"takes": (Fraction(3, 4), Fraction(2, 3), Fraction(1, 2)),
          "extra": 2, "leftover": Fraction(1, 34)}
ANSWER = 272
VARIANTS = [
    {"takes": (Fraction(1, 2), Fraction(1, 2)), "leftover": Fraction(1, 8)},
    {"extra": 1},
    {"extra": 5},
    {"takes": (Fraction(2, 3), Fraction(3, 4)), "leftover": Fraction(1, 20)},
    {"leftover": Fraction(1, 30)},
    {"takes": (Fraction(1, 2),), "extra": 3, "leftover": Fraction(1, 4)},
]


def solve(takes=(Fraction(3, 4), Fraction(2, 3), Fraction(1, 2)), extra=2,
          leftover=Fraction(1, 34)):
    """Compose the days into one affine map, then solve for N."""
    if not takes or extra < 0:
        return None
    slope, shift = Fraction(1), Fraction(0)          # remaining = slope·N + shift
    for take in takes:
        keep = 1 - Fraction(take)
        if keep <= 0:
            return None
        slope, shift = keep * slope, keep * shift - extra
    # slope·N + shift = leftover·N
    gap = slope - Fraction(leftover)
    if gap == 0:
        return None
    total = -shift / gap
    if total <= 0 or total.denominator != 1:
        return None
    # the affine map does not care about whole oranges; the story does, so the
    # candidate is replayed and rejected if any day asks for a fraction of one.
    left = total
    for take in takes:
        gone = Fraction(take) * left
        if gone.denominator != 1:
            return None
        left = left - gone - extra
        if left < 0 or left.denominator != 1:
            return None
    return int(total)


def check(takes=(Fraction(3, 4), Fraction(2, 3), Fraction(1, 2)), extra=2,
          leftover=Fraction(1, 34)):
    """Independent: play the story forward for every N and see which one fits.

    No inversion and no composed map — each candidate crate is emptied day by
    day, and a day is only legal when ``take`` of the pile is a whole number of
    oranges and enough are left to take the ``extra`` ones.
    """
    if not takes or extra < 0:
        return None
    limit = 200_000
    for total in range(1, limit + 1):
        left = Fraction(total)
        ok = True
        for take in takes:
            gone = Fraction(take) * left
            if gone.denominator != 1:
                ok = False
                break
            left = left - gone - extra
            if left < 0 or left.denominator != 1:
                ok = False
                break
        if ok and left == Fraction(leftover) * total:
            return total
    return None
