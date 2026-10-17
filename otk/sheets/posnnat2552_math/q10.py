"""ข้อ 10 — 1/2² + 1/4² + ⋯ + 1/(p − 1)² = a/b ⇒ p | a  (พิสูจน์)

Σ 1/(2k)² = (1/4)Σ_{k ≤ (p−1)/2} 1/k², and since k and p − k have equal squares
mod p, that half sum is half of Σ_{k<p} k⁻² ≡ Σk² ≡ 0 (p ≥ 5). The solver
returns the sum modulo p via modular inverses: 0.

``check`` adds the exact fractions and reduces the numerator modulo p.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"p": 7}
ANSWER = 0
VARIANTS = [{"p": 11}, {"p": 13}, {"p": 31}]


def solve(p=7):
    return sum(pow((2 * k) ** 2, -1, p) for k in range(1, (p - 1) // 2 + 1)) % p


def check(p=7):
    total = sum((Fraction(1, (2 * k) ** 2) for k in range(1, (p - 1) // 2 + 1)), Fraction(0))
    return total.numerator % p
