"""ข้อ 9 — รากที่น้อยที่สุดของ 2x⁵ + 5x⁴ + 5x³ + ax² + bx + c = 0 เมื่อรากทุกตัวเป็นจำนวนจริง

Σr = −5/2 and Σ_{i<j} rᵢrⱼ = 5/2 give Σr² = 25/4 − 5 = 5/4 = (Σr)²/5, so
Cauchy–Schwarz forces every root to equal Σr/5 = −1/2.

``check`` expands 2(x + 1/2)⁵ and confirms its top three coefficients are the
given ones, so the polynomial is forced and its only root is −1/2.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb

PARAMS = {"degree": 5, "lead": 2, "second": 5, "third": 5}
ANSWER = Fraction(-1, 2)
VARIANTS = [{"degree": 3, "lead": 1, "second": 3, "third": 3}, {"degree": 4, "lead": 1, "second": -8, "third": 24}, {"degree": 2, "lead": 4, "second": 4, "third": 1}]


def solve(degree=5, lead=2, second=5, third=5):
    total = Fraction(-second, lead)
    squares = total * total - 2 * Fraction(third, lead)
    assert degree * squares == total * total
    return total / degree


def check(degree=5, lead=2, second=5, third=5):
    for num in range(-200, 201):
        r = Fraction(num, 2 * degree)
        coeffs = [lead * comb(degree, k) * (-r) ** k for k in range(3)]
        if coeffs[1] == second and coeffs[2] == third:
            return r
    return None
