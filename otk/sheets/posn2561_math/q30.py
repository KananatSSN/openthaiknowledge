"""ข้อ 30 — จำนวนตัวหารบวกที่เป็นจำนวนกำลังสอง

จงหาตัวหารบวกทั้งหมดของ 2³·3⁵·5⁷·7² ที่เป็นจำนวนกำลังสอง

A divisor is ``2^a·3^b·5^c·7^d`` with a ≤ 3, b ≤ 5, c ≤ 7, d ≤ 2, and it is a
perfect square exactly when every exponent is even. So each prime contributes
independently, ``⌊e/2⌋ + 1`` choices apiece:

    a ∈ {0,2}      b ∈ {0,2,4}      c ∈ {0,2,4,6}      d ∈ {0,2}

    2 · 3 · 4 · 2 = **48**

The sheet's wording ("จงหาตัวหารบวกทั้งหมด … ที่เป็นจำนวนกำลังสอง") asks for the
divisors themselves; as a single number the answer is how many there are. The
generated question says "จงหาจำนวนตัวหารบวก…" so that no draw is ambiguous.

``solve`` multiplies the ⌊e/2⌋ + 1. ``check`` builds every divisor of the number
and tests each one with ``isqrt``, which needs neither the exponent argument nor
the independence of the primes.
"""

from __future__ import annotations

from math import isqrt, prod

#: the number as ((prime, exponent), …).
PARAMS = {"factorization": ((2, 3), (3, 5), (5, 7), (7, 2))}
ANSWER = 48
VARIANTS = [
    {"factorization": ((2, 10),)},
    {"factorization": ((2, 4), (3, 4))},
    {"factorization": ((3, 1), (5, 1), (7, 1))},        # only 1 is a square
    {"factorization": ((2, 6), (5, 3), (11, 2))},
    {"factorization": ((2, 2), (3, 2), (5, 2), (7, 2), (11, 2))},
    {"factorization": ((13, 9), (2, 1))},
]


def solve(factorization=((2, 3), (3, 5), (5, 7), (7, 2))):
    """Every prime chooses an even exponent, independently."""
    if not factorization or any(e < 0 or p < 2 for p, e in factorization):
        return None
    if len({p for p, _ in factorization}) != len(factorization):
        return None
    return prod(e // 2 + 1 for _, e in factorization)


def check(factorization=((2, 3), (3, 5), (5, 7), (7, 2))):
    """Independent: list every divisor and test whether it is a square."""
    if not factorization or any(e < 0 or p < 2 for p, e in factorization):
        return None
    if len({p for p, _ in factorization}) != len(factorization):
        return None
    if prod(e + 1 for _, e in factorization) > 2 * 10 ** 5:
        return None

    divisors = [1]
    for prime, exponent in factorization:
        divisors = [d * prime ** i for d in divisors for i in range(exponent + 1)]
    return sum(1 for d in divisors if isqrt(d) ** 2 == d)
