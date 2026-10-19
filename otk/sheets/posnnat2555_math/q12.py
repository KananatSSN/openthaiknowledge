"""ข้อ 12 — a/b + b/c + c/a เป็นจำนวนเต็ม ⇒ abc เป็นกำลังสาม  (พิสูจน์)

For a prime with exponents α, β, γ, a²c + b²a + c²b ≡ 0 (mod abc) forces the two
smallest of 2α + γ, 2β + α, 2γ + β to be equal, which gives α + β + γ ≡ 0
(mod 3). The solver counts the triples with gcd 1 and entries ≤ L by the
divisibility test, and asserts that each abc is a cube (L = 20).

``check`` tests the sum a/b + b/c + c/a as an exact fraction instead.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd

PARAMS = {"limit": 20}
ANSWER = 10
VARIANTS = [{"limit": 4}, {"limit": 12}, {"limit": 30}]


def solve(limit=20):
    count = 0
    for a in range(1, limit + 1):
        for b in range(1, limit + 1):
            for c in range(1, limit + 1):
                if gcd(gcd(a, b), c) == 1 and (a * a * c + b * b * a + c * c * b) % (a * b * c) == 0:
                    root = round((a * b * c) ** (1 / 3))
                    assert root**3 == a * b * c
                    count += 1
    return count


def check(limit=20):
    return sum(1 for a in range(1, limit + 1) for b in range(1, limit + 1) for c in range(1, limit + 1)
               if gcd(gcd(a, b), c) == 1 and (Fraction(a, b) + Fraction(b, c) + Fraction(c, a)).denominator == 1)
