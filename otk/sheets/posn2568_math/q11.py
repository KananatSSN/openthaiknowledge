"""ข้อ 11 — ผลคูณของ (r + 1/r) เหนือรากทั้งหกของสมการ

ให้ a, b, c, d, e, f เป็นจำนวนจริงที่แตกต่างกันและเป็นคำตอบของ
    x⁶ − p·x⁴ + p·x² − 1 = 0            (โจทย์: p = 25)
ค่าของ (a + 1/a)(b + 1/b)⋯(f + 1/f) เท่ากับเท่าใด

Method: the polynomial is even, so u = x² satisfies u³ − p·u² + p·u − 1, which
has u = 1 as a root and factors as (u − 1)(u² − (p−1)u + 1). Each u contributes
the root pair ±√u, so

    ∏(r + 1/r) = ∏(r²+1) / ∏ r ,   ∏ r = (−1)⁶ · (constant term) = −1,
    ∏(r²+1) = (1+1)² · [(u₁+1)(u₂+1)]² = 4·[u₁u₂ + u₁ + u₂ + 1]² = 4(p+1)²

using Vieta on the quadratic (u₁u₂ = 1, u₁+u₂ = p−1). So the answer is
−4(p+1)², i.e. −2704 at p = 25.

``check`` asks numpy for the six roots and multiplies (r + 1/r) out.
"""

from __future__ import annotations

PARAMS = {"p": 25}
ANSWER = -2704
VARIANTS = [{"p": 3}, {"p": 4}, {"p": 10}, {"p": 99}, {"p": 7}]


def solve(p=25):
    """∏(r + 1/r) over the six roots."""
    return -4 * (p + 1) ** 2


def check(p=25):
    """Independent: numerically root-find the sextic and take the product."""
    import numpy as np
    roots = np.roots([1.0, 0.0, -float(p), 0.0, float(p), 0.0, -1.0])
    product = complex(1)
    for r in roots:
        product *= r + 1 / r
    assert abs(product.imag) < 1e-6, f"unexpected complex product {product}"
    return product.real
