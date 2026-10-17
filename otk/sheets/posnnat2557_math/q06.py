"""ข้อ 6 — จำนวนเฉพาะ p ที่ 2p² − 3p − 1 เป็นกำลังสาม

For the family αp² − βp − 1 = n³: p(αp − β) = (n + 1)(n² − n + 1), so p divides
one factor.

- p | n + 1, n = jp − 1: j(j²p² − 3jp + 3) = αp − β, a quadratic in p with
  2j³ < 3j² + α, so finitely many j.
- n² − n + 1 = mp: then m(n + 1) = αp − β gives αn² − (α + m²)n +
  (α − m² − βm) = 0. Its discriminant is (m² + 3α)² + 4αβm − 12α², a square
  only if m = 3α/β or m ≤ 2αβ, so finitely many m.

The solver runs both finite searches and keeps the primes that satisfy the
equation. The source (α, β = 2, 3) gives p = 2, 3; the case p | n² − n + 1 is
not empty in general (α, β = 13, 52 adds p = 67, 38³).

``check`` tests every prime below 20000 for an exact integer cube root.
"""

from __future__ import annotations

from math import isqrt

PARAMS = {"alpha": 2, "beta": 3}
ANSWER = (2, 3)
VARIANTS = [{"alpha": 4, "beta": 7}, {"alpha": 7, "beta": 18}, {"alpha": 13, "beta": 52}, {"alpha": 17, "beta": 88}]  # pairs (2, 5), (3, 7), (5, 11), (7, 13)


def _is_prime(n):
    return n > 1 and all(n % d for d in range(2, isqrt(n) + 1))


def _int_roots(a, b, c):
    """Integer roots of ax² + bx + c."""
    disc = b * b - 4 * a * c
    if disc < 0:
        return ()
    r = isqrt(disc)
    if r * r != disc:
        return ()
    return tuple(x // (2 * a) for x in {-b - r, -b + r} if x % (2 * a) == 0)


def solve(alpha=2, beta=3):
    found = set()
    j = 1
    while 2 * j**3 < 3 * j * j + alpha + 1:
        for p in _int_roots(j**3, -(3 * j * j + alpha), 3 * j + beta):
            if p >= 2 and _is_prime(p) and alpha * p * p - beta * p - 1 == (j * p - 1) ** 3:
                found.add(p)
        j += 1
    for m in range(1, 2 * alpha * beta + 3 * alpha + 2):
        for n in _int_roots(alpha, -(alpha + m * m), alpha - m * m - beta * m):
            if n >= 1 and (n * n - n + 1) % m == 0:
                p = (n * n - n + 1) // m
                if _is_prime(p) and alpha * p * p - beta * p - 1 == n**3:
                    found.add(p)
    return tuple(sorted(found))


def _cube_root(v):
    if v <= 0:
        return None
    r = round(v ** (1 / 3))
    for c in (r - 1, r, r + 1):
        if c > 0 and c**3 == v:
            return c
    return None


def check(alpha=2, beta=3):
    sieve = bytearray([1]) * 20000
    sieve[0] = sieve[1] = 0
    for i in range(2, 142):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(range(i * i, 20000, i)))
    return tuple(p for p in range(20000) if sieve[p] and _cube_root(alpha * p * p - beta * p - 1))
