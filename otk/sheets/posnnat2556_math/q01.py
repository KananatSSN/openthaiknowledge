"""ข้อ 1 — จำนวนเต็มมากสุดที่หาร p⁴ − 1 ทุกจำนวนเฉพาะ p > 4

By Dirichlet the primes above the bound meet every residue class prime to any
modulus, so q^e divides them all iff q ≤ bound and the unit group mod q^e has
exponent dividing k. That group is cyclic of order q^(e−1)(q − 1) for odd q;
for q = 2 its exponent is 1, 2, then 2^(e−2). The bound 4 lets p = 5 in, so 5
does not divide the answer: 2⁴·3 = 48.

``check`` takes the gcd of pᵏ − 1 over the actual primes up to 3000.
"""

from __future__ import annotations

from math import gcd

PARAMS = {"k": 4, "bound": 4}
ANSWER = 48
VARIANTS = [{"k": 2, "bound": 3}, {"k": 4, "bound": 5}, {"k": 6, "bound": 7}, {"k": 2, "bound": 2}]


def _is_prime(n):
    return n > 1 and all(n % d for d in range(2, int(n**0.5) + 1))


def _unit_exponent(q, e):
    if q == 2:
        return 1 if e == 1 else 2 if e == 2 else 2 ** (e - 2)
    return q ** (e - 1) * (q - 1)


def solve(k=4, bound=4):
    result = 1
    for q in range(2, bound + 1):
        if not _is_prime(q):
            continue
        e = 0
        while k % _unit_exponent(q, e + 1) == 0:
            e += 1
        result *= q**e
    return result


def check(k=4, bound=4):
    g = 0
    for p in range(bound + 1, 3000):
        if _is_prime(p):
            g = gcd(g, p**k - 1)
    return g
