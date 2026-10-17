"""ข้อ 4 — พหุนามโมนิกที่ราก a, b ให้ a + b + ab เป็นรากด้วย

For the family a + b + k·ab: (1 + ka)(1 + kb) = 1 + k(a + b + kab), so
u = 1 + ka turns the rule into closure under products (a = b included). A
finite set of distinct reals closed under products lies in {−1, 0, 1}: {0},
{1}, {0, 1}, {−1, 1}, {−1, 0, 1}. The source (k = 1) gives the roots {−1},
{0}, {−1, 0}, {−2, 0}, {−2, −1, 0}: x + 1, x, x(x + 1), x(x + 2),
x(x + 1)(x + 2). The answer is the sorted tuple of root sets.

``check`` searches every subset of up to four values j/|k| (|j| ≤ 3|k|) for
closure under the rule directly.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

PARAMS = {"k": 1}
ANSWER = ((Fraction(-2, 1), Fraction(-1, 1), Fraction(0, 1)), (Fraction(-2, 1), Fraction(0, 1)), (Fraction(-1, 1),), (Fraction(-1, 1), Fraction(0, 1)), (Fraction(0, 1),))
VARIANTS = [{"k": 2}, {"k": 3}, {"k": -1}]


def solve(k=1):
    product_closed = ((0,), (1,), (0, 1), (-1, 1), (-1, 0, 1))
    return tuple(sorted(tuple(sorted(Fraction(u - 1, k) for u in s)) for s in product_closed))


def check(k=1):
    n = abs(k)
    grid = [Fraction(j, n) for j in range(-3 * n, 3 * n + 1)]
    found = []
    for size in range(1, 5):
        for roots in combinations(grid, size):
            s = set(roots)
            if all(a + b + k * a * b in s for a in roots for b in roots):
                found.append(tuple(sorted(roots)))
    return tuple(sorted(found))
