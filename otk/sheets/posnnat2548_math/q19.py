"""ข้อ 19 — P โมนิกดีกรี 4 ที่ x − k หาร P(x) เหลือเศษ k (k = 1, 2, 3), หา P(4) + P(0)

P(x) = αx + β + (x − 1)⋯(x − (d − 1))(x − r). At d the product is
(d − 1)!(d − r) and at 0 it is (−1)^d (d − 1)! r; for even d the r-terms
cancel: P(d) + P(0) = αd + 2β + d! = 28.

``check`` builds P with an arbitrary fourth root (r = 7/3) and evaluates it.
"""

from __future__ import annotations

from fractions import Fraction
from math import factorial, prod

PARAMS = {"d": 4, "alpha": 1, "beta": 0}
ANSWER = 28
VARIANTS = [{"d": 2}, {"d": 6, "alpha": 4, "beta": -7}, {"d": 8, "alpha": -2, "beta": 3}, {"alpha": 0, "beta": 5}]


def solve(d=4, alpha=1, beta=0):
    return alpha * d + 2 * beta + factorial(d)


def check(d=4, alpha=1, beta=0):
    r = Fraction(7, 3)

    def p(x):
        return alpha * x + beta + prod(x - k for k in range(1, d)) * (x - r)

    assert all(p(k) == alpha * k + beta for k in range(1, d))
    return p(d) + p(0)
