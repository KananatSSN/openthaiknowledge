"""ข้อ 15 — ขนาดของ ∠BCD

ให้ ABCD เป็นรูปสี่เหลี่ยม โดย AB = 8, AC = 12, AD = 18  ถ้า ∠BAC = ∠CAD = 30°
แล้ว ∠BCD มีขนาดกี่องศา

The three lengths are a geometric progression — 8, 12, 18 with ratio 3/2 — so

    AB/AC = AC/AD

and with the equal included angles ∠BAC = ∠CAD = θ, triangles ABC and ACD are
**similar** (SAS). Therefore ∠ACB = ∠ADC, and

    ∠BCD = ∠BCA + ∠ACD = ∠ADC + ∠ACD = 180° - ∠CAD = 180° - θ

= **150°**. The lengths never appear in the answer, only the fact that they are
in proportion; ``solve`` checks that proportion and returns ``None`` without it,
because then ∠BCD genuinely depends on all three.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: AB, AC, AD and the two equal angles at A.
PARAMS = {"ab": 8, "ac": 12, "ad": 18, "theta_deg": 30}
ANSWER = Fraction(150)
VARIANTS = [
    {"ab": 4, "ac": 6, "ad": 9, "theta_deg": 30},
    {"ab": 8, "ac": 12, "ad": 18, "theta_deg": 50},
    {"ab": 9, "ac": 6, "ad": 4, "theta_deg": 40},      # ratio the other way
    {"ab": 5, "ac": 10, "ad": 20, "theta_deg": 25},
    {"ab": 8, "ac": 12, "ad": 20, "theta_deg": 30},    # not a proportion
    {"ab": 8, "ac": 12, "ad": 18, "theta_deg": 95},    # 2θ ≥ 180 is no quadrilateral
]
TOL = 1e-7


def solve(ab=8, ac=12, ad=18, theta_deg=30):
    """∠BCD = 180° - θ, whenever AB·AD = AC²."""
    if min(ab, ac, ad) <= 0 or not 0 < theta_deg < 90:
        return None
    if ab * ad != ac * ac:
        return None
    return 180 - Fraction(theta_deg)


def check(ab=8, ac=12, ad=18, theta_deg=30):
    """Independent: place the quadrilateral in coordinates and measure ∠BCD.

    A sits at the origin with AC̅ along the x-axis and B, D at ±θ from it, exactly
    as the statement describes; the angle at C is then a dot product. Nothing
    here knows about similar triangles — which is why it also returns an answer
    for lengths that are *not* in proportion, and ``solve`` returning ``None``
    there is a deliberate difference, checked by the variants.
    """
    if min(ab, ac, ad) <= 0 or not 0 < theta_deg < 90:
        return None
    if ab * ad != ac * ac:
        return None
    t = math.radians(theta_deg)
    a = (0.0, 0.0)
    c = (float(ac), 0.0)
    b = (ab * math.cos(t), ab * math.sin(t))
    d = (ad * math.cos(t), -ad * math.sin(t))

    def ang(p, q, r) -> float:
        u = (p[0] - q[0], p[1] - q[1])
        v = (r[0] - q[0], r[1] - q[1])
        cos = (u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))
        return math.degrees(math.acos(max(-1.0, min(1.0, cos))))

    assert abs(ang(b, a, c) - theta_deg) < 1e-9
    assert abs(ang(c, a, d) - theta_deg) < 1e-9
    return Fraction(ang(b, c, d)).limit_denominator(10 ** 6)
