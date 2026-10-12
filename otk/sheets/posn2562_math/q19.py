"""ข้อ 19 — รัศมีของวงกลมแนบในสามเหลี่ยม

กำหนดให้ ABC เป็นรูปสามเหลี่ยมหน้าจั่วที่ AB = AC ให้ D และ E เป็นจุดบนด้าน AB และ
AC ตามลำดับ โดยที่ DE สัมผัสวงกลมแนบในสามเหลี่ยม ABC และขนานกับด้าน BC
ถ้า DE = 20 หน่วย และ BC = 52 หน่วย จงหารัศมีของวงกลมแนบในสามเหลี่ยม

DE is the tangent to the incircle parallel to the base, so it runs across the
top of the circle: the distance from BC to DE is exactly the **diameter** 2r.
Writing k = DE/BC for the similarity ratio of △ADE to △ABC and H for the height
to BC,

    H − kH = 2r        (the gap between the two parallel lines)
    r = area/s = BC·H / (BC + 2L),   L = √((BC/2)² + H²)

Eliminating between them gives ``L = BC(1+k)/(2(1−k))``, hence
``H² = L² − (BC/2)² = BC²k/(1−k)²``, so ``H = BC√k/(1−k)`` and

    r = H(1 − k)/2 = (BC/2)·√k = **√(BC · DE) / 2**

— the inradius is half the geometric mean of the two parallel sides, with the
triangle's height dropping out entirely. For 52 and 20:

    r = √1040/2 = 4√65/2 = **2√65** ≈ 16.1245

(The same geometric mean as ข้อ 6, arrived at along a completely different road.)
The formula needs DE < BC; equality would put the tangent line on the base.

``solve`` uses that closed form. ``check`` reconstructs the triangle: it bisects
on the height until the tangent line parallel to BC at height 2r really does cut
a chord of length DE, computing the inradius each time from area over
semiperimeter.
"""

from __future__ import annotations

from math import isqrt, sqrt

#: the tangent chord parallel to the base, and the base.
PARAMS = {"de": 20, "bc": 52}
ANSWER = 16.124515496597099
TOL = 1e-9
VARIANTS = [
    {"de": 4, "bc": 9},           # a whole number: 3
    {"de": 1, "bc": 4},
    {"de": 9, "bc": 25},
    {"de": 13, "bc": 52},
    {"de": 52, "bc": 20},         # DE longer than BC: impossible
    {"de": 0, "bc": 52},
]


def exact_square(de=20, bc=52):
    """r as a whole number when de·bc is a perfect square of an even number."""
    if de <= 0 or bc <= de:
        return None
    product = de * bc
    root = isqrt(product)
    if root * root != product or root % 2:
        return None
    return root // 2


def solve(de=20, bc=52):
    """r = √(DE·BC)/2 — half the geometric mean of the two parallel sides."""
    if de <= 0 or bc <= de:
        return None
    return sqrt(de * bc) / 2


def check(de=20, bc=52):
    """Independent: rebuild the triangle and cut the tangent chord for real.

    For a trial height the isosceles triangle is laid out in coordinates, its
    inradius comes from area over semiperimeter, and the horizontal line at
    height 2r is intersected with the two equal sides to measure the chord it
    cuts. Bisecting the height until that chord equals DE gives the triangle,
    and the inradius is read off it. No similarity ratio is used anywhere.
    """
    if de <= 0 or bc <= de:
        return None

    def chord(height: float):
        """(inradius, length of the tangent chord parallel to the base)."""
        if height <= 0:
            return None
        side = sqrt((bc / 2) ** 2 + height * height)
        semi = (bc + 2 * side) / 2
        area = bc * height / 2
        r = area / semi
        if 2 * r >= height:
            return None
        # the sides run from (±bc/2, 0) to the apex (0, height)
        width = bc * (1 - 2 * r / height)
        return r, width

    def residual(height: float):
        got = chord(height)
        return None if got is None else got[1] - de

    lo, hi, steps = 1e-6, 20.0 * max(bc, de), 200_000
    found = []
    prev, prev_h = residual(lo), lo
    for i in range(1, steps + 1):
        h = lo + (hi - lo) * i / steps
        cur = residual(h)
        if cur is not None and prev is not None:
            if cur == 0.0:
                found.append(h)
            elif prev * cur < 0:
                left, right = prev_h, h
                for _ in range(200):
                    mid = (left + right) / 2
                    fl, fm = residual(left), residual(mid)
                    if fl is None or fm is None:
                        break
                    if fl * fm <= 0:
                        right = mid
                    else:
                        left = mid
                found.append((left + right) / 2)
        prev, prev_h = cur, h

    radii = []
    for h in found:
        got = chord(h)
        if got is None or abs(got[1] - de) > 1e-6:
            continue
        radii.append(got[0])
    if not radii or max(radii) - min(radii) > 1e-7:
        return None
    return sum(radii) / len(radii)
