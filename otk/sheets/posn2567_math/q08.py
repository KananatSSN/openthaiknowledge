"""ข้อ 8 — ค่าของ m² + n²

กำหนดให้ m และ n เป็นจำนวนเต็ม
ถ้า x² + 2x + 5 เป็นตัวประกอบของ x⁴ + mx³ + 4x² - 3x + n
แล้วค่าของ m² + n² เท่ากับเท่าใด

Divide by writing the cofactor as x² + bx + c and matching coefficients:

    x⁴ + (b+2)x³ + (c+2b+5)x² + (2c+5b)x + 5c

The x² and x coefficients are both known, so b and c are pinned without touching
m or n: c = -1 - 2b from the x² row, then the x row gives b = -1, c = 1. Only
then do m = b + 2 = 1 and n = 5c = 5 fall out, so m² + n² = 26.

``check`` runs the polynomial division and insists the remainder is identically
zero — no coefficient matching, and it fails loudly if the divisor does not
actually divide.
"""

from __future__ import annotations

from fractions import Fraction

#: divisor x² + px + q, and the known x² / x coefficients of the quartic.
PARAMS = {"p": 2, "q": 5, "c2": 4, "c1": -3}
ANSWER = 26
VARIANTS = [
    {"p": 1, "q": 3, "c2": 2, "c1": -1},
    {"p": 3, "q": 2, "c2": 5, "c1": 4},
    {"p": 2, "q": 5, "c2": 0, "c1": 1},
    {"p": 4, "q": 1, "c2": 6, "c1": -2},
    {"p": -1, "q": 7, "c2": 3, "c1": 5},
]


def _mn(p, q, c2, c1):
    """(m, n) as exact rationals, from the two coefficient rows."""
    # cofactor x² + bx + c:  c + p·b + q = c2,  q·b + p·c = c1
    #   → c = c2 - q - p·b   and   q·b + p·(c2 - q - p·b) = c1
    denom = q - p * p
    if denom == 0:
        return None
    b = Fraction(c1 - p * (c2 - q), denom)
    c = c2 - q - p * b
    return b + p, q * c


def solve(p=2, q=5, c2=4, c1=-3):
    """m² + n², or None when m and n do not come out integral."""
    mn = _mn(p, q, c2, c1)
    if mn is None:
        return None
    m, n = mn
    if m.denominator != 1 or n.denominator != 1:
        return None
    return int(m) ** 2 + int(n) ** 2


def check(p=2, q=5, c2=4, c1=-3):
    """Independent: divide the quartic and require a zero remainder."""
    mn = _mn(p, q, c2, c1)
    if mn is None:
        return None
    m, n = mn
    if m.denominator != 1 or n.denominator != 1:
        return None
    num = [Fraction(1), m, Fraction(c2), Fraction(c1), n]      # x⁴ … constant
    den = [Fraction(1), Fraction(p), Fraction(q)]
    rem = list(num)
    for i in range(len(num) - len(den) + 1):
        factor = rem[i]
        for j, d in enumerate(den):
            rem[i + j] -= factor * d
    if any(v != 0 for v in rem):
        raise AssertionError(f"x²+{p}x+{q} does not divide the quartic: {rem}")
    return int(m) ** 2 + int(n) ** 2
