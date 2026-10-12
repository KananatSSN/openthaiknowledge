"""ข้อ 11 — ค่าของ m + p

ให้ m เป็นจำนวนเต็มบวก โดยที่เศษเหลือจากการหาร 555 และ 670 ด้วย m มีค่าเท่ากัน คือ p
ถ้า p เป็นจำนวนเฉพาะบวก จงหาค่าของ m + p

Equal remainders means the *difference* is divisible by m:

    670 − 555 = 115 = 5 · 23   ⟹  m ∈ {1, 5, 23, 115}

and each candidate is then tested on the remainder itself:

    m = 1   → p = 0    ✗ not prime
    m = 5   → p = 0    ✗ (both numbers are multiples of 5)
    m = 23  → p = 3    ✓ (555 = 23·24 + 3, 670 = 23·29 + 3)
    m = 115 → p = 95   ✗ = 5·19

So m = 23, p = 3 and **m + p = 26**.

The primality is what picks a single divisor out of the four; without it the
question has no answer at all.

``solve`` factors the difference and tests each divisor; ``check`` sweeps every
modulus up to the larger number and compares the two remainders directly, never
using the fact that m must divide the difference.
"""

from __future__ import annotations

from math import isqrt

#: the two numbers whose remainders coincide.
PARAMS = {"x": 555, "y": 670}
ANSWER = 26
VARIANTS = [
    {"x": 96, "y": 117},
    {"x": 269, "y": 284},
    {"x": 213, "y": 219},
    {"x": 104, "y": 225},
    {"x": 555, "y": 555},        # every m works: hopelessly ambiguous
    {"x": 12, "y": 18},          # no divisor leaves a prime remainder
]


def _is_prime(n: int) -> bool:
    return n >= 2 and all(n % f for f in range(2, isqrt(n) + 1))


def solve(x=555, y=670):
    """m + p, where m divides y − x and the shared remainder p is prime."""
    if x <= 0 or y <= 0 or x == y:
        return None
    gap = abs(y - x)
    hits = set()
    for m in range(1, gap + 1):
        if gap % m:
            continue
        p = x % m
        if _is_prime(p):
            hits.add((m, p))
    if len(hits) != 1:
        return None
    m, p = next(iter(hits))
    return m + p


def check(x=555, y=670):
    """Independent: try every modulus and compare the two remainders as printed.

    No divisibility argument is used — each m from 1 up to the larger number is
    tried, ``x % m`` and ``y % m`` are compared directly, and the modulus is kept
    only when they agree and the shared value is prime by trial division.
    """
    if x <= 0 or y <= 0 or x == y:
        return None
    hits = set()
    for m in range(1, max(x, y) + 1):
        if x % m == y % m and _is_prime(x % m):
            hits.add((m, x % m))
    if len(hits) != 1:
        return None
    m, p = next(iter(hits))
    return m + p
