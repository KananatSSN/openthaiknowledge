"""ข้อ 2 — 2a(a² + b²)/(a² − b²) ไม่เป็นจำนวนเต็ม  (พิสูจน์)

For the family k·a(a² + b²)/(a² − b²) with gcd(a, b) = 1: a² − b² is prime to
a and shares at most 2 with a² + b², so it divides 2k, and a² − b² ≥ a + b
leaves only a + b ≤ 2k. The source (k = 2) has a² − b² | 4, impossible for
a > b ≥ 1 coprime (a² − b² = 3 fails 3 | 4·2·5). The solver counts the pairs
a > b ≥ 1 that work.

``check`` tries every coprime pair with a up to 6k + 10, testing the quotient
directly.
"""

from __future__ import annotations

from math import gcd

PARAMS = {"k": 2}
ANSWER = 0
VARIANTS = [{"k": 3}, {"k": 6}, {"k": 12}, {"k": 30}]


def solve(k=2):
    count = 0
    for total in range(3, 2 * k + 1):
        for b in range(1, (total + 1) // 2):
            a = total - b
            d = a * a - b * b
            if gcd(a, b) == 1 and (2 * k) % d == 0 and k * a * (a * a + b * b) % d == 0:
                count += 1
    return count


def check(k=2):
    return sum(1 for a in range(2, 6 * k + 11) for b in range(1, a)
               if gcd(a, b) == 1 and (k * a * (a * a + b * b)) % (a * a - b * b) == 0)
