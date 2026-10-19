"""วันที่สอง ข้อ 2 — มีฟังก์ชันหนึ่งต่อหนึ่ง f : ℕ → ℚ ที่ f(xy) = f(x) + f(y) หรือไม่ (ไม่มี)

f(2^a) = a·f(2) and f(3^b) = b·f(3); with a/b = f(3)/f(2) in lowest terms (if
both are positive) f(2^a) = f(3^b) although 2^a ≠ 3^b, so f is not injective.
The solver returns that collision (a, b) (f(2) = 1, f(3) = 3/2: (3, 2)).

``check`` searches a, b ≤ 200 for the first a·f(2) = b·f(3).
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"f2": Fraction(1), "f3": Fraction(3, 2)}
ANSWER = (3, 2)
VARIANTS = [{"f2": Fraction(2), "f3": Fraction(5)}, {"f2": Fraction(1, 3), "f3": Fraction(1, 4)}, {"f3": Fraction(1)}]


def solve(f2=Fraction(1), f3=Fraction(3, 2)):
    ratio = Fraction(f3) / Fraction(f2)
    return (ratio.numerator, ratio.denominator)


def check(f2=Fraction(1), f3=Fraction(3, 2)):
    for total in range(2, 401):
        for a in range(1, total):
            b = total - a
            if a * f2 == b * f3:
                return (a, b)
    return None
