"""ข้อ 2 — เขียน a ในรูปเศษส่วนอย่างต่ำ

ให้ a เป็นจำนวนตรรกยะบวก โดยที่  √a = √(8+4√3) / (√2 + √(2+√3))
จงเขียน a ในรูปเศษส่วนอย่างต่ำของจำนวนเต็มบวก

Both radicals denest:

    8 + 4√3 = (√6 + √2)²           so the numerator is √6 + √2 = √2(√3+1)
    2 + √3  = (√3+1)²/2            so √(2+√3) = (√3+1)/√2

and the denominator collapses to √2 + (√3+1)/√2 = (3+√3)/√2 = √3(√3+1)/√2.
Dividing, the (√3+1) cancels and

    √a = √2(√3+1)·√2 / (√3(√3+1)) = 2/√3,   a = **4/3**.

The family this belongs to: the numerator √(4k + 2k√3) denests as √k + √(3k) —
those are the roots of z² − 4kz + 3k² — and the same cancellation then gives

    √a = √(2k)/√3,   a = 2k/3,

with the sheet's k = 2 printing as √(8+4√3). That is the tunable, and it keeps
the answer a fraction for every k.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: the numerator is √(4k + 2k√3); the sheet's k = 2 prints as √(8 + 4√3).
PARAMS = {"k": 2}
ANSWER = Fraction(4, 3)
VARIANTS = [
    {"k": 1},
    {"k": 3},
    {"k": 6},
    {"k": 12},
    {"k": 0},          # degenerate
]
TOL = 1e-12


def solve(k=2):
    """a = 2k/3."""
    if k < 1:
        return None
    return Fraction(2 * k, 3)


def check(k=2):
    """Independent: evaluate the printed expression numerically and square it.

    Nothing is denested here — the nested radicals are computed as written, so a
    mis-stated identity in ``solve`` would show up immediately.
    """
    if k < 1:
        return None
    numerator = math.sqrt(4 * k + 2 * k * math.sqrt(3))
    denominator = math.sqrt(2) + math.sqrt(2 + math.sqrt(3))
    return Fraction((numerator / denominator) ** 2).limit_denominator(10 ** 6)
