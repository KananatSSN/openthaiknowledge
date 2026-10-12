"""ข้อ 21 — จำนวนลูกบอลสีน้ำเงินในกล่องใบที่สอง

มีกล่อง 2 ใบ กล่องใบที่หนึ่งบรรจุลูกบอลสีเขียว 7 ลูก และลูกบอลสีน้ำเงิน 5 ลูก
กล่องใบที่สองบรรจุลูกบอลสีเขียว 5 ลูก และลูกบอลสีน้ำเงินอย่างน้อยหนึ่งลูก
สุ่มหยิบลูกบอลออกจากกล่อง กล่องละหนึ่งลูก ถ้าความน่าจะเป็นที่ได้ลูกบอลทั้งสองลูก
มีสีเดียวกันเท่ากับ 4/9 แล้วกล่องใบที่สองมีลูกบอลสีน้ำเงินทั้งหมดกี่ลูก

With b unknown,

    P(same) = (g₁g₂ + b₁b) / ((g₁+b₁)(g₂+b)) = p

is linear in b once cleared, so

    b = g₂(p(g₁+b₁) - g₁) / (b₁ - p(g₁+b₁)).

For 7, 5 | 5, b and p = 4/9 that is 5(4·12/9 - 7)/(5 - 4·12/9) = 25.

The item is only well posed when that comes out a positive integer, which is what
``solve`` returns ``None`` for otherwise — p is a free constant and most values of
it give a fractional count.
"""

from __future__ import annotations

from fractions import Fraction

#: box 1 holds g1 green and b1 blue; box 2 holds g2 green and the unknown blue.
PARAMS = {"g1": 7, "b1": 5, "g2": 5, "p_num": 4, "p_den": 9}
ANSWER = 25
VARIANTS = [
    {"g1": 3, "b1": 2, "g2": 4, "p_num": 1, "p_den": 2},
    {"g1": 6, "b1": 4, "g2": 3, "p_num": 2, "p_den": 5},
    {"g1": 8, "b1": 2, "g2": 1, "p_num": 1, "p_den": 5},
    {"g1": 7, "b1": 5, "g2": 5, "p_num": 1, "p_den": 3},   # no integer count
    {"g1": 7, "b1": 5, "g2": 5, "p_num": 9, "p_den": 4},   # p > 1
]


def solve(g1=7, b1=5, g2=5, p_num=4, p_den=9):
    """The number of blue balls in box 2, or None if no positive integer works."""
    if min(g1, b1, g2, p_num, p_den) <= 0:
        return None
    p = Fraction(p_num, p_den)
    if p >= 1:
        return None
    den = b1 - p * (g1 + b1)
    if den == 0:
        return None
    b = g2 * (p * (g1 + b1) - g1) / den
    if b <= 0 or b.denominator != 1:
        return None
    return int(b)


def check(g1=7, b1=5, g2=5, p_num=4, p_den=9):
    """Independent: try every count and compute the probability from scratch."""
    if min(g1, b1, g2, p_num, p_den) <= 0:
        return None
    want = Fraction(p_num, p_den)
    hits = [b for b in range(1, 10 ** 4 + 1)
            if Fraction(g1 * g2 + b1 * b, (g1 + b1) * (g2 + b)) == want]
    if len(hits) != 1:
        return None if not hits else hits[0]
    return hits[0]
