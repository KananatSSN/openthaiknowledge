"""ข้อ 16 — ผลบวกรากของ (2 − x)²⁰⁰⁵ + x²⁰⁰⁵ = 0

For odd n the xⁿ terms cancel, leaving degree n − 1; the roots pair up as x and
c − x (x = c/2 is not a root), so the sum is (n − 1)c/2 = 2004. (Even n keeps
degree n and the sum nc/2.)

``check`` reads the two leading coefficients of the expanded polynomial.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb

PARAMS = {"c": 2, "n": 2005}
ANSWER = 2004
VARIANTS = [{"c": 3, "n": 7}, {"c": 1, "n": 10}, {"c": 7, "n": 2336}, {"c": 5, "n": 15}]


def solve(c=2, n=2005):
    return Fraction((n - 1) * c, 2) if n % 2 else Fraction(n * c, 2)


def check(c=2, n=2005):
    coeffs = [0] * (n + 1)  # coeffs[j] for x^j
    for j in range(n + 1):
        coeffs[j] += comb(n, j) * c ** (n - j) * (-1) ** j
    coeffs[n] += 1
    degree = max(j for j in range(n + 1) if coeffs[j])
    return Fraction(-coeffs[degree - 1], coeffs[degree])
