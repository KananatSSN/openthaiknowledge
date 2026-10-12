"""ข้อ 10 — ค่าของ AC²/((AB)(AE))

ให้ ABCD เป็นรูปสี่เหลี่ยมขนมเปียกปูน และ CE ตั้งฉากกับ BE ดังรูป
จงหาค่าของ  AC²/((AB)(AE))

รูปประกอบ: E อยู่บน AB ต่อออกไปทางด้าน B และ CE ตั้งฉากกับเส้นนั้น — E is the
foot of the perpendicular from C to line AB.

Put A at the origin with AB along the x-axis, side s, ∠DAB = α. Then
C = (s(1 + cos α), s·sin α) and E = (s(1 + cos α), 0), so

    AC² = s²[(1 + cos α)² + sin²α] = 2s²(1 + cos α)
    AB·AE = s · s(1 + cos α)

and the ratio is 2 for every rhombus. Both the side and the angle cancel, which
is why the question can be asked with no measurement given at all.

That independence is the claim worth testing, so ``PARAMS`` carries a side and
an angle even though ``solve`` ignores them: the variants push those around and
``check`` rebuilds the figure from each pair and measures. A ``solve`` that had
smuggled in a dependence on either would be caught immediately.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"side": 6, "angle_deg": 70}
ANSWER = Fraction(2)
VARIANTS = [
    {"angle_deg": 30},
    {"angle_deg": 120},
    {"side": 1, "angle_deg": 45},
    {"side": 13, "angle_deg": 95},
    {"side": 2, "angle_deg": 150},
]
TOL = 1e-9


def solve(side=6, angle_deg=70):
    """AC²/((AB)(AE)) — 2 for any rhombus, whatever its side and angle."""
    if side <= 0 or not 0 < angle_deg < 180:
        return None
    return Fraction(2)


def check(side=6, angle_deg=70):
    """Independent: build this rhombus in coordinates and measure the ratio."""
    if side <= 0 or not 0 < angle_deg < 180:
        return None
    a = math.radians(angle_deg)
    cx, cy = side * (1 + math.cos(a)), side * math.sin(a)
    ex, ey = cx, 0.0                        # foot of the perpendicular from C
    # CE ⊥ AB, as the question states.
    assert abs((cx - ex) * side + (cy - ey) * 0.0) < 1e-9
    ae = math.hypot(ex, ey)
    ac2 = cx * cx + cy * cy
    return Fraction(ac2 / (side * ae)).limit_denominator(10 ** 6)
