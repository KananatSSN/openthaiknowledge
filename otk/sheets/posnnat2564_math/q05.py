"""ข้อ 5 — (p, m, k) ที่ m⁴ + 4ᵏp⁴ | m²(m⁴ − 4ᵏp⁴)

For the family with m^e in place of m²: if p ∤ m, then m⁴ + 4ᵏp⁴ is prime to m
(m odd) and must divide m⁴ − 4ᵏp⁴, which is smaller and non-zero. So m = pt,
and t⁴ + 4ᵏ, prime to t and to t⁴ − 4ᵏ, divides p^e. Sophie Germain gives
t⁴ + 4ᵏ = ((t − v)² + v²)((t + v)² + v²) with v = 2^((k−1)/2); the two factors
are coprime, so the smaller is 1: t = v = 1, k = 1, and 5 | p^e gives p = 5
(none when e = 0). The answer is the tuple of triples.

``check`` searches primes p < 60, odd m < 400 and odd k < 12 directly.
"""

from __future__ import annotations

PARAMS = {"e": 2}
ANSWER = ((5, 5, 1),)
VARIANTS = [{"e": 0}, {"e": 4}, {"e": 6}]


def _prime_power(n):
    """(p, j) with n = p^j for a prime p, else None."""
    p = next(d for d in range(2, n + 1) if n % d == 0)
    j = 0
    while n % p == 0:
        n //= p
        j += 1
    return (p, j) if n == 1 else None


def solve(e=2):
    found = []
    for k in range(1, 12, 2):
        v = 2 ** ((k - 1) // 2)
        for t in range(1, 400, 2):
            if (t - v) ** 2 + v * v == 1:
                power = _prime_power(t**4 + 4**k)  # t⁴ + 4ᵏ must divide p^e
                if power and 1 <= power[1] <= e:
                    found.append((power[0], power[0] * t, k))
    return tuple(sorted(found))


def check(e=2):
    primes = [p for p in range(2, 60) if all(p % d for d in range(2, p))]
    found = []
    for p in primes:
        for m in range(1, 400, 2):
            for k in range(1, 12, 2):
                n = m**4 + 4**k * p**4
                if (m**e * (m**4 - 4**k * p**4)) % n == 0:
                    found.append((p, m, k))
    return tuple(sorted(found))
