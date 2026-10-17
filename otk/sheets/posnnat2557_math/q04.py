"""ข้อ 4 — พหุนาม P ที่ P(n) | 2557ⁿ + 213 × 2014 ทุก n

A prime p | P(n) divides P(n + kp), so p | bᵐ + K for all m ≥ n and, by
Fermat, p | b(b − 1); P's values have finitely many prime factors, so P is
constant (Schur), a divisor ±d of g = gcd over n of bⁿ + K. Consecutive
differences are bⁿ(b − 1), so g = gcd(b + K, b(b − 1)). For the source
g = gcd(2557 + 428982, 2557·2556) = 1: P = ±1. The answer is the sorted tuple
of the constant polynomials.

``check`` takes the gcd of bⁿ + K over n = 1..60 directly and lists ±d.
"""

from __future__ import annotations

from math import gcd

PARAMS = {"base": 2557, "constant": 213 * 2014}
ANSWER = (-1, 1)
VARIANTS = [{"base": 3, "constant": 1}, {"base": 5, "constant": 3}, {"base": 7, "constant": 5}]


def solve(base=2557, constant=213 * 2014):
    g = gcd(base + constant, base * (base - 1))
    divisors = [d for d in range(1, g + 1) if g % d == 0]
    return tuple(sorted([-d for d in divisors] + divisors))


def check(base=2557, constant=213 * 2014):
    g = 0
    for n in range(1, 61):
        g = gcd(g, base**n + constant)
    return tuple(sorted(s * d for d in range(1, g + 1) if g % d == 0 for s in (1, -1)))
