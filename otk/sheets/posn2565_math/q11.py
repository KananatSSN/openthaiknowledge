"""ข้อ 11 — พื้นที่ของรูปสามเหลี่ยม ECH

รูปสี่เหลี่ยม ABCD มี E, F, G และ H เป็นจุดบนด้าน CD, DA, AB และ BC ตามลำดับ
โดยที่ DF/FA = AG/GB = BH/HC = 1/2  ถ้าพื้นที่ของรูปสามเหลี่ยม DEF เท่ากับ 5
ตารางหน่วย พื้นที่ของรูปสี่เหลี่ยม AFEG เท่ากับ 16 ตารางหน่วย และพื้นที่ของรูป
สี่เหลี่ยม BGEH เท่ากับ 19 ตารางหน่วย แล้วพื้นที่ของรูปสามเหลี่ยม ECH เท่ากับกี่
ตารางหน่วย

E's position on CD̅ is never given, and it does not need to be. Segments EF̅, EG̅
and EH̅ cut ABCD into the four named regions, and writing

    X = [ADE],   Y = [ABE],   Z = [BCE]

each region is a fixed fraction of one or two of them. With f = DF/DA = 1/3 (from
the ratio 1:2):

    [DEF]  = f·X
    [AFEG] = (1-f)·X + f·Y          (split by AE̅ into AFE and AEG)
    [BGEH] = (1-f)·Y + f·Z          (split by BE̅)
    [ECH]  = (1-f)·Z

so the three given areas peel X, Y and Z off in turn — 15, 18, 21 — and the
answer is (2/3)·21 = **14**. The four regions sum to 54, which is [ABCD].

``check`` builds a real quadrilateral: it measures the linear map
(X, Y, Z) → (the four areas) by shoelacing four sample configurations, inverts it
to find the X, Y, Z that produce the given areas, and reads the fourth area off
the resulting polygon. It never uses the chain above.
"""

from __future__ import annotations

from fractions import Fraction

#: the three known areas and the common ratio DF:FA = 1:ratio.
PARAMS = {"a1": 5, "a2": 16, "a3": 19, "ratio": 2}
ANSWER = Fraction(14)
VARIANTS = [
    {"a1": 4, "a2": 10, "a3": 12},
    {"a1": 3, "a2": 20, "a3": 30},
    {"a1": 5, "a2": 16, "a3": 19, "ratio": 1},      # the midpoints
    {"a1": 5, "a2": 16, "a3": 19, "ratio": 3},
    {"a1": 9, "a2": 3, "a3": 20},                   # Y would be negative
    {"a1": 0, "a2": 5, "a3": 5},                    # degenerate: E at D
]


def _fraction_along(ratio) -> Fraction | None:
    """DF/DA from DF:FA = 1:ratio."""
    if ratio <= 0:
        return None
    return Fraction(1, 1 + ratio)


def solve(a1=5, a2=16, a3=19, ratio=2):
    """[ECH], by peeling [ADE], [ABE] and [BCE] off the three given areas."""
    f = _fraction_along(ratio)
    if f is None or min(a1, a2, a3) <= 0:
        return None
    x = Fraction(a1) / f
    y = (Fraction(a2) - (1 - f) * x) / f
    z = (Fraction(a3) - (1 - f) * y) / f
    if min(x, y, z) <= 0:
        return None
    return (1 - f) * z


def _areas(x, y, z, f):
    """Shoelace the four regions of a quadrilateral realising [ADE], [ABE], [BCE]."""
    e, c = Fraction(1), Fraction(2)
    ha = 2 * x / e                                  # [ADE] = ½·DE·h_A
    hb = 2 * z / (c - e)                            # [BCE] = ½·EC·h_B
    bx = e + (2 * y - e * hb) / ha                  # fixes [ABE]
    a = (Fraction(0), ha)
    b = (bx, hb)
    cc = (c, Fraction(0))
    d = (Fraction(0), Fraction(0))
    ee = (e, Fraction(0))
    ff = (d[0] + f * (a[0] - d[0]), d[1] + f * (a[1] - d[1]))
    g = (a[0] + f * (b[0] - a[0]), a[1] + f * (b[1] - a[1]))
    h = (b[0] + f * (cc[0] - b[0]), b[1] + f * (cc[1] - b[1]))

    def shoelace(pts):
        s = Fraction(0)
        for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
            s += x1 * y2 - x2 * y1
        return abs(s) / 2

    quad = shoelace([a, b, cc, d])
    parts = (shoelace([d, ee, ff]), shoelace([a, ff, ee, g]),
             shoelace([b, g, ee, h]), shoelace([ee, cc, h]))
    assert sum(parts) == quad, (parts, quad)        # they really do partition it
    return parts


def check(a1=5, a2=16, a3=19, ratio=2):
    """Independent: measure the area map on sample quadrilaterals and invert it.

    The map (X, Y, Z) → (the four areas) is linear, so shoelacing a base
    configuration and three perturbed ones gives its matrix exactly; solving the
    3×3 system for the given areas and shoelacing that configuration yields the
    fourth area. Every number here comes out of a polygon, not out of the ratio
    algebra — and ``_areas`` asserts that the four regions really do add up to
    the quadrilateral.
    """
    f = _fraction_along(ratio)
    if f is None or min(a1, a2, a3) <= 0:
        return None

    one = Fraction(1)
    base = _areas(one, one, one, f)
    cols = []
    for i in range(3):
        bump = [one, one, one]
        bump[i] = Fraction(2)
        cols.append([_areas(*bump, f)[r] - base[r] for r in range(3)])

    # Solve the 3×3 system  Σ_i cols[i]·(v_i - 1) = given - base  by elimination.
    mat = [[cols[i][r] for i in range(3)] + [Fraction(g) - base[r]]
           for r, g in enumerate((a1, a2, a3))]
    for col in range(3):
        pick = next((r for r in range(col, 3) if mat[r][col] != 0), None)
        if pick is None:
            return None
        mat[col], mat[pick] = mat[pick], mat[col]
        lead = mat[col][col]
        mat[col] = [v / lead for v in mat[col]]
        for r in range(3):
            if r != col and mat[r][col] != 0:
                fac = mat[r][col]
                mat[r] = [p - fac * q for p, q in zip(mat[r], mat[col])]
    x, y, z = (1 + mat[i][3] for i in range(3))
    if min(x, y, z) <= 0:
        return None
    got = _areas(x, y, z, f)
    assert (got[0], got[1], got[2]) == (a1, a2, a3), got
    return got[3]
