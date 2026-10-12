"""ข้อ 6 — ความยาวของ CD

กำหนดให้ ABC เป็นรูปสามเหลี่ยมที่มีมุม C เป็นมุมฉาก ลากส่วนของเส้นตรงจากจุด C ไป
ตั้งฉากกับด้าน AB ที่จุด D  ถ้า AD = 2 และ BD = 3 จงหาความยาวของ CD

The altitude to the hypotenuse is the geometric mean of the two pieces it cuts:
triangles ACD and CBD are each similar to ABC, so ``AD/CD = CD/BD`` and

    CD = √(AD · BD) = √(2 · 3) = **√6** ≈ 2.4495.

Equivalently, D lies inside the circle with diameter AB and CD is the half-chord
through it perpendicular to that diameter.

``solve`` uses the mean. ``check`` builds the figure in coordinates and measures
— and it *asserts* both defining properties (the right angle at C, and CD ⊥ AB)
by dot product before reading the length off, so the construction is verified
rather than assumed.
"""

from __future__ import annotations

from math import isqrt, sqrt

#: the two pieces the foot of the altitude cuts the hypotenuse into.
PARAMS = {"ad": 2, "bd": 3}
ANSWER = 2.449489742783178
TOL = 1e-9
VARIANTS = [
    {"ad": 4, "bd": 9},          # a whole number: 6
    {"ad": 1, "bd": 1},
    {"ad": 5, "bd": 20},
    {"ad": 3, "bd": 7},
    {"ad": 0, "bd": 5},          # the foot lands on A: no triangle
    {"ad": 2, "bd": -3},
]


def exact_square(ad=2, bd=3):
    """CD as a whole number when ad·bd is a perfect square, else None."""
    if ad <= 0 or bd <= 0:
        return None
    root = isqrt(ad * bd)
    return root if root * root == ad * bd else None


def solve(ad=2, bd=3):
    """CD = √(AD·BD), the geometric mean of the two pieces."""
    if ad <= 0 or bd <= 0:
        return None
    return sqrt(ad * bd)


def check(ad=2, bd=3):
    """Independent: place the triangle in coordinates and measure.

    A and B sit on the x-axis with D at the origin, and C is placed on the circle
    with diameter AB — the locus of the right angle — directly above D. Both
    defining conditions are then verified by dot product before the distance is
    taken, so nothing about the geometric mean is presupposed.
    """
    if ad <= 0 or bd <= 0:
        return None
    a = (-float(ad), 0.0)
    b = (float(bd), 0.0)
    centre_x = (a[0] + b[0]) / 2
    radius = (ad + bd) / 2
    height_sq = radius * radius - centre_x * centre_x
    if height_sq <= 0:
        return None
    c = (0.0, sqrt(height_sq))

    ca = (a[0] - c[0], a[1] - c[1])
    cb = (b[0] - c[0], b[1] - c[1])
    assert abs(ca[0] * cb[0] + ca[1] * cb[1]) < 1e-9, "the angle at C is not right"
    cd = (0.0 - c[0], 0.0 - c[1])
    ab = (b[0] - a[0], b[1] - a[1])
    assert abs(cd[0] * ab[0] + cd[1] * ab[1]) < 1e-9, "CD is not perpendicular to AB"
    return sqrt(cd[0] ** 2 + cd[1] ** 2)
