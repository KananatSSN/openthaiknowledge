"""วันที่สอง ข้อ 2 — f : ℚ → ℚ, f(x + y) = f(x) + f(y) + 2547, f(2004) = 2547, หา f(2547)

g = f + c is additive on ℚ, so g(x) = kx with k = (b + c)/a, and
f(t) = (b + c)t/a − c = 1311705/334.

``check`` works on the integers only: y = 1 gives f(n + 1) = f(n) + f(1) + c,
so f(n) = n·f(1) + (n − 1)c; f(a) = b fixes f(1), and f(t) follows.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"c": 2547, "a": 2004, "b": 2547, "t": 2547}
ANSWER = Fraction(1311705, 334)
VARIANTS = [{"c": 10, "a": 3, "b": 4, "t": 17}, {"c": 560, "a": 2341, "b": 268, "t": 1054}, {"t": 1}, {"b": -2547}]


def solve(c=2547, a=2004, b=2547, t=2547):
    return Fraction((b + c) * t, a) - c


def check(c=2547, a=2004, b=2547, t=2547):
    f1 = Fraction(b - (a - 1) * c, a)
    return t * f1 + (t - 1) * c
