"""ข้อ 9 — มีลำดับ dᵢ ที่ติดกันและไม่เป็นกำลังสมบูรณ์  (พิสูจน์)

Choosing N + i ≡ pᵢ (mod pᵢ²) for distinct primes pᵢ makes pᵢ divide N + i
exactly once, so no N + i is a perfect power; the Chinese remainder theorem
gives the least such N. The solver builds it modulus by modulus
(2, 3, 5: the residue mod 900).

``check`` tries every N below Π pᵢ² directly.
"""

from __future__ import annotations

PARAMS = {"primes": (2, 3, 5)}
ANSWER = 577
VARIANTS = [{"primes": (3, 2)}, {"primes": (5, 7)}, {"primes": (2, 3, 5, 7)}, {"primes": (7, 2, 3)}]


def solve(primes=(2, 3, 5)):
    modulus, residue = 1, 0
    for i, p in enumerate(primes, 1):
        m = p * p
        target = (p - i) % m
        step = (target - residue) * pow(modulus, -1, m) % m
        residue += modulus * step
        modulus *= m
    return residue


def check(primes=(2, 3, 5)):
    total = 1
    for p in primes:
        total *= p * p
    for n in range(total):
        if all((n + i) % (p * p) == p for i, p in enumerate(primes, 1)):
            for i, p in enumerate(primes, 1):
                assert (n + i) % p == 0 and (n + i) % (p * p) != 0
            return n
    raise AssertionError
