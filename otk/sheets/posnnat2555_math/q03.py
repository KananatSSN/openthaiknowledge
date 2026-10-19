"""ข้อ 3 — ⌊(m^(φ(n)+1) + n^(φ(m)+1))/(mn)⌋ เป็นจำนวนคู่  (พิสูจน์)

Mod m the sum is n·n^φ(m) ≡ n, mod n it is m, so it is ≡ m + n (mod mn) and the
remainder is m + n (< mn). For odd m, n both the sum and m + n are even, so the
quotient is even. The solver returns the remainder (m = 3, n = 5: 8).

``check`` computes the sum exactly and reduces it.
"""

from __future__ import annotations

from math import gcd

PARAMS = {"m": 3, "n": 5}
ANSWER = 8
VARIANTS = [{"m": 7, "n": 9}, {"m": 15, "n": 11}, {"m": 21, "n": 25}]


def _phi(n):
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


def solve(m=3, n=5):
    return (m + n) % (m * n)


def check(m=3, n=5):
    total = m ** (_phi(n) + 1) + n ** (_phi(m) + 1)
    assert (total // (m * n)) % 2 == 0
    return total % (m * n)
