"""ข้อ 7 — x⁵ − ax⁴ + bx³ − cx² + dx = 1 มีรากจริงทั้งหมด ⇒ 1/a + 1/b + 1/c + 1/d ≤ 3/5  (พิสูจน์)

The signs alternate, so all roots are positive, with product 1; each e_k is a
sum of C(n, k) terms whose product is 1, so e_k ≥ C(n, k) by AM–GM. The solver
returns Σ 1/C(n, k) over k = 1, …, n − 1 (n = 5: 3/5), the value at the
equality case.

``check`` expands (x − 1)ⁿ (all roots 1, the equality case) and adds the
reciprocals of its elementary symmetric functions.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"n": 5}
ANSWER = Fraction(3, 5)
VARIANTS = [{"n": 2}, {"n": 3}, {"n": 8}]


def solve(n=5):
    from math import comb

    return sum((Fraction(1, comb(n, k)) for k in range(1, n)), Fraction(0))


def check(n=5):
    coeffs = [1]
    for _ in range(n):  # multiply by (x − 1)
        coeffs = [a - b for a, b in zip(coeffs + [0], [0] + coeffs)]
    # coeffs[k] = (−1)^k e_k
    return sum((Fraction(1, abs(coeffs[k])) for k in range(1, n)), Fraction(0))
