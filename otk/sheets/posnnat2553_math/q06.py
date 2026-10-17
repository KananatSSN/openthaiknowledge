"""ข้อ 6 — f(3x + y) + f(3x − y) = f(x + y) + f(x − y) + 16f(x) ⇒ f คู่  (พิสูจน์)

x = y = 0 gives f(0) = 0, and y = x gives f(4x) = 16f(x), so f(4ᵏx) = 16ᵏf(x).
The solver returns f(4ᵏx) from f(x) (f(x) = 3, k = 2: 768).

``check`` verifies that f(t) = ct² satisfies the equation and evaluates
f(4ᵏx) for c chosen so that f(x) matches.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"given": 3, "steps": 2}
ANSWER = 768
VARIANTS = [{"given": 1, "steps": 5}, {"given": -2, "steps": 3}, {"steps": 0}]


def solve(given=3, steps=2):
    return given * 16**steps


def check(given=3, steps=2):
    x = Fraction(5, 7)
    c = Fraction(given) / (x * x)

    def f(t):
        return c * t * t

    for u, v in ((Fraction(1), Fraction(2)), (Fraction(-3, 2), Fraction(1, 3))):
        assert f(3 * u + v) + f(3 * u - v) == f(u + v) + f(u - v) + 16 * f(u)
    return f(4**steps * x)
