"""ข้อ 7 — x ที่ทำให้ 2x² + 3y² + 4z² ต่ำสุด เมื่อ x + y + z = 1

Cauchy–Schwarz: the minimum has wᵢxᵢ constant, so xᵢ = s(1/wᵢ)/Σ(1/wⱼ):
x = (1/2)/(13/12) = 6/13.

``check`` solves the Lagrange system 2wᵢxᵢ = λ, Σxᵢ = s by Gaussian
elimination in fractions.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"weights": (2, 3, 4), "s": 1, "which": 0}
ANSWER = Fraction(6, 13)
VARIANTS = [{"which": 2}, {"weights": (3, 2, 9), "which": 1}, {"weights": (1, 5, 7), "s": 4}, {"s": 6, "which": 1}]


def solve(weights=(2, 3, 4), s=1, which=0):
    inv = [Fraction(1, w) for w in weights]
    return s * inv[which] / sum(inv)


def check(weights=(2, 3, 4), s=1, which=0):
    # unknowns x0, x1, x2, λ
    rows = [[Fraction(0)] * 4 for _ in range(4)]
    rhs = [Fraction(0)] * 4
    for i, w in enumerate(weights):
        rows[i][i], rows[i][3] = Fraction(2 * w), Fraction(-1)
    rows[3] = [Fraction(1), Fraction(1), Fraction(1), Fraction(0)]
    rhs[3] = Fraction(s)
    for col in range(4):
        piv = next(r for r in range(col, 4) if rows[r][col] != 0)
        rows[col], rows[piv] = rows[piv], rows[col]
        rhs[col], rhs[piv] = rhs[piv], rhs[col]
        for r in range(4):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col])]
                rhs[r] -= factor * rhs[col]
    return rhs[which] / rows[which][which]
