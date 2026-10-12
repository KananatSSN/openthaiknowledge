"""ข้อ 16 — ค่ามากที่สุดของ P + Q (หลอดไฟสองกล่อง)

กล่องละ n หลอด (โจทย์: n = 25) แต่ละกล่องมีหลอดเสียอย่างน้อยหนึ่งหลอด จำนวนเท่ากัน
และเป็นพหุคูณของ mult (โจทย์: 7)  สุ่มหยิบกล่องละ 1 หลอด
ให้ P = ความน่าจะเป็นที่ได้หลอดดีทั้งสอง, Q = ความน่าจะเป็นที่ได้หลอดเสียทั้งสอง
จงหาค่ามากที่สุดที่เป็นไปได้ของ P + Q

Method: with d defectives in each box the two draws are independent, so
    P + Q = ((n−d)/n)² + (d/n)² = ((n−d)² + d²)/n².
As a function of d that is a upward parabola with its minimum at d = n/2, so on
any set of admissible d the maximum is at whichever *endpoint* is further from
the middle — here d = 7 or d = 21, and d = 21 wins with 457/625.

``check`` evaluates every admissible d instead of reasoning about convexity.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"n": 25, "mult": 7}
ANSWER = Fraction(457, 625)
VARIANTS = [
    {"n": 25, "mult": 5},
    {"n": 20, "mult": 3},
    {"n": 100, "mult": 7},
    {"n": 10, "mult": 4},
    {"n": 12, "mult": 12},
]


def _value(d: int, n: int) -> Fraction:
    return Fraction((n - d) ** 2 + d * d, n * n)


def admissible(n=25, mult=7) -> list[int]:
    """Defect counts allowed: at least one, at most n, a multiple of mult."""
    return [d for d in range(mult, n + 1, mult)]


def solve(n=25, mult=7):
    """Max of P+Q. Convexity puts it at an endpoint of the admissible set."""
    options = admissible(n, mult)
    if not options:
        return None
    return max(_value(options[0], n), _value(options[-1], n))


def check(n=25, mult=7):
    """Independent: score every admissible d."""
    options = admissible(n, mult)
    return max((_value(d, n) for d in options), default=None)
