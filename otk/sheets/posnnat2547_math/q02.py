"""ข้อ 2 — a⁴ + b⁴ จาก a⁶ − 3a²b⁴ = 3 และ b⁶ − 3a⁴b² = 3√2

With z = a² + ib², z³ = (a⁶ − 3a²b⁴) + i(3a⁴b² − b⁶), so |z|⁶ = p² + q² and
a⁴ + b⁴ = |z|² = (p² + q²)^(1/3) = 27^(1/3) = 3.

The paper's system as printed has no real solution: with x = a², y = b² ≥ 0 the
second equation forces y² > 3x², and then x³ − 3xy² ≤ 0 ≠ 3. The answer 3 is the
formal value; the solver works with q² so the sign of q does not enter.

So ANSWER is verified for the corrected system (3a⁴b² − b⁶ = +q), not the
printed one. ``check`` builds an actual solution of it: the principal cube root
z of p + iq lies in the first quadrant, a = √Re z, b = √Im z; it confirms that
this a, b satisfies both corrected equations, then measures a⁴ + b⁴.
test_math_olympiad_posn_national_2547.py proves the printed system has no real
solution.
"""

from __future__ import annotations

import math

PARAMS = {"p": 3, "q2": 18}
ANSWER = 3.0
VARIANTS = [{"p": 2, "q2": 121}, {"p": 52, "q2": 2209}, {"p": 1, "q2": 0}, {"p": 10, "q2": 300}]


def solve(p=3, q2=18):
    return (p * p + q2) ** (1 / 3)


def check(p=3, q2=18):
    z = complex(p, math.sqrt(q2)) ** (1 / 3)
    a, b = math.sqrt(z.real), math.sqrt(max(z.imag, 0.0))
    assert math.isclose(a**6 - 3 * a**2 * b**4, p, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(3 * a**4 * b**2 - b**6, math.sqrt(q2), rel_tol=1e-9, abs_tol=1e-9)
    return a**4 + b**4
