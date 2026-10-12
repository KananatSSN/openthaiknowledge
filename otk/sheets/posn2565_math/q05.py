"""ข้อ 5 — ค่าของ P(4) − P(0)

ให้ P(x) เป็นพหุนามดีกรีสองซึ่งสอดคล้องกับสมการ  P(x²) + 4x = P(x) + 4x⁴
แล้ว P(4) − P(0) มีค่าเท่ากับเท่าใด

Write P(x) = αx² + βx + γ. Then P(x²) = αx⁴ + βx² + γ, and matching the two
sides coefficient by coefficient:

    x⁴ :  α = k          (k = 4 on the sheet)
    x² :  β = α
    x¹ :  k = β

so all three agree on α = β = k, γ is free, and it cancels in the difference:

    P(m) - P(0) = k(m² + m)

which is 4(16 + 4) = **80** for k = 4 and m = 4. The constant term never being
determined is the point of asking for a *difference*.

``check`` never matches coefficients: it solves for α, β from the equation
evaluated at particular x, then verifies the resulting polynomial satisfies it at
several more.
"""

from __future__ import annotations

from fractions import Fraction

#: P(x²) + k·x = P(x) + k·x⁴, and the point m at which P is compared with P(0).
PARAMS = {"k": 4, "m": 4}
ANSWER = 80
VARIANTS = [
    {"k": 4, "m": 7},
    {"k": 1, "m": 4},
    {"k": 9, "m": 2},
    {"k": 6, "m": 10},
    {"k": -3, "m": 5},
    {"k": 0, "m": 4},          # P is constant: the difference vanishes
]


def solve(k=4, m=4):
    """P(m) - P(0) = k(m² + m)."""
    return Fraction(k) * (m * m + m)


def check(k=4, m=4):
    """Independent: fit a quadratic to the functional equation, then test it.

    Two sample points give two linear equations for α and β (γ cancels out of the
    equation entirely, which is itself worth seeing), and the fitted polynomial is
    verified at five more values of x before its difference is reported.
    """
    # P(x²) + kx - P(x) - kx⁴ = α(x⁴ - x²) + β(x² - x) + kx - kx⁴ = 0.
    # At x = 2: 12α + 2β + 2k - 16k = 0;  at x = 3: 72α + 6β + 3k - 81k = 0.
    det = 12 * 6 - 2 * 72
    if det == 0:                                     # pragma: no cover
        return None
    r2, r3 = Fraction(14 * k), Fraction(78 * k)
    alpha = Fraction(r2 * 6 - 2 * r3, det)
    beta = Fraction(12 * r3 - r2 * 72, det)

    gamma = Fraction(37, 5)                          # anything: it must cancel
    def poly(x):
        return alpha * x * x + beta * x + gamma

    for x in (Fraction(-4), Fraction(-1), Fraction(1, 2), Fraction(5),
              Fraction(11, 3)):
        assert poly(x * x) + k * x == poly(x) + k * x ** 4, x
    return poly(m) - poly(0)
