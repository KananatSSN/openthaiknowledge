"""ข้อ 3 — x > 0 ที่ x + ⌊x/3⌋ = ⌊2x/3⌋ + ⌊3x/5⌋

The right side and ⌊x/3⌋ are integers, so x is an integer; the linear parts have
slope 2/3 + 3/5 − 1/3 < 1 and each floor is within 1 of its value, so solutions
are bounded and an integer search finds x = 2, 5. The family is
x + ⌊x/a⌋ = ⌊bx/c⌋ + ⌊dx/e⌋.

``check`` searches positive rationals with denominators up to 30 (it does not
assume x is an integer).
"""

from __future__ import annotations

from fractions import Fraction
from math import floor

PARAMS = {"a": 3, "b": 2, "c": 3, "d": 3, "e": 5}
ANSWER = (2, 5)
VARIANTS = [{"a": 2, "b": 1, "c": 2, "d": 4, "e": 5}, {"a": 4, "b": 1, "c": 2, "d": 2, "e": 3}, {"a": 5, "b": 2, "c": 3, "d": 1, "e": 2}]


def solve(a=3, b=2, c=3, d=3, e=5):
    slope = Fraction(b, c) + Fraction(d, e) - Fraction(1, a)
    bound = int(3 / (1 - slope)) + 3
    return tuple(x for x in range(1, bound + 1) if x + x // a == (b * x) // c + (d * x) // e)


def check(a=3, b=2, c=3, d=3, e=5):
    found = set()
    for den in range(1, 31):
        for num in range(1, 60 * den + 1):
            x = Fraction(num, den)
            if x + floor(x / a) == floor(b * x / c) + floor(d * x / e):
                found.add(x)
    return tuple(int(x) if x.denominator == 1 else x for x in sorted(found))
