"""ข้อ 5 — f(xy + 2x + 2y − 1) = f(x)f(y) + f(y) + x − 2

For the family f(xy + (c + 1)x + (c + 1)y + c² − d) = f(x)f(y) + f(y) + x − d and
f = px + q: the xy terms give p = p², and p = 0 leaves an x on one side, so
p = 1; then the x terms give q = c. The source (c = 1, d = 2) gives
f(x) = x + 1, recorded as (p, q) = (1, 1).

``check`` tries every (p, q) on a grid of small rationals and keeps those for
which both sides agree at a spread of points.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"c": 1, "d": 2}
ANSWER = (1, 1)
VARIANTS = [{"c": 3, "d": 5}, {"c": 2, "d": 1}, {"c": 5, "d": 6}]


def solve(c=1, d=2):
    return (1, c)


def check(c=1, d=2):
    points = [(Fraction(x), Fraction(y)) for x, y in ((0, 0), (1, 2), (-3, 5), (2, -7), (4, 4))]
    found = []
    for p in [Fraction(v, 2) for v in range(-6, 7)]:
        for q in [Fraction(v, 2) for v in range(-14, 15)]:
            def f(t, p=p, q=q):
                return p * t + q

            if all(f(x * y + (c + 1) * x + (c + 1) * y + c * c - d) == f(x) * f(y) + f(y) + x - d for x, y in points):
                found.append((p, q))
    assert len(found) == 1
    return found[0]
