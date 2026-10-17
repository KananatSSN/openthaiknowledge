"""ข้อ 7 — a⁵/(bc²) + b⁵/(ca²) + c⁵/(ab²) ≥ a² + b² + c²  (พิสูจน์)

Weighted AM–GM: a⁵/(bc²) + b²/2 + c² ≥ (5/2)a²; summing cyclically gives the
claim, and Σa² ≥ (Σa)²/3. The solver returns the minimum of the left side when
a + b + c = S: S²/3 (S = 3: 3).

``check`` minimises the left side numerically on a + b + c = S.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"total": 3}
ANSWER = 3
TOL = 1e-7
VARIANTS = [{"total": 1}, {"total": 6}, {"total": 10}]


def solve(total=3):
    return Fraction(total * total, 3)


def check(total=3):
    def value(a, b):
        c = total - a - b
        if min(a, b, c) <= 0:
            return float("inf")
        return a**5 / (b * c * c) + b**5 / (c * a * a) + c**5 / (a * b * b)

    v, step = [total * 0.2, total * 0.5], total * 0.05
    best = value(*v)
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
