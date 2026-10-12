"""ข้อ 2 — ค่าที่น้อยที่สุดที่เป็นไปได้ของ m + n

ให้ m และ n เป็นจำนวนเต็มบวกที่มี ห.ร.ม. และ ค.ร.น. เป็น 20 และ 50400 ตามลำดับ
จงหาค่าที่น้อยที่สุดที่เป็นไปได้ของ m + n

Write m = g·a and n = g·b with g = 20 and gcd(a, b) = 1. The lcm is then g·a·b,
so ``a·b = 50400/20 = 2520 = 2³·3²·5·7`` and the pair must be **coprime**: each
prime power goes wholly to one side. With four prime powers there are only
2⁴ = 16 ordered splits, and minimising ``m + n = 20(a + b)`` means taking the
split whose halves sit closest to √2520 ≈ 50.2. The unitary divisors are
1, 5, 7, 8, 9, 35, 40, 45, 56, 63, 72, 280, 315, 360, 504, 2520, and

    45 · 56 = 2520,   45 + 56 = 101   (the next best, 40 + 63, gives 103)

so the answer is ``20 · 101`` = **2020**, the pair (900, 1120).

Coprimality is the whole trick: the instinct to make the two factors as equal as
possible would want 2520 ≈ 50·50, which no coprime split can reach.

``solve`` enumerates the coprime factorisations of l/g; ``check`` walks the
divisors of the lcm that are multiples of g and tests both directly.
"""

from __future__ import annotations

from math import gcd, isqrt

#: the pair's gcd and lcm.
PARAMS = {"g": 20, "lcm": 50400}
ANSWER = 2020
VARIANTS = [
    {"g": 6, "lcm": 360},
    {"g": 1, "lcm": 2520},
    {"g": 12, "lcm": 720},
    {"g": 15, "lcm": 15},          # m = n = g is the only pair
    {"g": 8, "lcm": 20},           # g does not divide the lcm: impossible
    {"g": 20, "lcm": 50401},
]


def solve(g=20, lcm=50400):
    """g(a + b) minimised over coprime a·b = lcm/g."""
    if g <= 0 or lcm <= 0 or lcm % g:
        return None
    quotient = lcm // g
    best = None
    for a in range(1, isqrt(quotient) + 1):
        if quotient % a:
            continue
        b = quotient // a
        if gcd(a, b) != 1:
            continue
        total = g * (a + b)
        best = total if best is None else min(best, total)
    return best


def check(g=20, lcm=50400):
    """Independent: search the pairs themselves and test gcd and lcm as printed.

    Every m that is a multiple of g and a divisor of the lcm is tried, its partner
    comes from ``m·n = g·lcm``, and the pair is kept only when ``gcd(m, n)`` really
    is g and ``lcm(m, n)`` really is the lcm — the arithmetic the closed form assumes.
    """
    if g <= 0 or lcm <= 0:
        return None
    best = None
    for m in range(g, lcm + 1, g):
        if lcm % m or (g * lcm) % m:
            continue
        n = g * lcm // m
        if gcd(m, n) == g and m * n // gcd(m, n) == lcm:
            best = m + n if best is None else min(best, m + n)
    return best
