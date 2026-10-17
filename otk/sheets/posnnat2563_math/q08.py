"""ข้อ 8 — Σ a⁶/(c² + 2b³) ≥ 1 เมื่อ a + b + c = 3  (พิสูจน์)

For the homogeneous family a + b + c = 3t with denominators c² + (2/t)b³,
putting a = tA (and so on) multiplies every term by t⁴, leaving the source
inequality (minimum 1 at A = B = C = 1). The solver returns t⁴.

``check`` evaluates the sum on a grid of the simplex a + b + c = 3t (which
contains a = b = c = t), asserts nothing falls below t⁴, and returns the least
value found.
"""

from __future__ import annotations

PARAMS = {"t": 1}
ANSWER = 1
VARIANTS = [{"t": 2}, {"t": 3}, {"t": 5}]
TOL = 1e-9


def solve(t=1):
    return t**4


def check(t=1):
    steps = 60
    best = None
    for i in range(1, steps * 3):
        for j in range(1, steps * 3 - i):
            a, b = t * i / steps, t * j / steps
            c = 3 * t - a - b
            if c <= 0:
                continue
            total = (a**6 / (c * c + 2 / t * b**3) + b**6 / (a * a + 2 / t * c**3)
                     + c**6 / (b * b + 2 / t * a**3))
            assert total >= t**4 * (1 - 1e-12)
            best = total if best is None else min(best, total)
    return best
