"""วันที่สอง ข้อ 2 — N ที่มีตัวประกอบเฉพาะต่างกันอย่างน้อยสองตัว และ N = d₁² + d₂² + d₃² + d₄²

Parity forces N even with d₂ = 2, then d₃ = p prime and d₄ = 2p, so
N = 5(1 + p²) and p = 5: N = 130. The solver searches N ≤ bound directly.

``check`` goes the other way: it runs over candidate (d₂, d₃, d₄), forms
N = 1 + d₂² + d₃² + d₄², and keeps N whose four smallest divisors are exactly
those and which has two distinct prime factors.
"""

from __future__ import annotations

PARAMS = {"bound": 3000}
ANSWER = (130,)
VARIANTS = [{"bound": 100}, {"bound": 6000}, {"bound": 131}]


def _small_divisors(n, count):
    out = []
    for d in range(1, n + 1):
        if n % d == 0:
            out.append(d)
            if len(out) == count:
                break
    return out


def _distinct_primes(n):
    count, f = 0, 2
    while f * f <= n:
        if n % f == 0:
            count += 1
            while n % f == 0:
                n //= f
        f += 1
    return count + (n > 1)


def solve(bound=3000):
    return tuple(n for n in range(2, bound + 1)
                 if _distinct_primes(n) >= 2 and len(_small_divisors(n, 4)) == 4
                 and sum(d * d for d in _small_divisors(n, 4)) == n)


def check(bound=3000):
    found = set()
    for d2 in range(2, 60):
        for d3 in range(d2 + 1, 60):
            for d4 in range(d3 + 1, 60):
                n = 1 + d2 * d2 + d3 * d3 + d4 * d4
                if n <= bound and _small_divisors(n, 4) == [1, d2, d3, d4] and _distinct_primes(n) >= 2:
                    found.add(n)
    return tuple(sorted(found))
