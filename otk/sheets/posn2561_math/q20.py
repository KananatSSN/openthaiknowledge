"""ข้อ 20 — ความยาวเส้นสัมผัส AB จากคอร์ดที่ตั้งฉากกับเส้นผ่านศูนย์กลาง

จากจุด A ลากเส้นสัมผัสวงกลมรัศมี 5 หน่วย ที่จุด B และ C กำหนดให้ BD เป็นเส้นผ่านศูนย์กลาง
ของวงกลมและ CE ตั้งฉากกับ BD ดังรูป ถ้าให้ CE ยาว 4 หน่วย จงหาความยาว AB

**Read off the figure:** the foot E sits between the centre and D — that is, C is
on the far half of the diameter from B — and A is on the far side of the tangent
at B. Put the centre at the origin with B = (−r, 0) and D = (r, 0). Then

    C = (√(r² − h²), h)      with h = CE

The tangent at B is the vertical line x = −r; the tangent at C is
``x·√(r² − h²) + y·h = r²``. Substituting x = −r into the second,

    AB = y = r(r + √(r² − h²)) / h

and for r = 5, h = 4 that is 5·(5 + 3)/4 = **10**.

Nothing else on the figure is needed — in particular BD being a diameter is what
makes the tangent at B perpendicular to it, which is what puts A on x = −r.

``solve`` evaluates that formula. ``check`` never writes a tangent-line equation:
it constructs both tangents as the lines through B and through C perpendicular to
the radii, intersects them numerically, and then confirms the two invariants the
construction must satisfy — AB = AC (equal tangents) and OA² = r² + AB² — before
reporting the measured length.
"""

from __future__ import annotations

from fractions import Fraction
from math import hypot, isqrt

#: circle radius, and the perpendicular CE from the circle to the diameter.
PARAMS = {"r": 5, "ce": 4}
ANSWER = 10
TOL = 1e-7
VARIANTS = [
    {"r": 13, "ce": 5},
    {"r": 13, "ce": 12},
    {"r": 25, "ce": 7},
    {"r": 10, "ce": 6},
    {"r": 5, "ce": 5},          # C at the top: E is the centre
    {"r": 5, "ce": 7},          # CE longer than the radius: no such chord
    {"r": 6, "ce": 4},          # an irrational offset
]


def solve(r=5, ce=4):
    """AB = r(r + √(r² − ce²)) / ce, from the two tangent lines."""
    if r <= 0 or ce <= 0 or ce > r:
        return None
    gap = r * r - ce * ce
    root = isqrt(gap)
    if root * root == gap:                          # exact
        value = Fraction(r * (r + root), ce)
        return int(value) if value.denominator == 1 else value
    return r * (r + gap ** 0.5) / ce


def check(r=5, ce=4):
    """Independent: build both tangents as perpendiculars and measure AB.

    Each tangent is the line through its point of contact with direction
    perpendicular to that radius; the two are intersected by determinants. The
    construction is then audited against facts it was not given — the two tangent
    lengths from A are equal, and OA² = r² + AB² — so a mis-sited C shows up as a
    refusal rather than a number.
    """
    if r <= 0 or ce <= 0 or ce > r:
        return None
    radius, h = float(r), float(ce)
    contact_b = (-radius, 0.0)
    contact_c = ((radius * radius - h * h) ** 0.5, h)

    def tangent(point):
        # through `point`, perpendicular to the radius: px + qy = t
        return point[0], point[1], point[0] ** 2 + point[1] ** 2

    a1, b1, t1 = tangent(contact_b)
    a2, b2, t2 = tangent(contact_c)
    determinant = a1 * b2 - a2 * b1
    if abs(determinant) < 1e-12:
        return None
    apex = ((t1 * b2 - t2 * b1) / determinant,
            (a1 * t2 - a2 * t1) / determinant)

    length_b = hypot(apex[0] - contact_b[0], apex[1] - contact_b[1])
    length_c = hypot(apex[0] - contact_c[0], apex[1] - contact_c[1])
    if abs(length_b - length_c) > 1e-7 * max(1.0, length_b):
        return None
    if abs(hypot(*apex) ** 2 - radius * radius - length_b * length_b) > 1e-6:
        return None
    return length_b
