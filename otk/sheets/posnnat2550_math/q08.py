"""ข้อ 8 — Σ xₖ/(xₖ − 1) บนรากของ x⁸⁴ + 7x − 6

x/(x − 1) = 1 + 1/(x − 1) and Σ 1/(1 − xₖ) = P′(1)/P(1), so the sum is
n − (n + a)/(1 + a − b) = 84 − 91/2 = 77/2.

``check`` maps the roots by y = 1/(1 − x): yⁿ·P(1 − 1/y) is a polynomial whose
roots are the yₖ, and Σyₖ is minus its second coefficient over its first.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb

PARAMS = {"n": 84, "a": 7, "b": 6}
ANSWER = Fraction(77, 2)
VARIANTS = [{"n": 20, "a": 10, "b": 2}, {"n": 3, "a": 1, "b": 5}, {"n": 50, "a": 12, "b": 1}]


def solve(n=84, a=7, b=6):
    return n - Fraction(n + a, 1 + a - b)


def check(n=84, a=7, b=6):
    # P(x) = xⁿ + a·x − b with x = 1 − 1/y = (y − 1)/y:
    # yⁿ P = (y − 1)ⁿ + a(y − 1)y^(n−1) − b·yⁿ
    coeffs = [Fraction(0)] * (n + 1)  # coeffs[j] for y^j
    for j in range(n + 1):
        coeffs[j] += comb(n, j) * (-1) ** (n - j)
    coeffs[n] += a
    coeffs[n - 1] -= a
    coeffs[n] -= b
    sum_y = -coeffs[n - 1] / coeffs[n]
    return n - sum_y  # Σ x/(x − 1) = Σ(1 − y) = n − Σy
