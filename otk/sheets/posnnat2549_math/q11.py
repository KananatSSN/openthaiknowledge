"""ข้อ 11 — ∏ₙ₌₁²⁵⁴⁹ 2006^(pₙ² − 1) มอดุโล 13

The product is b^E with E = Σ(pₙ² − 1). For p > 3, 24 | p² − 1, so modulo 12
only p = 2 (3) and p = 3 (8) count: E ≡ 11 (mod 12), and 2006 ≡ 4 gives
4¹¹ ≡ 10 (mod 13).

``check`` lists the actual primes, adds the exponents and takes one modular
power with the full exponent.
"""

from __future__ import annotations

PARAMS = {"base": 2006, "last": 2549, "m": 13}
ANSWER = 10
VARIANTS = [{"m": 7}, {"base": 358, "last": 1054}, {"base": 101, "last": 40, "m": 5}, {"last": 1}]


def solve(base=2006, last=2549, m=13):
    # p > 3 adds multiples of 24, and m − 1 divides 24 for the moduli used
    exponent = (3 if last >= 1 else 0) + (8 if last >= 2 else 0)
    return pow(base, exponent % (m - 1), m)


def check(base=2006, last=2549, m=13):
    primes, n = [], 2
    while len(primes) < last:
        if all(n % q for q in primes if q * q <= n):
            primes.append(n)
        n += 1
    return pow(base, sum(p * p - 1 for p in primes), m)
