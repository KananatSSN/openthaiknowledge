"""ข้อ 3 — ค่าของ x + y

ให้ x และ y เป็นจำนวนเต็มบวกที่สอดคล้องกับสมการ
    15^(1/(x+1)) = (2025 · 5^(y/2))^(1/(x+13))
ค่าของ x + y เท่ากับเท่าใด

Both sides are products of powers of 3 and 5 — 15 = 3·5 and 2025 = 3⁴·5² — and
3 and 5 are multiplicatively independent, so the exponents of each prime must
match separately. That turns one equation into two:

    3 :  1/(x+1) = 4/(x+13)          →  x = 3
    5 :  1/(x+1) = (2 + y/2)/(x+13)  →  y = 4

so x + y = 7. ``check`` never separates the primes: it evaluates both sides as
floating-point logarithms over a grid of (x, y) and reports the pairs that agree,
which is a different way of being wrong if the exponent bookkeeping is off.
"""

from __future__ import annotations

from fractions import Fraction

#: (exponent of 3, exponent of 5) on each side, and the two offsets.
PARAMS = {"lhs3": 1, "lhs5": 1, "rhs3": 4, "rhs5": 2, "off_lo": 1, "off_hi": 13}
ANSWER = 7
VARIANTS = [
    {"off_hi": 9},                        # x smaller
    {"rhs3": 3, "off_hi": 7},
    {"lhs3": 1, "lhs5": 1, "rhs3": 9, "rhs5": 3, "off_hi": 17},
    {"off_lo": 2, "off_hi": 14},
    {"rhs3": 2, "off_hi": 5},
]


def solve(lhs3=1, lhs5=1, rhs3=4, rhs5=2, off_lo=1, off_hi=13):
    """x + y, or None when the exponents force a non-positive-integer solution.

    Matching the exponent of 3 gives (x+off_hi)·lhs3 = (x+off_lo)·rhs3; matching
    the exponent of 5 then gives y.
    """
    if rhs3 == lhs3:
        return None
    x = Fraction(lhs3 * off_hi - rhs3 * off_lo, rhs3 - lhs3)
    if x.denominator != 1 or x <= 0:
        return None
    # lhs5/(x+off_lo) = (rhs5 + y/2)/(x+off_hi)
    y = 2 * (Fraction(lhs5 * (x + off_hi), x + off_lo) - rhs5)
    if y.denominator != 1 or y <= 0:
        return None
    return int(x) + int(y)


def check(lhs3=1, lhs5=1, rhs3=4, rhs5=2, off_lo=1, off_hi=13):
    """Independent: evaluate both sides numerically over a grid of (x, y)."""
    import math
    lhs_log = lhs3 * math.log(3) + lhs5 * math.log(5)
    hits = set()
    for x in range(1, 200):
        for y in range(1, 200):
            rhs_log = rhs3 * math.log(3) + (rhs5 + y / 2) * math.log(5)
            if abs(lhs_log / (x + off_lo) - rhs_log / (x + off_hi)) < 1e-12:
                hits.add(x + y)
    if len(hits) != 1:
        return None
    return hits.pop()
