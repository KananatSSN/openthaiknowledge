"""ข้อ 5 — Σ (4a − 1)/(2b + 1)² ≥ 1 เมื่อ abc = 1  (พิสูจน์)

For the family abc = s³, putting a = s·a′ (and so on) divides every term by s,
leaving the source inequality with equality at a = b = c. The solver returns
the minimum 1/s (s = 1: 1).

``check`` evaluates the sum on a log-spaced grid of (a, b) with c = s³/(ab),
asserts nothing falls below 1/s, and returns the smallest value found (the grid
contains a = b = c = s).
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"s": 1}
ANSWER = 1
VARIANTS = [{"s": 2}, {"s": 3}, {"s": 5}]
TOL = 1e-9


def solve(s=1):
    return Fraction(1, s)


def check(s=1):
    grid = [s * 2 ** (j / 4) for j in range(-16, 17)]
    best = None
    for a in grid:
        for b in grid:
            c = s**3 / (a * b)
            total = sum((4 * x - s) / (2 * y + s) ** 2 for x, y in ((a, b), (b, c), (c, a)))
            assert total >= 1 / s - 1e-12
            best = total if best is None else min(best, total)
    return best
