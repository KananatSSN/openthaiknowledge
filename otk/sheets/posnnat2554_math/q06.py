"""ข้อ 6 — ค่าสูงสุดของ Σ(xᵢ − m)² เมื่อ 0 ≤ xᵢ ≤ 1 (2011 ตัว)

Σ(xᵢ − m)² = Σxᵢ² − (Σxᵢ)²/N is convex in each xᵢ, so the maximum is at a
vertex: k ones give k(N − k)/N, largest at k = ⌊N/2⌋: 1005·1006/2011.

``check`` evaluates the sum exactly for every vertex count k of ones.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"n": 2011}
ANSWER = Fraction(1011030, 2011)
VARIANTS = [{"n": 1}, {"n": 2}, {"n": 10}, {"n": 99}]


def solve(n=2011):
    k = n // 2
    return Fraction(k * (n - k), n)


def check(n=2011):
    best = Fraction(0)
    for k in range(n + 1):
        mean = Fraction(k, n)
        best = max(best, k * (1 - mean) ** 2 + (n - k) * mean**2)
    return best
