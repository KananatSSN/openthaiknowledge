"""ข้อ 5 — f(f(x) + x f(y)) = 3f(x) + 4xy

For the family f(f(x) + x f(y)) = (a + 1)f(x) + a²xy and f = px + q: the xy terms
give p² = a², the constants q(p − a) = 0, and the x terms p² + pq = (a + 1)p;
for a ≥ 2 only p = a, q = 1 survives. The source (a = 2) gives f(x) = 2x + 1,
recorded as (2, 1).

``check`` tries every (p, q) on a grid of rationals and keeps those satisfying
the equation at a spread of points.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"a": 2}
ANSWER = (2, 1)
VARIANTS = [{"a": 3}, {"a": 4}, {"a": 6}]


def solve(a=2):
    return (a, 1)


def check(a=2):
    points = [(Fraction(x), Fraction(y)) for x, y in ((0, 0), (1, 2), (-3, 5), (2, -7), (4, 4))]
    found = []
    for p in [Fraction(v, 2) for v in range(-16, 17)]:
        for q in [Fraction(v, 2) for v in range(-8, 9)]:
            def f(t, p=p, q=q):
                return p * t + q

            if all(f(f(x) + x * f(y)) == (a + 1) * f(x) + a * a * x * y for x, y in points):
                found.append((p, q))
    assert len(found) == 1
    return found[0]
