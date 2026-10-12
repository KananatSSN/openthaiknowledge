"""ข้อ 19 — ความน่าจะเป็นที่ x² + ax + b = 0 จะมีคำตอบเดียว

กำหนดให้ n ≥ 2 เป็นจำนวนนับ สุ่มเลือกจำนวนนับ a, b โดยที่ a, b ∈ {1, 2, …, n²}
จงหาความน่าจะเป็นที่สมการ x² + ax + b = 0 จะมีคำตอบเดียว

"One solution" means a repeated root, i.e. a² = 4b. So a must be even, a = 2m,
and then b = m² — and the only constraint left is that b stay in range:

    m² ≤ n²  ⟺  m ≤ n

while a = 2m ≤ n² is automatic for n ≥ 2. That is exactly **n** favourable pairs
out of n⁴, so the probability is **1/n³**.

The pretty part is that the bound on b, not the bound on a, is what bites — the
count is n rather than n²/2 because the square grows faster than the double.

``solve`` returns that closed form. ``check`` counts the pairs, but from the
other side: it walks b and asks whether 4b is a perfect square whose root is in
range, so it never parametrises by m.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: a, b drawn uniformly from 1 … n².
PARAMS = {"n": 5}
ANSWER = Fraction(1, 125)
VARIANTS = [
    {"n": 2},
    {"n": 3},
    {"n": 7},
    {"n": 10},
    {"n": 12},
    {"n": 1},          # n ≥ 2 is printed; n = 1 leaves a single pair
]


def solve(n=5):
    """1/n³ — n favourable pairs out of n⁴."""
    if n < 2:
        return None
    return Fraction(1, n ** 3)


def check(n=5):
    """Independent: count over b instead of over the repeated root.

    For each b in range, a discriminant of zero needs a = √(4b) to be a whole
    number that is itself in range. Nothing here knows that b must be a perfect
    square or that the count comes to n.
    """
    if n < 2:
        return None
    top = n * n
    if top > 4000:
        return None
    favourable = 0
    for b in range(1, top + 1):
        root = math.isqrt(4 * b)
        if root * root == 4 * b and 1 <= root <= top:
            favourable += 1
    return Fraction(favourable, top * top)
