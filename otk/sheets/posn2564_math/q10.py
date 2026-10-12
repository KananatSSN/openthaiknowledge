"""ข้อ 10 — ความยาว PR เมื่อเส้นสัมผัสร่วมตัด O₁O₂ ที่ R

จากรูป กำหนดให้เส้นตรง ℓ สัมผัสกับวงกลมสองวงที่มีจุดศูนย์กลางเป็น O₁ และ O₂
ที่จุด P และ Q ตามลำดับ ให้ O₁O₂ ตัดกับ PQ ที่จุด R
ถ้า PR : RQ = 3 : 4, QO₂ = 12 หน่วย และ O₁O₂ = 28 หน่วย แล้วจงหาความยาว PR

The drawing shows the **internal** tangent — it crosses between the two circles —
and that is what makes R lie inside the segment O₁O₂. Then △O₁PR and △O₂QR are
similar: both have a right angle at the point of tangency, and the angles at R
are vertical. So all three pairs of sides share the ratio 3 : 4:

    O₁P = QO₂·3/4 = 9,   O₁R = 28·3/7 = 12,   O₂R = 16

and Pythagoras in △O₁PR gives PR = √(12² − 9²) = √63 = **3√7**.

The cross-check is free: QR = √(16² − 12²) = 4√7, and PR : QR is 3 : 4 as
printed — so the configuration is consistent rather than over-determined.

``solve`` follows that similarity. ``check`` puts the two circles on an axis and
solves for the internal tangent line directly from the tangency distances, with
no similar triangles anywhere.
"""

from __future__ import annotations

import math

#: PR : RQ = p : q, with the far radius and the centre distance given.
PARAMS = {"p": 3, "q": 4, "qo2": 12, "o1o2": 28}
ANSWER = math.sqrt(63)
TOL = 1e-7
VARIANTS = [
    {"p": 1, "q": 1, "qo2": 10, "o1o2": 26},
    {"p": 3, "q": 5, "qo2": 15, "o1o2": 32},
    {"p": 2, "q": 3, "qo2": 9, "o1o2": 20},
    {"p": 4, "q": 3, "qo2": 6, "o1o2": 25},
    {"p": 3, "q": 4, "qo2": 12, "o1o2": 20},   # radii too big: no tangent
    {"p": 5, "q": 6, "qo2": 18, "o1o2": 40},
]


def solve(p=3, q=4, qo2=12, o1o2=28):
    """√(O₁R² − O₁P²) with both taken from the p : q similarity."""
    if min(p, q, qo2, o1o2) <= 0:
        return None
    r1 = qo2 * p / q
    o1r = o1o2 * p / (p + q)
    if o1r <= r1:
        return None            # the tangent point would not exist
    if o1o2 <= r1 + qo2:
        return None            # circles overlap: no internal tangent
    return math.sqrt(o1r * o1r - r1 * r1)


def check(p=3, q=4, qo2=12, o1o2=28):
    """Independent: build the internal tangent from its distances to the centres.

    O₁ sits at the origin and O₂ at (d, 0). A line is internally tangent when
    its (signed) distances to the two centres are the radii with *opposite*
    signs; solving that pair of equations gives the line, and P, Q, R are then
    the foot of each perpendicular and the crossing with the axis. The printed
    ratio is checked against the built figure rather than used to build it.
    """
    if min(p, q, qo2, o1o2) <= 0:
        return None
    r1 = qo2 * p / q
    r2 = float(qo2)
    d = float(o1o2)
    if d <= r1 + r2:
        return None

    # line: x·cosθ + y·sinθ = c, distance to O₁ is |c| = r1 and to O₂ is
    # |d·cosθ − c| = r2 with the opposite sign ⟹ d·cosθ = c − r2 = r1 − r2
    cos_t = (r1 + r2) / d
    if abs(cos_t) >= 1:
        return None
    sin_t = math.sqrt(1 - cos_t * cos_t)
    c = r1
    o1 = (0.0, 0.0)
    o2 = (d, 0.0)
    # feet of the perpendiculars from each centre onto the line
    def foot(pt):
        gap = pt[0] * cos_t + pt[1] * sin_t - c
        return (pt[0] - gap * cos_t, pt[1] - gap * sin_t)
    pp, qq = foot(o1), foot(o2)
    if abs(math.hypot(*pp) - r1) > 1e-9 or abs(math.hypot(qq[0] - d, qq[1]) - r2) > 1e-9:
        return None
    # R is where PQ crosses the axis O₁O₂ (the x-axis)
    if abs(qq[1] - pp[1]) < 1e-12:
        return None
    t = (0.0 - pp[1]) / (qq[1] - pp[1])
    r = (pp[0] + t * (qq[0] - pp[0]), 0.0)
    if not 0 < r[0] < d:
        return None                    # R must fall between the centres
    pr = math.hypot(pp[0] - r[0], pp[1] - r[1])
    rq = math.hypot(qq[0] - r[0], qq[1] - r[1])
    if abs(pr / rq - p / q) > 1e-7:
        return None                    # the built figure must match the ratio
    return pr
