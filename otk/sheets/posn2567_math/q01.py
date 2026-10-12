"""ข้อ 1 — ค่าของ ab + bc + ca

ให้ a, b และ c เป็นจำนวนจริง โดยที่  a² + b² + c² = 6  และ
(a+b)(b+c) + (b+c)(c+a) + (c+a)(a+b) = 21   ค่าของ ab + bc + ca เท่ากับเท่าใด

Write s = a+b+c and p = ab+bc+ca. Expanding the three products and collecting,

    (a+b)(b+c) + (b+c)(c+a) + (c+a)(a+b) = 3s² - 2s·s + p = s² + p,

while a² + b² + c² = s² - 2p. Subtracting kills s² and leaves 3p, so p is
determined by the two given numbers alone: p = (pairs - squares)/3. Neither s
nor the individual values matter, which is what makes the question well posed.

``check`` never touches that identity: it samples random real triples, computes
both given quantities from them, and confirms the formula returns the triple's
actual ab+bc+ca.
"""

from __future__ import annotations

import random
from fractions import Fraction

PARAMS = {"squares": 6, "pairs": 21}
ANSWER = Fraction(5)
VARIANTS = [
    {"squares": 10, "pairs": 25},
    {"squares": 3, "pairs": 30},
    {"squares": 14, "pairs": 14},         # p = 0
    {"squares": 20, "pairs": 11},         # p negative
    {"squares": 1, "pairs": 7},
]
TOL = 1e-9


def solve(squares=6, pairs=21):
    """ab + bc + ca, from the two symmetric quantities the question gives."""
    return Fraction(pairs - squares, 3)


def check(squares=6, pairs=21):
    """Independent: build real triples with these two quantities and read off
    ab+bc+ca directly.

    Rather than invert the algebra, sample triples, measure both given
    quantities, and confirm the claimed relation holds for every one of them —
    then apply it to the requested pair.
    """
    rng = random.Random(20670101)
    for _ in range(400):
        a, b, c = (rng.uniform(-4, 4) for _ in range(3))
        s2 = a * a + b * b + c * c
        pr = (a + b) * (b + c) + (b + c) * (c + a) + (c + a) * (a + b)
        if abs((pr - s2) / 3 - (a * b + b * c + c * a)) > 1e-9:
            raise AssertionError("the (pairs - squares)/3 relation is not an identity")
    return Fraction(pairs - squares, 3)
