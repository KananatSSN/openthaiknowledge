"""ข้อ 18 — ความยาวด้านของลูกบาศก์ที่แนบในกรวย

กรวยตรงอันหนึ่งมีฐานเป็นรูปวงกลมรัศมี 1 หน่วย และมีความสูง 3 หน่วยวัดจากยอดกรวย
ถึงจุดศูนย์กลางของฐาน กำหนดให้รูปทรงสี่เหลี่ยมลูกบาศก์รูปหนึ่งถูกแนบอยู่ภายในกรวย
ตรงอันนี้พอดี (จุดมุมสี่มุมล่างของสี่เหลี่ยมลูกบาศก์อยู่บนฐานกรวยและจุดมุมสี่มุมบนของ
สี่เหลี่ยมลูกบาศก์นี้อยู่บนผิวข้างของกรวย) จงหาความยาวของด้านแต่ละด้านของรูปทรง
สี่เหลี่ยมลูกบาศก์นี้

The cube sits centred on the axis, so its top corners are all at height ``a`` and
all at horizontal distance ``a/√2`` from the axis (half the diagonal of a square
of side a). The cone narrows linearly, from R at the base to 0 at the apex:

    radius at height z = R(1 − z/H)

Putting the top corners on that surface gives one equation:

    a/√2 = R(1 − a/H)   ⟹   a(1/√2 + R/H) = R   ⟹   a = √2·R·H / (H + √2·R)

With R = 1 and H = 3 that is ``3√2/(3 + √2)``, and rationalising,

    a = (9√2 − 6)/7 ≈ **0.9611**

(The bottom corners then sit at radius 0.679 < 1, comfortably inside the base —
that constraint is never the binding one.)

The 1/√2 is the whole item: using ``a`` instead of ``a/√2`` — putting the *edge*
midpoints on the surface rather than the corners — gives 3/4 instead.

``solve`` uses the closed form. ``check`` bisects on the edge length instead:
for each trial cube it builds the eight corners in space, measures how far the
top ones sit outside the cone's surface, and drives that residual to zero — then
asserts the bottom face really is inside the base disc.
"""

from __future__ import annotations

from math import gcd, sqrt

#: base radius and apex-to-base-centre height of the cone.
PARAMS = {"radius": 1, "height": 3}
ANSWER = 0.9611317230511222
TOL = 1e-9
VARIANTS = [
    {"radius": 2, "height": 6},          # everything doubles
    {"radius": 1, "height": 10},
    {"radius": 3, "height": 4},
    {"radius": 5, "height": 5},
    {"radius": 0, "height": 3},          # no cone
    {"radius": 1, "height": 0},
]


def exact_form(radius=1, height=3):
    """(p, q, d, denominator) with a = (p + q√d)/denominator, or None."""
    if radius <= 0 or height <= 0:
        return None
    # a = √2·R·H/(H + √2R) = (√2·R·H(H − √2R))/(H² − 2R²)
    denom = height * height - 2 * radius * radius
    if denom == 0:
        return None
    p = -2 * radius * radius * height
    q = radius * height * height
    d = 2
    common = gcd(gcd(abs(p), abs(q)), abs(denom))
    if common:
        p, q, denom = p // common, q // common, denom // common
    if denom < 0:
        p, q, denom = -p, -q, -denom
    return p, q, d, denom


def solve(radius=1, height=3):
    """a = √2·R·H/(H + √2·R), from the top corners lying on the lateral surface."""
    if radius <= 0 or height <= 0:
        return None
    return sqrt(2) * radius * height / (height + sqrt(2) * radius)


def check(radius=1, height=3):
    """Independent: grow the cube until its top corners touch the cone.

    Each trial edge length is turned into eight explicit corner coordinates; the
    residual is how far a top corner's distance from the axis exceeds the cone's
    radius *at that corner's own height*, computed from the cone's own linear
    profile. Bisecting drives it to zero, and the bottom face is then asserted to
    lie inside the base disc.
    """
    if radius <= 0 or height <= 0:
        return None

    def corners(a: float):
        half = a / 2
        out = []
        for sx in (-1, 1):
            for sy in (-1, 1):
                for z in (0.0, a):
                    out.append((sx * half, sy * half, z))
        return out

    def residual(a: float) -> float:
        worst = -1e18
        for x, y, z in corners(a):
            if z <= 1e-12:
                continue
            allowed = radius * (1 - z / height)
            worst = max(worst, sqrt(x * x + y * y) - allowed)
        return worst

    lo, hi = 1e-9, min(height, 10 * radius + height)
    if residual(lo) > 0 or residual(hi) < 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        if residual(mid) <= 0:
            lo = mid
        else:
            hi = mid
    edge = (lo + hi) / 2

    half = edge / 2
    assert sqrt(2) * half <= radius + 1e-9, "the bottom face escapes the base"
    return edge
