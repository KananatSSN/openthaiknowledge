"""ข้อ 6 — |f(x + y) − f(x) − f(y)| < 1 ⇒ |f(x/2008) − f(x)/2008| < 1  (พิสูจน์)

Induction gives |f(nx) − n·f(x)| < n − 1, so with x → x/n,
|f(x/n) − f(x)/n| < (n − 1)/n < 1. The bound n − 1 is sharp: f = c⌊x⌋ with
c → 1. The solver returns n − 1 (n = 2008: 2007).

``check`` evaluates sup |f(nx) − n f(x)| for f(x) = c⌊x⌋ with c = 1 − 10⁻¹²
(x just below 1) and confirms that f satisfies the hypothesis.
"""

from __future__ import annotations

import math

PARAMS = {"n": 2008}
ANSWER = 2007
TOL = 1e-6
VARIANTS = [{"n": 2}, {"n": 10}, {"n": 500}]


def solve(n=2008):
    return n - 1


def check(n=2008):
    c = 1 - 1e-12

    def f(x):
        return c * math.floor(x)

    for x, y in ((0.6, 0.7), (-0.2, 0.9), (2.5, 3.5)):
        assert abs(f(x + y) - f(x) - f(y)) < 1
    best = 0.0
    for x in (1 - 1 / (2 * n), 1 - 1 / (3 * n), 0.999999):
        best = max(best, abs(f(n * x) - n * f(x)))
    return best
