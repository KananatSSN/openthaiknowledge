"""ข้อ 13 — ค.ร.น. ของ a และ b

ให้ a และ b เป็นจำนวนเต็มบวก โดยที่ a² + b² = 425 ถ้า ห.ร.ม. ของ a และ b มีค่า
เท่ากับ 5 จงหา ค.ร.น. ของ a และ b

The gcd factors straight out. Writing a = 5x and b = 5y with gcd(x, y) = 1,

    25(x² + y²) = 425  ⟹  x² + y² = 17

and the only way to write 17 as a sum of two positive squares is 1 + 16, so
{x, y} = {1, 4} — which is coprime, as required. Hence {a, b} = {5, 20} and

    lcm(a, b) = 5·x·y = 5 · 1 · 4 = **20**.

(Consistency check: 5² + 20² = 25 + 400 = 425 ✓ and gcd(5, 20) = 5 ✓.)

Note 425 = 5²·17 also equals 13² + 16², but gcd(13, 16) = 1, not 5 — the gcd
condition is what selects the right representation out of the two.

``solve`` divides out the gcd and searches the reduced equation; ``check`` sweeps
a and b directly over the printed equation and computes gcd and lcm with the
Euclidean algorithm, never reducing anything.
"""

from __future__ import annotations

from math import gcd, isqrt

#: a² + b² = total with gcd(a, b) = g.
PARAMS = {"total": 425, "g": 5}
ANSWER = 20
VARIANTS = [
    {"total": 425, "g": 1},
    {"total": 100, "g": 2},
    {"total": 200, "g": 10},
    {"total": 325, "g": 5},          # 13 = 2² + 3², so the pair is (10, 15)
    {"total": 50, "g": 5},
    {"total": 425, "g": 3},          # 9 does not divide 425
]


def solve(total=425, g=5):
    """lcm = g·x·y from x² + y² = total/g² with x, y coprime — when unique."""
    if total <= 0 or g <= 0 or total % (g * g):
        return None
    reduced = total // (g * g)
    hits = set()
    for x in range(1, isqrt(reduced) + 1):
        rest = reduced - x * x
        y = isqrt(rest)
        if y * y != rest or y < 1:
            continue
        if gcd(x, y) != 1:
            continue
        hits.add(g * x * y // gcd(x, y))
    if len(hits) != 1:
        return None
    return next(iter(hits))


def check(total=425, g=5):
    """Independent: sweep a and b over the printed equation and measure.

    Every positive pair with ``a² + b² = total`` is found by testing whether the
    remainder is a perfect square, then ``gcd(a, b)`` is computed with the
    Euclidean algorithm and compared against g, and the lcm is taken as
    ``a·b/gcd``. Nothing is divided out beforehand, so a wrong reduction would
    show up as a disagreement.
    """
    if total <= 0 or g <= 0:
        return None
    hits = set()
    for a in range(1, isqrt(total) + 1):
        rest = total - a * a
        b = isqrt(rest)
        if b * b != rest or b < 1:
            continue
        if gcd(a, b) != g:
            continue
        hits.add(a * b // gcd(a, b))
    if len(hits) != 1:
        return None
    return next(iter(hits))
