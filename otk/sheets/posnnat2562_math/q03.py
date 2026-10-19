"""ข้อ 3 — f(x + y f(x) + y²) = f(x) + 2y บน ℝ⁺

For the family f(x + y·f(x) + m²y²) = f(x) + 2m²y the solutions are
f(x) = √(4m²x + c) with c ≥ 0 (the source, m = 1: √(4x + c)), so
f(b)² − f(a)² = 4m²(b − a). The solver returns f(b) from f(a) = value
(m = 1, f(1) = 3: f(5) = 5).

``check`` takes c = value² − 4m²a, confirms c ≥ 0 and that √(4m²x + c)
satisfies the original equation at a spread of positive x, y, and evaluates it
at b.
"""

from __future__ import annotations

from math import isqrt, sqrt

PARAMS = {"m": 1, "a": 1, "value": 3, "b": 5}
ANSWER = 5
VARIANTS = [{"m": 1, "a": 2, "value": 3, "b": 6}, {"m": 1, "a": 3, "value": 4, "b": 8},
            {"m": 2, "a": 1, "value": 4, "b": 4}, {"m": 3, "a": 1, "value": 6, "b": 4}]
TOL = 1e-9


def solve(m=1, a=1, value=3, b=5):
    square = value * value + 4 * m * m * (b - a)
    root = isqrt(square)
    assert root * root == square
    return root


def check(m=1, a=1, value=3, b=5):
    c = value * value - 4 * m * m * a
    assert c >= 0

    def f(x):
        return sqrt(4 * m * m * x + c)

    for x in (0.1, 0.7, 2.0, 9.5):
        for y in (0.05, 0.3, 1.0, 4.2):
            assert abs(f(x + y * f(x) + m * m * y * y) - (f(x) + 2 * m * m * y)) < 1e-9
    return f(b)
