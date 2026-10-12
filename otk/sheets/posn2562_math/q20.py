"""ข้อ 20 — พื้นที่ของรูปสามเหลี่ยม BMN

กำหนดให้ ABC และ ABD เป็นรูปสามเหลี่ยมมุมฉากที่มี ∠ABC = ∠BAD = 90° ดังรูป โดยมี
AB = 4, BC = 6 และ AD = 8 หน่วย ลากส่วนของเส้นตรงจากจุด B ไปแบ่งครึ่งส่วนของ
เส้นตรง AD ที่จุด L  ถ้า AC ตัดกับ BD และ BL ที่จุด M และ N ตามลำดับ แล้ว
จงหาพื้นที่ของรูปสามเหลี่ยม BMN

The two right angles pin the figure to a coordinate grid: with A at the origin
and AB along the x-axis, ``AD ⊥ AB`` puts D straight above A and ``BC ⊥ AB``
puts C straight above B.

    A = (0, 0)   B = (4, 0)   C = (4, 6)   D = (0, 8)   L = (0, 4)

M and N are both on AC (``y = 3x/2``), so they are found by intersecting it with
BD (``y = 8 − 2x``) and BL (``y = 4 − x``):

    M = (16/7, 24/7),   N = (8/5, 12/5)

and the shoelace on B, M, N gives

    area = **72/35** ≈ 2.0571

Everything is rational because the two right angles make the whole figure
rational; no length is ever irrational and no square root appears.

``solve`` intersects the lines with exact fractions and shoelaces. ``check``
never forms a shoelace: M and N are located as parameters *along AC*, and the
area is taken as the difference of the two triangles ABM and ABN, which share
the base AB — legitimate precisely because A, N and M are collinear.
"""

from __future__ import annotations

from fractions import Fraction

#: AB along the x-axis, BC up from B, AD up from A; L splits AD at num/den.
PARAMS = {"ab": 4, "bc": 6, "ad": 8, "num": 1, "den": 2}
ANSWER = Fraction(72, 35)
VARIANTS = [
    {"ab": 4, "bc": 6, "ad": 8, "num": 1, "den": 3},
    {"ab": 3, "bc": 5, "ad": 9, "num": 1, "den": 2},
    {"ab": 5, "bc": 5, "ad": 5, "num": 1, "den": 2},
    {"ab": 4, "bc": 12, "ad": 8, "num": 2, "den": 3},
    {"ab": 4, "bc": 6, "ad": 8, "num": 1, "den": 1},     # L = D, so N = M
    {"ab": 0, "bc": 6, "ad": 8, "num": 1, "den": 2},     # degenerate
]


def _points(ab=4, bc=6, ad=8, num=1, den=2):
    """A, B, C, D, L as exact rational coordinates, or None."""
    if ab <= 0 or bc <= 0 or ad <= 0 or den <= 0 or not 0 < num <= den:
        return None
    a = (Fraction(0), Fraction(0))
    b = (Fraction(ab), Fraction(0))
    c = (Fraction(ab), Fraction(bc))
    d = (Fraction(0), Fraction(ad))
    ratio = Fraction(num, den)
    ell = (Fraction(0), ratio * ad)
    return a, b, c, d, ell


def _cross(p, q, r) -> Fraction:
    """Twice the signed area of the triangle pqr."""
    return ((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1]))


def _meet(p1, p2, p3, p4):
    """Intersection of lines p1p2 and p3p4, or None when they are parallel."""
    den = ((p1[0] - p2[0]) * (p3[1] - p4[1])
           - (p1[1] - p2[1]) * (p3[0] - p4[0]))
    if den == 0:
        return None
    one = p1[0] * p2[1] - p1[1] * p2[0]
    two = p3[0] * p4[1] - p3[1] * p4[0]
    x = (one * (p3[0] - p4[0]) - (p1[0] - p2[0]) * two) / den
    y = (one * (p3[1] - p4[1]) - (p1[1] - p2[1]) * two) / den
    return x, y


def solve(ab=4, bc=6, ad=8, num=1, den=2):
    """Area of BMN, by intersecting the three lines exactly."""
    got = _points(ab, bc, ad, num, den)
    if got is None:
        return None
    a, b, c, d, ell = got
    m = _meet(a, c, b, d)
    n = _meet(a, c, b, ell)
    if m is None or n is None or m == n:
        return None
    return abs(_cross(b, m, n)) / 2


def check(ab=4, bc=6, ad=8, num=1, den=2):
    """Independent: locate M and N along AC, then subtract two triangles.

    Each of BD and BL is written as a single linear condition and solved for the
    parameter t with ``M = A + t(C − A)``; the areas of ABM and ABN are then
    computed as ½·AB·(height above the x-axis), and BMN is their difference —
    valid because A, N and M all lie on AC. No cross product of BM and BN is
    ever taken.
    """
    got = _points(ab, bc, ad, num, den)
    if got is None:
        return None
    a, b, c, d, ell = got

    def along(p, q):
        """t with A + t(C − A) on the line pq, or None."""
        # line pq: (y − p_y)(q_x − p_x) = (x − p_x)(q_y − p_y)
        dx, dy = q[0] - p[0], q[1] - p[1]
        # substitute x = t·c_x, y = t·c_y (A is the origin)
        coef = c[1] * dx - c[0] * dy
        const = (0 - p[1]) * dx - (0 - p[0]) * dy
        if coef == 0:
            return None
        return -const / coef

    t_m, t_n = along(b, d), along(b, ell)
    if t_m is None or t_n is None or t_m == t_n:
        return None
    height_m, height_n = t_m * c[1], t_n * c[1]
    area_m = Fraction(ab) * abs(height_m) / 2
    area_n = Fraction(ab) * abs(height_n) / 2
    return abs(area_m - area_n)
