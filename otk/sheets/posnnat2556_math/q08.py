"""ข้อ 8 — a₃a₂₀₁₁ ≥ 1012036  (พิสูจน์)

p(x) = x·Π(x² − bᵢ²) for n = 1006 pairs, so a_{2n−1} = −Σbᵢ² and
a₃ = (−1)ⁿ⁻¹Πbᵢ²·Σbᵢ⁻². With Πbᵢ = 1 and n even, a₃a_{2n−1} = (Σbᵢ²)(Σbᵢ⁻²)
≥ n² by Cauchy–Schwarz, with equality at every bᵢ = 1. The solver returns that
minimum n² (1006² = 1012036).

``check`` multiplies out the polynomial for bᵢ = 1, keeping only the two lowest
and two highest coefficients of Π(y − bᵢ²), and confirms that perturbed roots
with the same product give a larger value.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"n": 1006}
ANSWER = 1012036
VARIANTS = [{"n": 2}, {"n": 4}, {"n": 10}, {"n": 50}]


def solve(n=1006):
    return n * n


def _a3_times_top(squares):
    # Π(y − s): low = [y⁰, y¹] coefficients, high = [y^(m−1)] coefficient
    low0, low1, top = Fraction(1), Fraction(0), Fraction(0)
    for count, s in enumerate(squares):
        low0, low1 = -s * low0, low0 - s * low1
        top = top - s  # coefficient of y^(count) in a monic product of count + 1 factors
    a3 = low1  # x·Q(x²): x³ comes from y¹
    a_top = top  # x^(2n−1) comes from y^(n−1)
    return a3 * a_top


def check(n=1006):
    best = _a3_times_top([Fraction(1)] * n)
    for t in (Fraction(2), Fraction(3, 2), Fraction(5, 7)):
        b = [t, 1 / t] + [Fraction(1)] * (n - 2)
        assert _a3_times_top([x * x for x in b]) > best
    return best
