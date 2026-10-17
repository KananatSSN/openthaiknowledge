"""ข้อ 15 — f(x + 2y) + 2f(y − 2x) = 3x − 4y + 6, หา f(2548)

With f(t) = at + b the left side is a(1 − 2k)x + a(2 + k)y + (1 + k)b; matching
gives a = −1, b = 2, so f(2548) = −2546.

``check`` does not assume a form: x = y = 0 gives (1 + k)f(0) = c₀, and y = 2x
makes the second argument 0, so f(5x) = (c_x + 2c_y)x + c₀ − k f(0).
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"cx": 3, "cy": -4, "c0": 6, "k": 2, "n": 2548}
ANSWER = -2546
VARIANTS = [{"cx": -15, "cy": 15, "c0": 9, "k": 3, "n": 1094}, {"cx": 6, "cy": -8, "c0": 27, "n": 1}, {"cx": -14, "cy": 12, "c0": -10, "k": 4, "n": 300}]


def solve(cx=3, cy=-4, c0=6, k=2, n=2548):
    return Fraction(cx, 1 - 2 * k) * n + Fraction(c0, 1 + k)


def check(cx=3, cy=-4, c0=6, k=2, n=2548):
    f0 = Fraction(c0, 1 + k)
    x = Fraction(n, 5)
    return (cx + 2 * cy) * x + c0 - k * f0
