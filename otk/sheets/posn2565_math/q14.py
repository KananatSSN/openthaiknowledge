"""ข้อ 14 — รัศมีของวงกลมวงเล็กที่สุด

กำหนดให้วงกลมที่มีขนาดแตกต่างกัน 3 วงสัมผัสภายนอกซึ่งกันและกันและมีเส้นสัมผัส
ร่วมกัน ดังรูป  ถ้าความยาวรัศมีของวงกลมทั้งสามวงเรียงจากมากไปน้อยเป็น 4 หน่วย
1 หน่วย และ x หน่วย แล้ว จงหา x

รูปประกอบ (extract/figures/item14.png): all three circles sit on one line, the
big one on the right, the medium one on the left, and the tiny one wedged in the
gap between them — so the small circle's touch point lies *between* the other two.

Two circles resting on a line and touching each other have their touch points
2√(r₁r₂) apart, so reading the three gaps along the line:

    2√(R₁x) + 2√(R₂x) = 2√(R₁R₂)

Dividing by 2√(R₁R₂x) gives the descartes-like form

    1/√x = 1/√R₁ + 1/√R₂

and for R₁ = 4, R₂ = 1 that is 1/√x = 1/2 + 1 = 3/2, so

    x = (2/3)² = **4/9**.

The answer is rational exactly when both radii are perfect squares — with
p = √R₁ and q = √R₂ it is (pq/(p+q))² — and ``solve`` returns ``None`` otherwise
so the generator never has to print a surd here.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: the two larger radii, biggest first.
PARAMS = {"r1": 4, "r2": 1}
ANSWER = Fraction(4, 9)
VARIANTS = [
    {"r1": 9, "r2": 1},
    {"r1": 9, "r2": 4},
    {"r1": 16, "r2": 9},
    {"r1": 25, "r2": 4},
    {"r1": 3, "r2": 1},          # not perfect squares: x is irrational
    {"r1": 4, "r2": 4},          # the sheet says the three differ in size
]
TOL = 1e-9


def solve(r1=4, r2=1):
    """x = (pq/(p+q))² for p = √r₁, q = √r₂ — the third circle in the gap."""
    if r1 <= 0 or r2 <= 0 or r1 == r2:
        return None
    p, q = math.isqrt(int(r1)), math.isqrt(int(r2))
    if p * p != r1 or q * q != r2:
        return None
    return Fraction(p * q, p + q) ** 2


def check(r1=4, r2=1):
    """Independent: rest the two circles on a line and bisect the third's radius.

    Positions come from the distance between centres — tangency means the centres
    are r₁+r₂ apart — and the wedged circle's radius is found by shrinking it
    until it touches both. The 2√(r₁r₂) spacing rule is never used.
    """
    if r1 <= 0 or r2 <= 0 or r1 == r2:
        return None
    p, q = math.isqrt(int(r1)), math.isqrt(int(r2))
    if p * p != r1 or q * q != r2:
        return None
    a, b = float(r1), float(r2)
    # Both rest on y = 0; their centres are (0, a) and (dx, b), a+b apart.
    dx = math.sqrt((a + b) ** 2 - (a - b) ** 2)

    def touches(r: float) -> float:
        """How far the small circle, placed against the first, is from the second."""
        x1 = math.sqrt((a + r) ** 2 - (a - r) ** 2)      # tangent to circle 1
        return math.hypot(x1 - dx, r - b) - (b + r)

    lo, hi = 1e-12, min(a, b)
    if touches(lo) * touches(hi) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if touches(lo) * touches(mid) <= 0:
            hi = mid
        else:
            lo = mid
    r = (lo + hi) / 2
    x1 = math.sqrt((a + r) ** 2 - (a - r) ** 2)
    assert abs(math.hypot(x1, r - a) - (a + r)) < 1e-6
    assert abs(math.hypot(x1 - dx, r - b) - (b + r)) < 1e-6
    assert 0 < x1 < dx, "the small circle is not between the other two"
    return Fraction(r).limit_denominator(10 ** 6)
