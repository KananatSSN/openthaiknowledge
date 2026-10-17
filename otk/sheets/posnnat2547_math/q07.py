"""ข้อ 7 — f(n) = 2f(n − 1) − f(n − 2) + (−1)ⁿ(2n − 4), f(0) = 0, f(1) = 1

g(n) = (n + 1)/2 + (−1)ⁿ(n − 1)/2 solves the recurrence with g(0) = 0, g(1) = 1
(it is n for even n and 1 for odd n); adding the homogeneous solution A + Bn
fits other starts: f(n) = g(n) + f(0) + (f(1) − f(0) − 1)n. The sheet asks for
f(n) as a formula; PARAMS evaluates it at n = 2547.

``check`` iterates the recurrence.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"f0": 0, "f1": 1, "n": 2547}
ANSWER = 1
VARIANTS = [{"n": 2548}, {"f0": -3, "f1": 4, "n": 42}, {"f0": 5, "f1": -2, "n": 101}, {"n": 0}]


def solve(f0=0, f1=1, n=2547):
    g = Fraction(n + 1, 2) + (-1) ** n * Fraction(n - 1, 2)
    return g + f0 + (f1 - f0 - 1) * n


def check(f0=0, f1=1, n=2547):
    a, b = f0, f1
    if n == 0:
        return a
    for k in range(2, n + 1):
        a, b = b, 2 * b - a + (-1) ** k * (2 * k - 4)
    return b
