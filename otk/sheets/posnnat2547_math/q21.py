"""ข้อ 21 — ด้านที่สามเมื่อ R = (7/2)r และด้านสองด้านยาว 3, 7

R/r = abc/(4(s − a)(s − b)(s − c)) = 2abc/((−a + b + c)(a − b + c)(a + b − c)).
Scanning the integer third sides allowed by the triangle inequality, only
c = 8 gives 7/2.

``check`` builds each candidate triangle in coordinates and measures R and r
from the area.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"a": 3, "b": 7, "ratio": Fraction(7, 2)}
ANSWER = (8,)
VARIANTS = [{"a": 4, "b": 5, "ratio": Fraction(50, 21)}, {"a": 5, "b": 12, "ratio": Fraction(13, 4)}, {"a": 3, "b": 7, "ratio": Fraction(14, 3)}]


def solve(a=3, b=7, ratio=Fraction(7, 2)):
    return tuple(c for c in range(b - a + 1, a + b) if Fraction(2 * a * b * c, (-a + b + c) * (a - b + c) * (a + b - c)) == ratio)


def check(a=3, b=7, ratio=Fraction(7, 2)):
    found = []
    for c in range(abs(a - b) + 1, a + b):
        x = (a * a + c * c - b * b) / (2 * a)
        y = math.sqrt(c * c - x * x)
        area = a * y / 2
        r_big, r_small = a * b * c / (4 * area), area / ((a + b + c) / 2)
        if abs(r_big / r_small - float(ratio)) < 1e-9:
            found.append(c)
    return tuple(found)
