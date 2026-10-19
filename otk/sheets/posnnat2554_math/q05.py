"""ข้อ 5 — n ทั้งหมดที่ n = d(n)⁴

n is a fourth power Πp^(4a) and d(n) = Π(4a + 1) is odd, so n is odd; then
4a + 1 ≤ p^a with equality only for (p, a) = (5, 1), (3, 2), leaving
1, 625, 6561, 4100625. ``solve`` searches n = m⁴ for m ≤ bound.

``check`` builds n from exponent vectors on the primes 3, 5, 7, 11, 13 (odd n,
small exponents) and keeps those with d(n)⁴ = n.
"""

from __future__ import annotations

from itertools import product

PARAMS = {"bound": 60}
ANSWER = (1, 625, 6561, 4100625)
VARIANTS = [{"bound": 5}, {"bound": 26}, {"bound": 80}]


def _d(n):
    count, f = 1, 2
    while f * f <= n:
        e = 0
        while n % f == 0:
            n //= f
            e += 1
        count *= e + 1
        f += 1
    return count * (2 if n > 1 else 1)


def solve(bound=60):
    return tuple(m**4 for m in range(1, bound + 1) if _d(m**4) ** 4 == m**4)


def check(bound=60):
    found = set()
    for exps in product(range(0, 4), repeat=5):
        n = 1
        for p, a in zip((3, 5, 7, 11, 13), exps):
            n *= p ** (4 * a)
        if n <= bound**4 and _d(n) ** 4 == n:
            found.add(n)
    return tuple(sorted(found))
