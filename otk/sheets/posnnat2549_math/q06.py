"""ข้อ 6 — f(cos(x + y)) = cos x f(cos y) + 2f(sin x)f(sin y), f(1) < 0, หา f(2006/2549)

x = y = 0 gives f(0) = 0; y = 0 gives f(cos x) = c·cos x with c = f(1);
x = y = π/2 gives −c = kc², so c = −1/k and f(t) = −t/k: −1003/2549.

``check`` finds the negative root of kc² + c = 0 by bisection and also
verifies the functional equation at sample points before evaluating.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"k": 2, "t": Fraction(2006, 2549)}
ANSWER = Fraction(-1003, 2549)
TOL = 1e-9
VARIANTS = [{"k": 4, "t": Fraction(-259, 2336)}, {"k": 3}, {"k": 9, "t": Fraction(1, 2)}]


def solve(k=2, t=Fraction(2006, 2549)):
    return -t / k


def check(k=2, t=Fraction(2006, 2549)):
    lo, hi = -10.0, -1e-9
    for _ in range(200):
        mid = (lo + hi) / 2
        if k * mid * mid + mid > 0:
            lo = mid
        else:
            hi = mid
    c = (lo + hi) / 2
    for x, y in ((0.3, 1.1), (-2.0, 0.7), (5.0, -4.0)):
        lhs = c * math.cos(x + y)
        rhs = math.cos(x) * c * math.cos(y) + k * c * math.sin(x) * c * math.sin(y)
        assert math.isclose(lhs, rhs, abs_tol=1e-9)
    return c * float(t)
