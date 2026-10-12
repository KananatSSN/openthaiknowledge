"""ข้อ 17 — พื้นที่สี่เหลี่ยมจัตุรัสที่มีสองมุมอยู่บนวงกลมแนบใน

สามเหลี่ยมมุมฉาก XYZ มีด้าน XZ ยาว 3 หน่วย และด้าน ZY ยาว 4 หน่วย วงกลมวงหนึ่งแนบใน
รูปสามเหลี่ยมนี้โดยเส้นรอบวงสัมผัสด้าน XZ ที่จุด E สี่เหลี่ยมจัตุรัส ABCD มีมุม B และ C
อยู่บนเส้นรอบวงของวงกลมและด้าน AD อยู่บนด้าน XZ ของสามเหลี่ยมโดยที่จุด E แบ่งครึ่งด้าน AD
ดังรูป จงหาพื้นที่สี่เหลี่ยม ABCD

**Read off the figure, not the text:** AD lies *along the leg XZ*, E is both the
incircle's tangent point on that leg and the midpoint of AD, and B and C are the
two vertices off the leg — so the square straddles E symmetrically.

Put the right angle at the origin with the legs on the axes. The incircle has
centre (r, r) and touches the leg at E = (0, r). A square of side s placed as
described has

    A = (0, r + s/2)   D = (0, r − s/2)   B = (s, r + s/2)   C = (s, r − s/2)

and B and C are the *same* distance from the centre, so one equation covers both:

    (s − r)² + (s/2)² = r²   ⟹   (5/4)s² = 2rs   ⟹   s = 8r/5

**The legs only enter through r.** Area = s² = 64r²/25, and for the 3-4-5
triangle r = (3 + 4 − 5)/2 = 1, so the area is **64/25**.

One coincidence of these particular numbers is worth recording, because the
figure shows it and a redraw does not: at 3-4-5 the vertex B lands *exactly* on
the hypotenuse. In general B is strictly inside — ``0.8a + 0.6b ≤ √(a² + b²)`` by
Cauchy–Schwarz, with equality only when a : b = 4 : 3.

``solve`` uses r = (a + b − c)/2. ``check`` builds the figure in coordinates with
the *other* inradius formula, r = area/semiperimeter = ab/(a + b + c), then finds
the side by bisecting the circle equation rather than solving it, and confirms
the incircle really is tangent to all three sides before measuring.
"""

from __future__ import annotations

from fractions import Fraction
from math import hypot, isqrt

#: right angle between the two legs.
PARAMS = {"leg_a": 4, "leg_b": 3}
ANSWER = Fraction(64, 25)
TOL = 1e-7
VARIANTS = [
    {"leg_a": 8, "leg_b": 6},
    {"leg_a": 5, "leg_b": 12},
    {"leg_a": 12, "leg_b": 5},
    {"leg_a": 8, "leg_b": 15},
    {"leg_a": 1, "leg_b": 1},          # an irrational inradius
    {"leg_a": 7, "leg_b": 24},
]


def solve(leg_a=4, leg_b=3):
    """Area = 64r²/25, with r the inradius of the right triangle."""
    if leg_a <= 0 or leg_b <= 0:
        return None
    squared = leg_a * leg_a + leg_b * leg_b
    root = isqrt(squared) if float(squared).is_integer() else 0
    if root * root == squared:                     # a Pythagorean triple: exact
        inradius = Fraction(leg_a + leg_b - root, 2)
        return Fraction(64, 25) * inradius * inradius
    inradius = (leg_a + leg_b - squared ** 0.5) / 2
    return 64 * inradius * inradius / 25


def check(leg_a=4, leg_b=3):
    """Independent: build the figure and measure it.

    The inradius comes from area over semiperimeter — a different formula from
    ``(a + b − c)/2`` — and is confirmed by measuring the distance from the
    centre to all three sides. The square's side is then bisected out of the
    circle equation instead of being solved for.
    """
    if leg_a <= 0 or leg_b <= 0:
        return None
    a, b = float(leg_a), float(leg_b)
    c = hypot(a, b)
    r = a * b / (a + b + c)                        # area / semiperimeter

    # the centre must be r from each leg and r from the hypotenuse bx + ay = ab
    if abs((a * b - r * (a + b)) / c - r) > 1e-9:
        return None

    def residual(side: float) -> float:
        return (side - r) ** 2 + (side / 2) ** 2 - r * r

    lo, hi = r * 1e-9, 4 * r
    if residual(hi) <= 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        value = residual(mid)
        if value == 0.0:
            lo = hi = mid
            break
        if value < 0:
            lo = mid
        else:
            hi = mid
    side = (lo + hi) / 2

    # the two off-leg corners really are on the circle
    for corner in ((side, r + side / 2), (side, r - side / 2)):
        if abs(hypot(corner[0] - r, corner[1] - r) - r) > 1e-7:
            return None
    return side * side
