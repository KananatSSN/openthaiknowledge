"""ข้อ 13 — 29³⁰ + 31²⁸ + 28!(30!) มอดุโล 29·31

Twin primes p, q = p + 2. Mod p: p^(q−1) ≡ 0, q^(p−1) ≡ 1 (Fermat), and
(q − 1)! ≡ 0, so the sum is 1. Mod q: p^(q−1) ≡ 1, q^(p−1) ≡ 0, and Wilson with
(q − 1)! = (q − 1)(q − 2)(p − 1)! ≡ 2(p − 1)! gives (p − 1)! ≡ −1/2, so the
last term is (−1/2)(−1) = 1/2 and the sum is 3/2. The Chinese remainder theorem
then gives 668.

``check`` computes the three terms directly modulo pq.
"""

from __future__ import annotations

from math import factorial

PARAMS = {"p": 29}
ANSWER = 668
VARIANTS = [{"p": 11}, {"p": 17}, {"p": 41}, {"p": 107}]


def solve(p=29):
    q = p + 2
    r_q = 3 * pow(2, -1, q) % q
    return next(x for x in range(1, p * q) if x % p == 1 and x % q == r_q)


def check(p=29):
    q, n = p + 2, p * (p + 2)
    return (pow(p, q - 1, n) + pow(q, p - 1, n) + factorial(p - 1) * factorial(q - 1)) % n
