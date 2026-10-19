"""ข้อ 9 — |S| ≤ 2  (พิสูจน์)

Write a = gu, b = gv with gcd(u, v) = 1: (b − a) | lcm = guv forces v − u = 1,
and the quotient u(u + 1) must be a or b. If it is a, g = u + 1 and
S = {u(u + 1), (u + 1)²}; if it is b, g = u and S = {u², u(u + 1)}. A third
member breaks one of these. The solver returns the largest member given the
smallest (12 = 3·4: 16).

``check`` tries every b up to ten times the minimum against the condition
directly, asserts exactly one works, and confirms no set of three numbers up to
60 satisfies the condition.
"""

from __future__ import annotations

from itertools import combinations
from math import isqrt, lcm

PARAMS = {"minimum": 12}
ANSWER = 16
VARIANTS = [{"minimum": 9}, {"minimum": 30}, {"minimum": 16}]


def solve(minimum=12):
    n = isqrt(minimum)
    if n * n == minimum:
        return n * (n + 1)
    assert n * (n + 1) == minimum
    return (n + 1) ** 2


def _good(a, b):
    q, r = divmod(lcm(a, b), b - a)
    return r == 0 and q


def _closed(s):
    return all((q := _good(a, b)) and q in s for a, b in combinations(sorted(s), 2))


def check(minimum=12):
    hits = [b for b in range(minimum + 1, 10 * minimum + 1) if _closed({minimum, b})]
    assert len(hits) == 1
    assert not any(_closed(set(t)) for t in combinations(range(1, 61), 3))
    return hits[0]
