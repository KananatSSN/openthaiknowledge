"""ข้อ 18 — Σₖ₌₀¹²⁷³ 1/(1 + tan²⁵⁴⁸(kπ/2548))

1/(1 + tanᵖx) + 1/(1 + tanᵖ(π/2 − x)) = 1. Pair k with D/2 − k: k = 0 gives 1,
the pairs give 1 each and the middle term (when 4 | D) gives 1/2, so the total
is (D + 2)/4 = 1275/2.

``check`` adds the terms in floating point, computing each as
1/(1 + exp(p·ln tan)) so the huge power never overflows.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"denominator": 2548, "power": 2548}
ANSWER = Fraction(1275, 2)
TOL = 1e-9
VARIANTS = [{"denominator": 20, "power": 3}, {"denominator": 38}, {"denominator": 802, "power": 7}, {"denominator": 570, "power": 2333}]


def solve(denominator=2548, power=2548):
    return Fraction(denominator + 2, 4)


def check(denominator=2548, power=2548):
    total = 1.0  # k = 0
    for k in range(1, denominator // 2):
        z = power * math.log(math.tan(k * math.pi / denominator))
        total += 0.0 if z > 700 else 1 / (1 + math.exp(z))
    return total
