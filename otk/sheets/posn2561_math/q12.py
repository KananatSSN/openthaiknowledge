"""ข้อ 12 — จำนวน n ที่น้อยที่สุดที่ทำให้สมการเป็นจริง

ให้ xᵢ ∈ ℝ โดยที่ |xᵢ| < 1 สำหรับ i = 1, 2, …, n และ

    x₁² + x₂² + ⋯ + xₙ² = (x₁ + x₂ + ⋯ + xₙ)² + 2561

จงหาค่า n ที่น้อยที่สุดที่ทำให้สมการนี้เป็นจริง

Write ``f(x) = Σxᵢ² − (Σxᵢ)²``. The second derivative of f in any single
variable is ``2 − 2 = 0``: **f is linear in each coordinate separately**, so over
the closed cube [−1, 1]ⁿ its maximum sits at a vertex. At a vertex every
``xᵢ = ±1``, so ``Σxᵢ² = n`` and ``Σxᵢ = k`` where k counts the signs and has the
same parity as n. There f = n − k², largest at the smallest admissible |k|:

    n even → k = 0 → sup f = n          n odd → k = ±1 → sup f = n − 1

The cube here is *open*, so that supremum is approached, never reached; and f is
continuous and vanishes at the origin, so every value in [0, sup) is hit. The
equation asks for f = 2561, hence

    n even: need n > 2561      n odd: need n − 1 > 2561

and the smallest n is 2562 — even, and 2562 > 2561. **n = 2562.**

(The rule in general: ``target + 1`` when the target is odd, ``target + 2`` when
it is even, because an odd n throws one unit away on the parity of k.)

``solve`` applies that parity rule. ``check`` knows nothing about vertices: for
each n it searches the two-value family — k coordinates at +u and n − k at −u —
for a u that satisfies the printed equation with |u| < 1, and returns the first n
that yields an actual witness.
"""

from __future__ import annotations

#: Σxᵢ² = (Σxᵢ)² + target, with |xᵢ| < 1.
PARAMS = {"target": 2561}
ANSWER = 2562
VARIANTS = [
    {"target": 1},
    {"target": 2},
    {"target": 10},
    {"target": 99},
    {"target": 100},
    {"target": 2560},
    {"target": 0},              # nothing to force: no n is large enough
]


def solve(target=2561):
    """Smallest n, from the parity of the target."""
    if target < 1:
        return None
    return target + 1 if target % 2 else target + 2


def check(target=2561):
    """Independent: find the first n that admits an explicit witness.

    For each n the family ``k`` coordinates at +u and ``n − k`` at −u gives
    ``Σxᵢ² = n u²`` and ``Σxᵢ = (2k − n)u``, so the printed equation reads
    ``u²(n − (2k − n)²) = target``. A witness needs ``0 < u² < 1``; the first n
    for which some k allows one is reported, and the witness is substituted back
    into the equation before it is believed.
    """
    if target < 1:
        return None
    if target > 20_000:
        return None

    for n in range(1, target + 3):
        for k in range(n + 1):
            spread = n - (2 * k - n) ** 2
            if spread <= 0:
                continue
            u_square = target / spread
            if not 0 < u_square < 1:
                continue
            u = u_square ** 0.5
            squares = n * u * u
            total = (2 * k - n) * u
            if abs(squares - total * total - target) < 1e-6 * max(1.0, target):
                return n
    return None
