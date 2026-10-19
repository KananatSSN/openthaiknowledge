"""วันที่สอง ข้อ 3 — อสมการผลบวกรากที่ n  (พิสูจน์)

1/((2k − 1)2k) = 1/(2k − 1) − 1/(2k), so Σₖ 1/a₂ₖ₋₁ = Σₖ₌ₙ₊₁²ⁿ 1/k, which the
HM–AM inequality bounds below by 2n/(3n + 1); AM–GM then gives the source's
inequality. The solver returns Σₖ₌ₙ₊₁²ⁿ 1/k (n = 5: 1627/2520).

``check`` adds 1/((2k − 1)·2k) for k = 1, …, n directly.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"n": 5}
ANSWER = Fraction(1627, 2520)
VARIANTS = [{"n": 1}, {"n": 3}, {"n": 12}]


def solve(n=5):
    return sum((Fraction(1, k) for k in range(n + 1, 2 * n + 1)), Fraction(0))


def check(n=5):
    return sum((Fraction(1, (2 * k - 1) * 2 * k) for k in range(1, n + 1)), Fraction(0))
