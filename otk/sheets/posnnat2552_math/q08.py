"""ข้อ 8 — Σ 2a(2a − s)/(b + c) ≥ s  (พิสูจน์)

With x = a/s ∈ (0, 1) each term is s·g(x), g(x) = 2x(2x − 1)/(2 − x); the
tangent line at x = 2/3 gives g(x) ≥ 1/3 + (11/4)(x − 2/3) on (0, 1), and the
x's add to 2, so the sum is at least s, with equality for the equilateral
triangle. The solver returns the minimum over triangles of perimeter P: P/2.

``check`` minimises the sum numerically over triangle shapes.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"perimeter": 6}
ANSWER = 3
TOL = 1e-7
VARIANTS = [{"perimeter": 2}, {"perimeter": 15}, {"perimeter": 40}]


def solve(perimeter=6):
    return Fraction(perimeter, 2)


def check(perimeter=6):
    s = perimeter / 2

    def value(a, b):
        c = perimeter - a - b
        if not (a < b + c and b < a + c and c < a + b):
            return float("inf")
        return sum(2 * x * (2 * x - s) / (y + z) for x, y, z in ((a, b, c), (b, a, c), (c, a, b)))

    v = [perimeter * 0.3, perimeter * 0.35]
    best, step = value(*v), perimeter * 0.05
    while step > 1e-12:
        improved = False
        for i in range(2):
            for sign in (1, -1):
                trial = list(v)
                trial[i] += sign * step
                val = value(*trial)
                if val < best:
                    v, best, improved = trial, val, True
        if not improved:
            step /= 2
    return best
