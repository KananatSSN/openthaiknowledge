"""ข้อ 7 — พื้นที่ของรูปห้าเหลี่ยม ABCDE จากมุมที่กำหนด

จากรูป กำหนด ABCE เป็นรูปสี่เหลี่ยมรูปหนึ่ง ที่มีด้าน AB ยาว 4 หน่วย ด้าน BC ยาวไม่เกิน
4 หน่วย และ △CDE เป็นรูปสามเหลี่ยมรูปหนึ่ง จงหาพื้นที่ของรูปห้าเหลี่ยม ABCDE

**The trap is reading "BC ยาวไม่เกิน 4" as a missing constant.** It is not: the
pentagon's area does not depend on BC at all. Building the figure at BC = 1, 2, 3
and 4 gives 8 every time. The inequality is there to say the picture closes as
drawn, nothing more.

What the figure supplies, and the text does not:

* ∠EAB = 45° at A, ∠ABC = 90° at B, ∠BCE = 125° and ∠ECD = 80° at C;
* at E the 25° is measured from ED to the **extension of AE**, so going along the
  straight line A–E–(dashed) the three angles ∠AEC, ∠CED and 25° add to 180°.

That fixes the rest: ∠AEC = 360 − 45 − 90 − 125 = 100° (angle sum of the
quadrilateral ABCE), hence ∠CED = 180 − 100 − 25 = 55°, and ∠CDE = 180 − 80 − 55
= 45°. With AB = 4 the whole pentagon is then determined up to the free length
BC — and its area, **8**, is not.

``solve`` exploits the invariance by evaluating the one case where the figure is
cheapest: BC = 0, where C collapses onto B and the pentagon becomes the
quadrilateral ABDE. ``check`` refuses that shortcut — it builds the full
five-vertex figure at several genuinely different BC and reports the area only
when they all agree, which is what turns the invariance from an assumption into
a measurement.
"""

from __future__ import annotations

from fractions import Fraction
from math import cos, radians, sin

#: all angles in degrees, as read off the figure.
PARAMS = {"ab": 4, "angle_a": 45, "angle_b": 90, "angle_c": 125,
          "angle_dce": 80, "angle_e_out": 25}
ANSWER = 8
TOL = 1e-7
VARIANTS = [
    {"ab": 6},
    {"angle_a": 30},
    {"angle_b": 80, "angle_c": 130},
    {"angle_dce": 70, "angle_e_out": 30},
    {"ab": 5, "angle_a": 60, "angle_b": 75},
    {"angle_c": 200},                       # angles no longer close a figure
]


def _build(bc, ab, angle_a, angle_b, angle_c, angle_dce, angle_e_out):
    """The five vertices, with A at the origin and AE along the +x axis."""
    aec = 360 - angle_a - angle_b - angle_c          # quadrilateral angle sum
    ced = 180 - aec - angle_e_out                    # A, E and the dashed ray are collinear
    cde = 180 - angle_dce - ced
    if min(aec, ced, cde) <= 0:
        return None

    a = (0.0, 0.0)
    b = (ab * cos(radians(angle_a)), ab * sin(radians(angle_a)))
    dir_bc = angle_a + 180 + angle_b
    c = (b[0] + bc * cos(radians(dir_bc)), b[1] + bc * sin(radians(dir_bc)))
    dir_ce = dir_bc + 180 + angle_c
    down = sin(radians(dir_ce))
    if abs(down) < 1e-12:
        return None
    ce = -c[1] / down                                # E is on the x-axis
    if ce <= 0:
        return None
    e = (c[0] + ce * cos(radians(dir_ce)), 0.0)
    ed = ce * sin(radians(angle_dce)) / sin(radians(cde))
    d = (e[0] + ed * cos(radians(angle_e_out)),
         e[1] + ed * sin(radians(angle_e_out)))
    return [a, b, c, d, e]


def _signed(points) -> float:
    total = 0.0
    for i, (x0, y0) in enumerate(points):
        x1, y1 = points[(i + 1) % len(points)]
        total += x0 * y1 - x1 * y0
    return total / 2


def _shoelace(points) -> float:
    return abs(_signed(points))


def _snap(value: float):
    if abs(value - round(value)) < 1e-7:
        return int(round(value))
    close = Fraction(value).limit_denominator(64)
    return close if abs(float(close) - value) < 1e-7 else value


def solve(ab=4, angle_a=45, angle_b=90, angle_c=125, angle_dce=80,
          angle_e_out=25):
    """Identify the area as a quadratic in BC, and read off its constant term.

    Every vertex moves *linearly* with BC — C by construction, E because it is
    where a fixed-direction ray from C meets the x-axis, D because it hangs off E
    at a fixed angle and a fixed multiple of CE — so the shoelace area is exactly
    a quadratic in BC. Three evaluations therefore determine it outright. The
    question is only well posed when the two leading coefficients vanish, which
    is the sheet's own case; otherwise "the area" is not a number and this
    returns None.
    """
    if ab <= 0:
        return None
    ys = []
    for t in (0.0, 1.0, 2.0):
        points = _build(t, ab, angle_a, angle_b, angle_c, angle_dce,
                        angle_e_out)
        if points is None:
            return None
        ys.append(_signed(points))
    constant = ys[0]
    linear = (4 * ys[1] - 3 * ys[0] - ys[2]) / 2       # q'(0)
    quadratic = (ys[2] - 2 * ys[1] + ys[0]) / 2        # q''(0)/2
    scale = max(1.0, abs(constant))
    if abs(linear) > 1e-9 * scale or abs(quadratic) > 1e-9 * scale:
        return None
    return _snap(abs(constant))


def check(ab=4, angle_a=45, angle_b=90, angle_c=125, angle_dce=80,
          angle_e_out=25):
    """Independent: build the full pentagon at several BC and require agreement.

    Nothing here assumes the area is invariant — that is the thing being tested.
    Four genuinely different BC are used, each producing five distinct vertices,
    and a value is returned only if the four shoelace areas match.
    """
    if ab <= 0:
        return None
    # BC is bounded above by the draw that puts C on the line AE; sample well
    # inside that range rather than at fixed lengths, which degenerate.
    drop = sin(radians(angle_a + 180 + angle_b))
    if drop >= 0:
        return None
    ceiling = ab * sin(radians(angle_a)) / -drop
    areas = []
    for share in (0.15, 0.35, 0.55, 0.75):
        points = _build(ceiling * share, ab, angle_a, angle_b, angle_c,
                        angle_dce, angle_e_out)
        if points is None:
            return None
        areas.append(_shoelace(points))
    if max(areas) - min(areas) > 1e-7 * max(1.0, max(areas)):
        return None
    return _snap(sum(areas) / len(areas))
