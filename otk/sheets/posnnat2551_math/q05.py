"""ข้อ 5 — P ดีกรี 2008 ที่ P(α) = 0 ⇒ P(α + 1) = 1 ต้องมีรากซ้ำ  (พิสูจน์)

If the roots α₁, …, α_n were distinct, P(x + 1) − P(x) − 1 (degree < n) would
vanish at n points, so P(x + 1) − P(x) = 1 and P would be linear. The solver
computes the telescoped value P(n) = c + Σ_{k<n}(ak + b) for a polynomial with
P(x + 1) − P(x) = ax + b and P(0) = c; the source's case a = 0, b = 1, c = 0
gives P(2008) = 2008.

``check`` iterates P(k + 1) = P(k) + ak + b.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"a": 0, "b": 1, "c": 0, "n": 2008}
ANSWER = 2008
VARIANTS = [{"a": 2, "b": -1, "c": 5, "n": 30}, {"a": 3, "b": 4, "c": -2, "n": 11}, {"c": 7}]


def solve(a=0, b=1, c=0, n=2008):
    return c + Fraction(a * n * (n - 1), 2) + b * n


def check(a=0, b=1, c=0, n=2008):
    value = c
    for k in range(n):
        value += a * k + b
    return value
