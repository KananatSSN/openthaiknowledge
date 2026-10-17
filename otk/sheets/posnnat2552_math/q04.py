"""ข้อ 4 — [BGH]/[ABC] เมื่อ D กึ่งกลาง BC, AF = FE = EC และ AD ตัด BE, BF ที่ G, H

Area ratios are affine invariants, so the unit right triangle A = (0, 0),
B = (1, 0), C = (0, 1) gives the answer exactly in fractions: 3/20 (F, E at 1/3,
2/3 of AC).

``check`` uses a skewed floating-point triangle instead and the shoelace area.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"f": Fraction(1, 3), "e": Fraction(2, 3)}
ANSWER = Fraction(3, 20)
TOL = 1e-9
VARIANTS = [{"f": Fraction(1, 4), "e": Fraction(1, 2)}, {"f": Fraction(1, 5), "e": Fraction(2, 5)}, {"f": Fraction(1, 2), "e": Fraction(3, 4)}]


def _intersect(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    return p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])


def _area(p, q, r):
    return abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) / 2


def solve(f=Fraction(1, 3), e=Fraction(2, 3)):
    a, b, c = (Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))
    d = (Fraction(1, 2), Fraction(1, 2))
    g = _intersect(a, d, b, (Fraction(0), e))
    h = _intersect(a, d, b, (Fraction(0), f))
    return _area(b, g, h) / _area(a, b, c)


def check(f=Fraction(1, 3), e=Fraction(2, 3)):
    a, b, c = (0.3, -1.2), (7.1, 0.4), (2.2, 5.9)
    d = ((b[0] + c[0]) / 2, (b[1] + c[1]) / 2)

    def on_ac(t):
        return (a[0] + float(t) * (c[0] - a[0]), a[1] + float(t) * (c[1] - a[1]))

    g = _intersect(a, d, b, on_ac(e))
    h = _intersect(a, d, b, on_ac(f))
    return _area(b, g, h) / _area(a, b, c)
