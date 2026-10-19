"""ข้อ 1 — cos⁸A − sin⁸A เมื่อ cos 4A = 1/3 และ −π/4 ≤ A ≤ π/4

cos⁸A − sin⁸A = (cos²A − sin²A)(cos⁴A + sin⁴A) = cos 2A·(1 − ½sin²2A).
On the given range cos 2A ≥ 0, cos²2A = (1 + c)/2 and sin²2A = (1 − c)/2, so the
value is √((1 + c)/2)·(3 + c)/4. For c = 1/3 that is 5√6/18.

``check`` recovers A = arccos(c)/4 and evaluates the eighth powers directly.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"c": Fraction(1, 3)}
ANSWER = 5 * math.sqrt(6) / 18
VARIANTS = [{"c": Fraction(0)}, {"c": Fraction(-1, 2)}, {"c": Fraction(3, 4)}, {"c": Fraction(1, 5)}]


def solve(c=Fraction(1, 3)):
    return math.sqrt((1 + c) / 2) * (3 + c) / 4


def check(c=Fraction(1, 3)):
    a = math.acos(float(c)) / 4
    return math.cos(a) ** 8 - math.sin(a) ** 8
