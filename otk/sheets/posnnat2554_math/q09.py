"""ข้อ 9 — 1/1 + 1/3 + ⋯ + 1/(2n − 1) ไม่เป็นจำนวนเต็ม (n > 1)  (พิสูจน์)

Let 3^t ≤ 2n − 1 < 3^(t+1). The only odd multiple of 3^t up to 2n − 1 is 3^t
itself, so 1/3^t is the one term with the full power of 3 and the reduced
denominator keeps 3^t; t ≥ 1 for n > 1. The solver returns t (n = 10: 2).

``check`` adds the fractions exactly and counts the 3s in the denominator.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"n": 10}
ANSWER = 2
VARIANTS = [{"n": 2}, {"n": 14}, {"n": 41}, {"n": 200}]


def solve(n=10):
    t = 0
    while 3 ** (t + 1) <= 2 * n - 1:
        t += 1
    return t


def check(n=10):
    total = sum((Fraction(1, k) for k in range(1, 2 * n, 2)), Fraction(0))
    den, t = total.denominator, 0
    while den % 3 == 0:
        den //= 3
        t += 1
    return t
