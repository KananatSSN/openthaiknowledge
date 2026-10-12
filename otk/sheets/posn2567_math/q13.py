"""ข้อ 13 — พื้นที่ของรูปสี่เหลี่ยมคางหมูที่เส้นทแยงมุมตั้งฉากกัน

รูปสี่เหลี่ยมคางหมูรูปหนึ่งมีส่วนสูงยาว 4 หน่วย โดยที่เส้นทแยงมุมของรูปสี่เหลี่ยม
คางหมูตั้งฉากกัน ถ้าเส้นทแยงมุมเส้นหนึ่งยาว 5 หน่วย จงหาพื้นที่ของรูปสี่เหลี่ยม
คางหมูนี้ (เขียนคำตอบเป็นเศษส่วนอย่างต่ำ)

No figure — the item is pure trigonometry, and the trapezoid is not determined
by the data (only its area is).

Let θ be the angle the given diagonal d₁ makes with the two parallel sides. Its
vertical extent is the height, so

    sin θ = h/d₁.

The other diagonal is perpendicular to it, so it makes θ with the *perpendicular*
to the parallel sides and its vertical extent gives

    d₂ cos θ = h,   i.e.   d₂ = h/cos θ = h·d₁/√(d₁² - h²).

Diagonals that cross at a right angle give area = d₁d₂/2 (the quadrilateral
splits into four right triangles), so

    area = h·d₁² / (2√(d₁² - h²))

= 4·25/(2·3) = 50/3 for the sheet's numbers. The sheet asks for a fraction, so
``solve`` returns one only when d₁² - h² is a perfect square, and ``None``
otherwise — the generator's pool is built from exactly those pairs.

``solve`` needs d₁ > h: a diagonal cannot be shorter than the height.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: the height, and the one diagonal whose length is given.
PARAMS = {"height": 4, "diagonal": 5}
ANSWER = Fraction(50, 3)
VARIANTS = [
    {"height": 3, "diagonal": 5},         # the 3-4-5 the other way round
    {"height": 12, "diagonal": 13},
    {"height": 8, "diagonal": 17},
    {"height": 20, "diagonal": 29},
    {"height": 6, "diagonal": 7},         # irrational leg — no fraction exists
    {"height": 9, "diagonal": 9},         # degenerate: the diagonal is the height
]
TOL = 1e-9


def solve(height=4, diagonal=5):
    """Area = h·d₁²/(2√(d₁²-h²)) — a fraction only when the root is rational."""
    if height <= 0 or diagonal <= height:
        return None
    leg2 = diagonal * diagonal - height * height
    leg = math.isqrt(leg2)
    if leg * leg != leg2:
        return None
    return Fraction(height * diagonal * diagonal, 2 * leg)


def check(height=4, diagonal=5):
    """Independent: build a trapezoid with these data and shoelace it.

    The diagonals are placed as vectors first and the four vertices derived from
    them, so the perpendicularity and both stated lengths are properties of the
    construction that get asserted back — then the area comes from the shoelace
    formula, never from d₁d₂/2.
    """
    if height <= 0 or diagonal <= height:
        return None
    leg2 = diagonal * diagonal - height * height
    leg = math.isqrt(leg2)
    if leg * leg != leg2:
        return None

    h, d1 = float(height), float(diagonal)
    theta = math.asin(h / d1)                     # tilt of the given diagonal

    # Bottom side on y = 0, top side on y = h. Put A at the origin and let AC be
    # the given diagonal, rising at theta; then BD is perpendicular to it, and
    # its own rise must also be h, which fixes its length.
    a = (0.0, 0.0)
    c = (d1 * math.cos(theta), d1 * math.sin(theta))
    d2 = h / math.cos(theta)
    # BD points up and to the left: direction (-sin θ, cos θ) rotated from AC.
    bd = (-d2 * math.sin(theta), d2 * math.cos(theta))
    # B is on y = 0 and D on y = h. Only BD̅'s direction and length are fixed, so
    # slide it until the four vertices are in convex position — the area cannot
    # depend on where, and putting D halfway along the top keeps them so.
    d = (c[0] / 2, h)
    b = (d[0] - bd[0], 0.0)

    assert abs((c[0] - a[0]) * bd[0] + (c[1] - a[1]) * bd[1]) < 1e-9 * d1 * d2
    assert abs(math.dist(a, c) - d1) < 1e-9 and abs(c[1] - h) < 1e-9
    assert abs(math.dist(b, d) - d2) < 1e-9       # the second diagonal
    assert a[1] == b[1] == 0.0 and abs(d[1] - h) < 1e-9   # AB̅ ∥ DC̅, h apart
    assert 0 < d[0] < c[0] and b[0] > 0            # convex, so shoelace applies

    quad = [a, b, c, d]                           # A, B bottom; C, D top
    area = abs(sum(p[0] * q[1] - q[0] * p[1]
                   for p, q in zip(quad, quad[1:] + quad[:1]))) / 2
    return Fraction(area).limit_denominator(10 ** 6)
