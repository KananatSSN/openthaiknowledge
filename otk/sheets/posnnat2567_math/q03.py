"""ข้อ 3 — x²f(x f(y))f(x)f(y) = c

The proof shows x·f(x) is constant, f(x) = k/x; substituting gives
x²·(k/(x·k/y))·(k/x)·(k/y) = k² = c, so f(x) = √c/x. The solver returns f(t)
for a square c (c = 4, t = 3: 2/3).

``check`` tries every k·xᵉ with k a fraction of denominator ≤ 3 up to 6 and
e ∈ {−2, …, 2} against the equation at many points and evaluates the survivor at t.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

PARAMS = {"c": 4, "t": 3}
ANSWER = Fraction(2, 3)
VARIANTS = [{"c": 9, "t": 2}, {"c": 1, "t": 5}, {"c": 16, "t": 7}]


def solve(c=4, t=3):
    root = isqrt(c)
    assert root * root == c
    return Fraction(root, t)


def check(c=4, t=3):
    pts = [Fraction(v, 2) for v in (1, 2, 3, 5, 8)]
    found = []
    for k in sorted({Fraction(n, d) for d in (1, 2, 3) for n in range(1, 6 * d + 1)}):
        for e in range(-2, 3):
            def f(x, k=k, e=e):
                return k * x**e

            if all(x * x * f(x * f(y)) * f(x) * f(y) == c for x in pts for y in pts):
                found.append(f(Fraction(t)))
    assert len(found) == 1
    return found[0]
