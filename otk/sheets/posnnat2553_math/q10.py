"""ข้อ 10 — จำนวนเฉพาะ p ที่ p | C(100, p) + 7

For p > N the binomial is 0 and p would divide 7 ≤ N anyway; otherwise test
each p ≤ max(N, c) directly: p = 7.

``check`` uses Lucas: C(N, p) ≡ ⌊N/p⌋ (mod p), so p | ⌊N/p⌋ + c.
"""

from __future__ import annotations

from math import comb

PARAMS = {"n": 100, "c": 7}
ANSWER = (7,)
VARIANTS = [{"n": 50, "c": 3}, {"n": 200, "c": 11}, {"n": 30, "c": 1}]


def _primes(limit):
    return [p for p in range(2, limit + 1) if all(p % d for d in range(2, int(p**0.5) + 1))]


def solve(n=100, c=7):
    return tuple(p for p in _primes(max(n, c)) if (comb(n, p) + c) % p == 0)


def check(n=100, c=7):
    return tuple(p for p in _primes(max(n, c)) if (n // p + c) % p == 0)
