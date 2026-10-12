"""ข้อ 22 — ผลบวกของ a ที่เป็นไปได้ทั้งหมด

กล่องใบหนึ่งบรรจุลูกแก้วสีม่วง 7 ลูก ลูกแก้วสีเขียว 6 ลูก และลูกแก้วสีส้มจำนวนหนึ่ง
สุ่มหยิบลูกแก้ว 1 ลูกจากกล่องใบนี้  ถ้าความน่าจะเป็นที่ได้ลูกแก้วสีส้มเท่ากับ 1/a
เมื่อ a เป็นจำนวนเต็มบวก แล้วผลบวกของ a ที่เป็นไปได้ทั้งหมดเท่ากับเท่าใด

With m = 7 + 6 = 13 other marbles and k ≥ 1 orange ones,

    1/a = k/(m + k)   ⟺   a = 1 + m/k,

so a is an integer exactly when k divides m, and the possible a are 1 + m/k over
the divisors k of m. Summing,

    Σ a = d(m) + σ(m)

— the number of divisors plus their sum. For m = 13 (prime) that is 2 + 14 = 16,
from k = 1 (a = 14) and k = 13 (a = 2).

The prime 13 is what makes the sheet's version short; ``solve`` handles any m, and
a composite m gives a longer list, which is the interesting variant.
"""

from __future__ import annotations

#: the two named colours; their total is the m above.
PARAMS = {"purple": 7, "green": 6}
ANSWER = 16
VARIANTS = [
    {"purple": 5, "green": 7},          # m = 12, six divisors
    {"purple": 10, "green": 10},        # m = 20
    {"purple": 1, "green": 1},          # m = 2
    {"purple": 20, "green": 16},        # m = 36, nine divisors
    {"purple": 0, "green": 0},          # degenerate
]


def solve(purple=7, green=6):
    """Σ a = d(m) + σ(m) over the divisors k of m = purple + green."""
    m = purple + green
    if m < 1:
        return None
    total = 0
    for k in range(1, m + 1):
        if m % k == 0:
            total += 1 + m // k
    return total


def check(purple=7, green=6):
    """Independent: scan the orange count and keep the ones giving 1/a exactly."""
    from fractions import Fraction
    m = purple + green
    if m < 1:
        return None
    found = []
    for k in range(1, m * 4 + 2):
        p = Fraction(k, m + k)
        if p.numerator == 1:
            found.append(p.denominator)
    return sum(found)
