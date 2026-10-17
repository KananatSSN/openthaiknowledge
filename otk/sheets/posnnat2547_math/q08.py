"""ข้อ 8 — f(x + f(y)) = 2x + 4y + 2547, หา f(0)

Put x = t − f(y): f(t) = αt + (βy + γ − αf(y)), so f is affine with slope α;
then α·αy matches βy (β = α²) and the constants give (α + 1)c = γ:
f(0) = γ/(α + 1) = 849.

``check`` takes the affine form f(t) = αt + c, fixes c from x = y = 0
(f(f(0)) = γ), and then tests the identity exactly at a spread of rational
points before returning f(0).
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"alpha": 2, "beta": 4, "gamma": 2547}
ANSWER = 849
VARIANTS = [{"alpha": 3, "beta": 9, "gamma": 2431}, {"alpha": 5, "beta": 25, "gamma": 7}, {"alpha": 4, "beta": 16, "gamma": 100}]


def solve(alpha=2, beta=4, gamma=2547):
    return Fraction(gamma, alpha + 1)


def check(alpha=2, beta=4, gamma=2547):
    # f(f(0)) = γ with f(t) = αt + c: α·c + c = γ
    c = Fraction(gamma, alpha + 1)

    def f(t):
        return alpha * t + c

    for x in (Fraction(0), Fraction(3, 7), Fraction(-5, 2)):
        for y in (Fraction(1), Fraction(-2, 3), Fraction(11)):
            assert f(x + f(y)) == alpha * x + beta * y + gamma
    return f(0)
