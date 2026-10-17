"""ข้อ 3 — ด้านที่สั้นที่สุดเมื่อเส้นมัธยฐานยาว 3, 4, 5

Apollonius inverted: a² = (4/9)(2m_b² + 2m_c² − m_a²); the longest median is
opposite the shortest side: a² = (4/9)(18 + 32 − 25) = 100/9, so 10/3.

``check`` solves the linear system m_x² = (2y² + 2z² − x²)/4 for the squared
sides by Gaussian elimination in fractions and takes the smallest root.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"medians": (3, 4, 5)}
ANSWER = Fraction(10, 3)
VARIANTS = [{"medians": (9, 14, 15)}, {"medians": (5, 5, 5)}, {"medians": (2, 3, 4)}, {"medians": (6, 7, 11)}]


def solve(medians=(3, 4, 5)):
    m1, m2, m3 = sorted(medians)
    return math.sqrt(Fraction(4, 9) * (2 * m1 * m1 + 2 * m2 * m2 - m3 * m3))


def check(medians=(3, 4, 5)):
    rows = [[Fraction(-1, 4), Fraction(1, 2), Fraction(1, 2)],
            [Fraction(1, 2), Fraction(-1, 4), Fraction(1, 2)],
            [Fraction(1, 2), Fraction(1, 2), Fraction(-1, 4)]]
    rhs = [Fraction(m * m) for m in medians]
    n = 3
    for col in range(n):
        piv = next(r for r in range(col, n) if rows[r][col] != 0)
        rows[col], rows[piv] = rows[piv], rows[col]
        rhs[col], rhs[piv] = rhs[piv], rhs[col]
        for r in range(n):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col])]
                rhs[r] -= factor * rhs[col]
    squares = [rhs[i] / rows[i][i] for i in range(n)]
    return math.sqrt(min(squares))
