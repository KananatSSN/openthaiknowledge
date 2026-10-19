"""ข้อ 18 — Σₖ₌₂²⁵⁵⁰ pₖ^(pₖ⁴ − 1) มอดุโล 2550

2550 = 2·3·5²·17 and λ(2550) = 80 divides p⁴ − 1 for every p coprime to 2550,
so those terms are 1; only p = 3, 5, 17 need computing. Total 1273.

``check`` evaluates every term with a modular power.
"""

from __future__ import annotations

PARAMS = {"last": 2550, "modulus": 2550}
ANSWER = 1273
VARIANTS = [{"last": 40, "modulus": 510}, {"last": 517, "modulus": 1530}, {"last": 3000, "modulus": 4080}, {"last": 2}]


def _primes(count):
    out, n = [], 2
    while len(out) < count:
        if all(n % q for q in out if q * q <= n):
            out.append(n)
        n += 1
    return out


def solve(last=2550, modulus=2550):
    primes = _primes(last)[1:]
    special = [p for p in primes if modulus % p == 0]
    return (len(primes) - len(special) + sum(pow(p, p**4 - 1, modulus) for p in special)) % modulus


def check(last=2550, modulus=2550):
    return sum(pow(p, p**4 - 1, modulus) for p in _primes(last)[1:]) % modulus
