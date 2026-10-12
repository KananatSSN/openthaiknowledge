"""ข้อ 5 — พื้นที่ก้นบ่อเลี้ยงปลาทรงสี่เหลี่ยมมุมฉาก

กำหนดให้ บ่อเลี้ยงปลารูปทรงสี่เหลี่ยมมุมฉากบ่อหนึ่ง กว้าง x หน่วย ยาว y หน่วย
และลึก z หน่วย โดยที่ x : (y+z) = 1 : 5, z : (x+y) = 2 : 3 และความยาวของบ่อ
ยาวกว่าความลึกอยู่ 6 หน่วย จงหาพื้นที่ก้นบ่อเลี้ยงปลานี้

Three linear conditions in three unknowns, so nothing is left free:

    5x = y + z,      3z = 2(x + y),      y = z + 6

Eliminating gives z = 72, y = 78, x = 30.

**ก้นบ่อ is the floor of the pond**, so the area asked for is width × length =
x·y = **2340** — not x·z, and not any of the side walls. That reading is the
whole difficulty; the algebra is routine.

``solve`` eliminates by hand in exact fractions. ``check`` builds the 3×3 system
and solves it by Gaussian elimination with pivoting, which shares no algebra with
the substitution route.
"""

from __future__ import annotations

from fractions import Fraction

#: x : (y+z) = wn : wd,  z : (x+y) = dn : dd,  and y = z + gap.
PARAMS = {"wn": 1, "wd": 5, "dn": 2, "dd": 3, "gap": 6}
ANSWER = 2340
VARIANTS = [
    {"wn": 1, "wd": 5, "dn": 2, "dd": 3, "gap": 12},
    {"wn": 1, "wd": 4, "dn": 1, "dd": 2, "gap": 6},
    {"wn": 2, "wd": 7, "dn": 3, "dd": 4, "gap": 10},
    {"wn": 1, "wd": 3, "dn": 2, "dd": 5, "gap": 9},
    {"wn": 1, "wd": 5, "dn": 2, "dd": 3, "gap": 5},
    {"wn": 1, "wd": 1, "dn": 1, "dd": 1, "gap": 6},    # degenerate: no pond
]


def solve(wn=1, wd=5, dn=2, dd=3, gap=6):
    """Eliminate to z, then read off x·y."""
    if min(wn, wd, dn, dd) <= 0 or gap <= 0:
        return None
    # 5x = y + z with y = z + gap  ⟹  x = (2z + gap)·wn/wd
    # 3z = 2(x + y)                ⟹  dd·z = dn·(x + y)
    # substituting gives a linear equation in z
    ratio_w = Fraction(wn, wd)
    ratio_d = Fraction(dn, dd)
    # x = ratio_w·(2z + gap);  z = ratio_d·(x + z + gap)
    # z = ratio_d·(ratio_w·(2z+gap) + z + gap)
    coeff = 1 - ratio_d * (2 * ratio_w + 1)
    if coeff == 0:
        return None
    z = ratio_d * ratio_w * gap + ratio_d * gap
    z = z / coeff
    y = z + gap
    x = ratio_w * (2 * z + gap)
    if min(x, y, z) <= 0:
        return None
    area = x * y
    return int(area) if area.denominator == 1 else area


def check(wn=1, wd=5, dn=2, dd=3, gap=6):
    """Independent: solve the 3×3 system by Gaussian elimination.

    The three printed conditions go in as rows of a matrix — no substitution
    order is chosen in advance — and the solver pivots its way to (x, y, z). The
    floor area is then measured from the dimensions it returns.
    """
    if min(wn, wd, dn, dd) <= 0 or gap <= 0:
        return None
    #  wd·x −  wn·y −  wn·z = 0
    # −dn·x −  dn·y +  dd·z = 0
    #        1·y  −   1·z   = gap
    rows = [
        [Fraction(wd), Fraction(-wn), Fraction(-wn), Fraction(0)],
        [Fraction(-dn), Fraction(-dn), Fraction(dd), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(-1), Fraction(gap)],
    ]
    n = 3
    for col in range(n):
        pivot = next((r for r in range(col, n) if rows[r][col] != 0), None)
        if pivot is None:
            return None
        rows[col], rows[pivot] = rows[pivot], rows[col]
        head = rows[col][col]
        rows[col] = [v / head for v in rows[col]]
        for r in range(n):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[col])]
    x, y, z = (rows[i][n] for i in range(n))
    if min(x, y, z) <= 0:
        return None
    area = x * y
    return int(area) if area.denominator == 1 else area
