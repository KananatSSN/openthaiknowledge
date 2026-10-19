"""ข้อ 8 — ถ้า A, S, T อยู่บนเส้นตรงเดียวกัน แล้ว P อยู่บนเส้นมัธยฐาน  (พิสูจน์)

A on the radical axis ST means equal powers: AD·AC = AE·AB, so AD/AC = AE/AB = λ
when the powers are compared along the sides, i.e. DE ∥ BC; then P = BD ∩ CE
lies on the median from A by Ceva. With A = (0, h) over BC on the x-axis, P is
at height h(1 − λ)/(1 + λ). The solver returns that height (h = 8, λ = 1/3: 4).

``check`` builds D, E from λ, both circles on diameters BD and CE, asserts A has
equal power to them (so A lies on line ST), finds P, asserts it lies on the
median from A, and returns its height.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"left": 3, "right": 5, "altitude": 8, "ratio": Fraction(1, 3)}
ANSWER = 4
VARIANTS = [{"left": 4, "right": 4, "altitude": 9, "ratio": Fraction(1, 2)},
            {"left": 2, "right": 7, "altitude": 10, "ratio": Fraction(3, 4)},
            {"left": 6, "right": 3, "altitude": 11, "ratio": Fraction(2, 5)}]


def solve(left=3, right=5, altitude=8, ratio=Fraction(1, 3)):
    return altitude * (1 - ratio) / (1 + ratio)


def _power(point, p, q):
    centre = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    r2 = ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) / 4
    return (point[0] - centre[0]) ** 2 + (point[1] - centre[1]) ** 2 - r2


def _meet(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


def check(left=3, right=5, altitude=8, ratio=Fraction(1, 3)):
    A = (Fraction(0), Fraction(altitude))
    B, C = (Fraction(-left), Fraction(0)), (Fraction(right), Fraction(0))
    D = (A[0] + ratio * (C[0] - A[0]), A[1] + ratio * (C[1] - A[1]))
    E = (A[0] + ratio * (B[0] - A[0]), A[1] + ratio * (B[1] - A[1]))
    assert _power(A, B, D) == _power(A, C, E)
    P = _meet(B, D, C, E)
    mid = ((B[0] + C[0]) / 2, Fraction(0))
    assert (P[0] - A[0]) * (mid[1] - A[1]) == (P[1] - A[1]) * (mid[0] - A[0])
    return P[1]
