"""ข้อ 14 — f(m + n) = f(m) + f(n) + 2mn − 2548, f(2548) = −2548, หา f(2)

h(n) = f(n) − n² − C is additive on ℕ, so f(n) = n² + cn + C; f(C) = D fixes
c = (D − C² − C)/C = −2550, and f(2) = −2548.

``check`` uses n = 1 only: f(n + 1) = f(n) + f(1) + 2n − C, so f(C) is linear in
the unknown f(1); it solves for f(1) and iterates up to t.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"shift": 2548, "anchor": -2548, "t": 2}
ANSWER = -2548
VARIANTS = [{"shift": 555, "anchor": 30525, "t": 6}, {"shift": 17, "anchor": 255, "t": 9}, {"t": 2548}, {"shift": 5, "anchor": 0, "t": 3}]


def solve(shift=2548, anchor=-2548, t=2):
    c = Fraction(anchor - shift * shift - shift, shift)
    return t * t + c * t + shift


def check(shift=2548, anchor=-2548, t=2):
    def value(n, f1):
        f = f1
        for k in range(1, n):
            f = f + f1 + 2 * k - shift
        return f

    base, slope = value(shift, 0), value(shift, 1) - value(shift, 0)
    f1 = Fraction(anchor - base, slope)
    return value(t, f1)
