"""ข้อ 9 — f(x² + x + 3) + 2f(x² − 3x + 5) = 6x² − 10x + 17, หา f(85)

x ↦ 1 − x swaps u = x² + x + 3 and v = x² − 3x + 5; solving the 2 × 2 system
gives f(u) = 2u − 3 and f(85) = 167. The solver takes f(t) = αt + β with the
right side built from it.

``check`` solves the system f(u) + k f(v) = R(x), f(v) + k f(u) = R(1 − x) at two
values of x, gets f at two points, and extends the line to n.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"alpha": 2, "beta": -3, "k": 2, "n": 85}
ANSWER = 167
VARIANTS = [{"alpha": 1, "beta": 4, "k": 3, "n": 52}, {"alpha": 4, "beta": 0, "k": 4, "n": 100}, {"beta": 6}]


def solve(alpha=2, beta=-3, k=2, n=85):
    return alpha * n + beta


def check(alpha=2, beta=-3, k=2, n=85):
    def rhs(x):
        return alpha * (x * x + x + 3) + beta + k * (alpha * (x * x - 3 * x + 5) + beta)

    points = []
    for x in (Fraction(2), Fraction(5)):
        r1, r2 = rhs(x), rhs(1 - x)
        fu = (r1 - k * r2) / (1 - k * k)
        points.append((x * x + x + 3, fu))
    (u1, f1), (u2, f2) = points
    return f1 + (f2 - f1) / (u2 - u1) * (n - u1)
