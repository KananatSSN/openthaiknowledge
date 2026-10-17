"""ข้อ 7 — f : ℝ → ℤ ที่ (f(x))² + (f(y))² ≤ 2f(xy)

x = y = 0 and x = y = 1 give f(0), f(1) ∈ {0, 1}. If f(1) = 1, then (x, 1) gives
(f(x) − 1)² ≤ 0, so f ≡ 1. If f(1) = 0, then (x, 1/x) gives f(x)² + f(1/x)² ≤ 0,
so f(x) = 0 for every x ≠ 0, and f(0) is 0 or 1 (both pass). So f ≡ 0, f ≡ 1,
or f(0) = 1 and f = 0 elsewhere. The answer is the sorted tuple of
(f(0), f(1), f(x)) over the three.

``check`` tries every integer assignment in −3..3 to f at −1, 0, 1, x and 1/x and
keeps those satisfying the inequality for every pair whose product is among
those points.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

PARAMS = {"x": 2}
ANSWER = ((0, 0, 0), (1, 0, 0), (1, 1, 1))
VARIANTS = [{"x": -3}, {"x": Fraction(1, 2)}, {"x": 7}]


def solve(x=2):
    return tuple(sorted(((0, 0, 0), (1, 1, 1), (1, 0, 0))))


def check(x=2):
    points = [Fraction(-1), Fraction(0), Fraction(1), Fraction(x), 1 / Fraction(x)]
    survivors = []
    for values in product(range(-3, 4), repeat=5):
        f = dict(zip(points, values))
        if all(f[u] ** 2 + f[v] ** 2 <= 2 * f[u * v]
               for u in points for v in points if u * v in f):
            survivors.append((f[Fraction(0)], f[Fraction(1)], f[Fraction(x)]))
    return tuple(sorted(set(survivors)))
