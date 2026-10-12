"""ข้อ 6 — ความยาวส่วนสูง AE ในสามเหลี่ยมหน้าจั่ว

กำหนด ABC เป็นรูปสามเหลี่ยมมีพื้นที่ 48 ตารางหน่วย ให้จุด D และจุด E อยู่บนด้าน AB และ BC
ตามลำดับ ซึ่งทำให้ CD ตั้งฉากกับ AB และ AE ตั้งฉากกับ BC  ถ้า AC = BC และ AB = 16
จงหาความยาวของ AE

Two altitudes of the same triangle measure the same area against different bases,
and that is the entire item — the two feet D and E never have to be located.

``AC = BC`` makes the triangle isosceles on base AB, so the altitude CD lands at
the midpoint of AB and

    area = ½·AB·CD   ⟹   48 = ½·16·CD   ⟹   CD = 6

Pythagoras on half the base then gives the equal sides:

    BC = √(8² + 6²) = 10

and measuring the same area against BC instead:

    48 = ½·BC·AE   ⟹   AE = 96/10 = **48/5**

``solve`` follows that. ``check`` puts the triangle in coordinates, drops the
perpendicular from A to the line BC by projection, and measures the distance —
confirming on the way that the printed area and the isosceles condition really
hold for the figure it built.
"""

from __future__ import annotations

from fractions import Fraction
from math import hypot, isqrt

#: isosceles with AC = BC on base AB, of the given area.
PARAMS = {"base": 16, "area": 48}
ANSWER = Fraction(48, 5)
TOL = 1e-9
VARIANTS = [
    {"base": 10, "area": 60},
    {"base": 6, "area": 12},
    {"base": 20, "area": 30},
    {"base": 16, "area": 96},
    {"base": 7, "area": 14},
    {"base": 24, "area": 48},
]


def solve(base=16, area=48):
    """Two altitudes, one area: AE = 2·area/BC with BC from the isosceles half."""
    if base <= 0 or area <= 0:
        return None
    height = Fraction(2 * area, base)                 # CD
    half = Fraction(base, 2)
    side_squared = half * half + height * height      # BC²
    root = isqrt(side_squared.numerator * side_squared.denominator)
    exact = Fraction(root, side_squared.denominator)
    if exact * exact != side_squared:
        return 2 * area / float(side_squared) ** 0.5
    return 2 * area / exact


def check(base=16, area=48):
    """Independent: build the triangle and project A onto the line BC.

    A = (0, 0), B = (base, 0) and C above the midpoint at the height the area
    demands. The foot E is found by projecting A onto BC — no second area
    formula is used — and the construction is audited against the printed data
    (|AC| = |BC|, and the shoelace area) before AE is measured.
    """
    if base <= 0 or area <= 0:
        return None
    a = (0.0, 0.0)
    b = (float(base), 0.0)
    height = 2 * area / base
    c = (base / 2, height)

    if abs(hypot(*c) - hypot(c[0] - b[0], c[1] - b[1])) > 1e-9:
        return None
    shoelace = abs(a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1])
                   + c[0] * (a[1] - b[1])) / 2
    if abs(shoelace - area) > 1e-9:
        return None

    dx, dy = c[0] - b[0], c[1] - b[1]
    t = ((a[0] - b[0]) * dx + (a[1] - b[1]) * dy) / (dx * dx + dy * dy)
    foot = (b[0] + t * dx, b[1] + t * dy)
    return hypot(a[0] - foot[0], a[1] - foot[1])
