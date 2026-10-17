"""ข้อ 12 — gcd(a₁, …, a₂₅₄₉) เมื่อ aₙ = 2^(3n−1) + 3^(6n−2) + 5^(6n−3)

``solve`` runs gcd(g, aₙ) = gcd(g, aₙ mod g) with modular powers, starting from
a₁ = 210: the answer is 14 (every term is even, and 2³ ≡ 3⁶ ≡ 5⁶ ≡ 1 (mod 7)
makes aₙ ≡ 4 + 4 + 6 ≡ 0).

``check`` works prime by prime: the gcd divides a₁, so for each prime power
p^k dividing a₁ it tests whether every aₙ (n ≤ N) is divisible by p^k.
"""

from __future__ import annotations

from math import gcd

PARAMS = {"shifts": (1, 2, 3), "last": 2549}
ANSWER = 14
VARIANTS = [{"shifts": (0, 1, 5), "last": 2336}, {"shifts": (1, 1, 1)}, {"shifts": (2, 0, 2), "last": 50}, {"last": 1}]


def _term_mod(n, shifts, modulus):
    i, j, k = shifts
    return (pow(2, 3 * n - i, modulus) + pow(3, 6 * n - j, modulus) + pow(5, 6 * n - k, modulus)) % modulus


def solve(shifts=(1, 2, 3), last=2549):
    i, j, k = shifts
    g = 2 ** (3 - i) + 3 ** (6 - j) + 5 ** (6 - k)
    for n in range(2, last + 1):
        g = gcd(g, _term_mod(n, shifts, g))
        if g == 1:
            break
    return g


def check(shifts=(1, 2, 3), last=2549):
    i, j, k = shifts
    a1 = 2 ** (3 - i) + 3 ** (6 - j) + 5 ** (6 - k)
    result, n, p = 1, a1, 2
    while n > 1:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            best = 0
            for power in range(1, e + 1):
                if all(_term_mod(t, shifts, p**power) == 0 for t in range(1, last + 1)):
                    best = power
                else:
                    break
            result *= p**best
        p += 1
    return result
