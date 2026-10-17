"""วันที่สอง ข้อ 3 — X, Y, Z อยู่บนเส้นตรงเดียวกัน  (พิสูจน์)

∠AMC = ∠BND = 90°; O on the radical axis gives OM·OC = ON·OB, so B, C, M, N
are concyclic; an angle chase (sketched in the bank note) makes A, M, N, D
concyclic, and AM, DN, XY are the three radical axes, meeting at Z. The solver
computes the point P where XY meets the line of centres:
AP = AB·AD/(AB + AD − AC) (AB = 2, AC = 5, AD = 8: 16/5).

``check`` intersects the two circles in coordinates and reads the common chord.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"ab": 2, "ac": 5, "ad": 8}
ANSWER = Fraction(16, 5)
VARIANTS = [{"ab": 3, "ac": 13, "ad": 27}, {"ab": 1, "ac": 2, "ad": 3}, {"ab": 5, "ac": 9, "ad": 20}]


def solve(ab=2, ac=5, ad=8):
    return Fraction(ab * ad, ab + ad - ac)


def check(ab=2, ac=5, ad=8):
    o1, r1 = Fraction(ac, 2), Fraction(ac, 2)
    o2, r2 = Fraction(ab + ad, 2), Fraction(ad - ab, 2)
    x0 = (r1 * r1 - r2 * r2 + o2 * o2 - o1 * o1) / (2 * (o2 - o1))
    assert r1 * r1 - (x0 - o1) ** 2 > 0  # the circles do meet
    return x0
