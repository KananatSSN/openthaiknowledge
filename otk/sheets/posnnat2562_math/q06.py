"""ข้อ 6 — x f(y) + y f(x) ≤ xy ทุก x, y ∈ ℝ

For the family x·f(y) + y·f(x) ≤ c·xy, h = f − cx/2 satisfies
x·h(y) + y·h(x) ≤ 0. x = y gives h ≤ 0 on the positives and h ≥ 0 on the
negatives; a positive x with a negative y makes both terms nonnegative, so h
vanishes, and x = 0 gives h(0) = 0. So f(x) = cx/2 (the source, c = 1: x/2).
The solver returns f(n).

``check`` tries every f(x) = px + q on a grid of rationals against the
inequality at many points of both signs and evaluates the one survivor at n.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"c": 1, "n": 3}
ANSWER = Fraction(3, 2)
VARIANTS = [{"c": 2, "n": 5}, {"c": 3, "n": 4}, {"c": -2, "n": 7}]


def solve(c=1, n=3):
    return Fraction(c * n, 2)


def check(c=1, n=3):
    pts = [Fraction(v, 2) for v in (-9, -4, -1, 0, 1, 3, 8)]
    found = []
    for p in [Fraction(v, 2) for v in range(-8, 9)]:
        for q in [Fraction(v, 2) for v in range(-4, 5)]:
            if all(x * (p * y + q) + y * (p * x + q) <= c * x * y for x in pts for y in pts):
                found.append(p * n + q)
    assert len(found) == 1
    return found[0]
