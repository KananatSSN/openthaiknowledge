"""ข้อ 6 — Σ a⁵/(xc + yb) ≥ 9/((x + y)(a² + b² + c²)) เมื่อ abc = 1  (พิสูจน์)

For abc = P: F = (x + y)(a² + b² + c²)·Σ a⁵/(xc + yb) scales as P², and with
abc = 1 Cauchy–Schwarz and AM–GM give F ≥ 9, equal at a = b = c (any x, y). So
the minimum is 9P². The solver returns it (P = 1: 9).

``check`` evaluates F on a grid of (a, b) with c = P/(ab) (containing
a = b = c) and several ratios y/x, asserts nothing falls below 9P², and returns
the least value.
"""

from __future__ import annotations

PARAMS = {"product": 1}
ANSWER = 9
VARIANTS = [{"product": 2}, {"product": 5}, {"product": 12}]
TOL = 1e-9


def solve(product=1):
    return 9 * product * product


def check(product=1):
    root = product ** (1 / 3)
    best = None
    for i in range(-12, 13):
        for j in range(-12, 13):
            a, b = root * 2 ** (i / 6), root * 2 ** (j / 6)
            c = product / (a * b)
            for x, y in ((1, 1), (1, 3), (5, 2), (1, 10)):
                value = (x + y) * (a * a + b * b + c * c) * (
                    a**5 / (x * c + y * b) + b**5 / (x * a + y * c) + c**5 / (x * b + y * a))
                assert value >= 9 * product * product * (1 - 1e-12)
                best = value if best is None else min(best, value)
    return best
