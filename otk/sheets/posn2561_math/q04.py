"""ข้อ 4 — ค่า m + n ที่น้อยที่สุด

จงหาค่า m + n ที่น้อยที่สุด เมื่อกำหนดให้ m และ n เป็นจำนวนนับที่มี ห.ร.ม. และ
ค.ร.น. เป็น 30 และ 5400 ตามลำดับ

With m = 30a and n = 30b the lcm is 30ab, so ``ab = 5400/30 = 180 = 2²·3²·5``
and a, b must be **coprime** — each prime power goes wholly to one side. The
three prime powers give 2³ = 8 ordered splits, i.e. four unordered ones:

    1 · 180 → 181     4 · 45 → 49     9 · 20 → **29**     5 · 36 → 41

so the answer is ``30 · 29 =`` **870**, from the pair (270, 600).

As on the 2562 sheet, the pull is to make the two cofactors as equal as possible
— √180 ≈ 13.4 — but coprimality only allows the eight unitary divisors, and 9·20
is the closest such split.

``solve`` enumerates the coprime factorisations of lcm/gcd. ``check`` walks the
divisors of the lcm that are multiples of the gcd and tests both quantities
directly with the Euclidean algorithm.
"""

from __future__ import annotations

from math import gcd, isqrt

#: the pair's gcd and lcm.
PARAMS = {"g": 30, "lcm": 5400}
ANSWER = 870
VARIANTS = [
    {"g": 20, "lcm": 50400},
    {"g": 1, "lcm": 180},
    {"g": 7, "lcm": 7},            # m = n = 7
    {"g": 6, "lcm": 3600},
    {"g": 8, "lcm": 20},           # g does not divide the lcm
    {"g": 30, "lcm": 5401},
]


def solve(g=30, lcm=5400):
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
        best = g * (a + b) if best is None else min(best, g * (a + b))
    return best


def check(g=30, lcm=5400):
    """Independent: search the pairs and test gcd and lcm as printed.

    Each m that is a multiple of g and a divisor of the lcm is tried with its
    partner from ``m·n = g·lcm``, and the pair counts only when ``gcd(m, n)``
    really is g and ``lcm(m, n)`` really is the lcm.
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
