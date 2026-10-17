"""ข้อ 10 — Σₖ₌₁²⁰⁰⁵ k^(2005·2²⁰⁰⁵) มอดุโล 2²⁰⁰⁵

Odd k: the unit group mod 2^M has exponent 2^(M − 2), which divides the
exponent, so k^E ≡ 1. Even k: 2^E divides k^E and E ≥ M. The sum is the number
of odd k ≤ N: 1003.

``check`` computes every odd term as (k^M)^(2^M) by M masked squarings
(even terms are 0 since E ≥ M), and adds them modulo 2^M.
"""

from __future__ import annotations

PARAMS = {"last": 2005, "m": 2005}
ANSWER = 1003
VARIANTS = [{"last": 40, "m": 12}, {"last": 351, "m": 287}, {"last": 7, "m": 3}, {"last": 100, "m": 64}]


def solve(last=2005, m=2005):
    return (last + 1) // 2 % 2**m


def check(last=2005, m=2005):
    mask = (1 << m) - 1
    total = 0
    for k in range(1, last + 1, 2):
        y = pow(k, m, 1 << m)
        for _ in range(m):
            y = (y * y) & mask
        total += y
    return total & mask
