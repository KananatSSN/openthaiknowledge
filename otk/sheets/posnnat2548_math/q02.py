"""ข้อ 2 — A′B/AB เมื่อ BH เท่ากับรัศมีวงกลมล้อม (BH = t·R, โจทย์ t = 1)

In an acute triangle BH = 2R cos B, so cos B = t/2, and in the right triangle
ABA′, A′B = AB cos B: the ratio is t/2 = 1/2.

``check`` builds an acute triangle with that angle B (2R = 1), finds H as the
intersection of two altitudes, and measures both BH/R and A′B/AB.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"t": Fraction(1)}
ANSWER = Fraction(1, 2)
VARIANTS = [{"t": Fraction(1, 2)}, {"t": Fraction(3, 2)}, {"t": Fraction(6, 5)}, {"t": Fraction(1, 3)}]


def solve(t=Fraction(1)):
    return t / 2


def check(t=Fraction(1)):
    angle_b = math.acos(float(t) / 2)
    angle_a = (math.pi - angle_b) / 2 + 0.05
    angle_c = math.pi - angle_a - angle_b
    assert max(angle_a, angle_b, angle_c) < math.pi / 2
    c = (math.sin(angle_a), 0.0)  # B at the origin; BC = 2R sin A with 2R = 1
    side_ab = math.sin(angle_c)
    a = (side_ab * math.cos(angle_b), side_ab * math.sin(angle_b))
    # altitude from A is x = a_x; altitude from C is perpendicular to AB through C
    hx = a[0]
    hy = (c[0] - hx) * a[0] / a[1]
    assert math.isclose(math.hypot(hx, hy) / 0.5, float(t))
    return a[0] / side_ab
