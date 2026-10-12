"""ข้อ 21 — อัตราส่วน BO : BD เมื่อ BO ต่อไปตัดวงกลมล้อมรอบที่ P

กำหนดให้วงกลมแนบในรูปสามเหลี่ยม ABC มีจุด O เป็นจุดศูนย์กลาง และสัมผัสด้าน AB
ที่จุด D ลากเส้นจากจุด B ผ่านจุด O ไปตัดวงกลมล้อมรอบรูปสามเหลี่ยม ABC ที่จุด P
ถ้า AC = 15 หน่วย และ AP = 9 หน่วย แล้ว อัตราส่วน BO : BD มีค่าเท่าใด

Two independent facts meet here, and neither needs the triangle's shape.

**The ratio itself is a single cosine.** OD ⊥ AB with O the incenter, so in the
right triangle BDO the angle at B is half of ∠ABC:

    BD = r·cot(B/2),   BO = r/sin(B/2)   ⟹   BO : BD = 1 : cos(B/2)

**And the two given lengths are chords of the circumcircle** subtending exactly
those angles. BP passes through the incenter, so it bisects ∠ABC; the inscribed
angle ∠ABP = B/2 stands on AP, and ∠ABC = B stands on AC. By the extended law of
sines,

    AC/AP = sin B / sin(B/2) = 2·cos(B/2)

So BO : BD = 2·AP : AC = 18 : 15 = **6 : 5** — the incircle's radius, the
triangle's sides and the angle B all cancel.

``solve`` returns 2·AP/AC. ``check`` builds triangles: it sweeps the apex until
the *measured* AC : AP matches, then computes the incenter, the touch point on
AB and the second crossing of line BO with the circumcircle, and measures the
ratio directly.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: the two printed chord lengths.
PARAMS = {"ac": 15, "ap": 9}
ANSWER = Fraction(6, 5)
TOL = 1e-6
VARIANTS = [
    {"ac": 16, "ap": 10},
    {"ac": 10, "ap": 6},
    {"ac": 24, "ap": 13},
    {"ac": 20, "ap": 11},
    {"ac": 15, "ap": 20},      # AP > AC needs cos(B/2) > 1: impossible
    {"ac": 12, "ap": 7},
]


def solve(ac=15, ap=9):
    """BO : BD = 1/cos(B/2) = 2·AP/AC."""
    if ac <= 0 or ap <= 0:
        return None
    ratio = Fraction(2 * ap, ac)
    if ratio <= 1:
        return None            # cos(B/2) ≤ 1 forces 2·AP ≥ AC, strictly
    return ratio


def _measure(beta, arm):
    """Build the figure with ∠ABC = beta and BA of length `arm`.

    Parametrising by the angle at B directly is what makes the sweep reach every
    achievable AC : AP — the ratio depends on that angle alone, so sweeping an
    apex along some arbitrary ray would only cover part of the range.
    """
    if not 0 < beta < math.pi:
        return None
    a = (arm * math.cos(beta), arm * math.sin(beta))
    b = (0.0, 0.0)
    c = (1.0, 0.0)

    dist = lambda p, q: math.hypot(p[0] - q[0], p[1] - q[1])   # noqa: E731
    side_a, side_b, side_c = dist(b, c), dist(a, c), dist(a, b)
    total = side_a + side_b + side_c
    incenter = ((side_a * a[0] + side_b * b[0] + side_c * c[0]) / total,
                (side_a * a[1] + side_b * b[1] + side_c * c[1]) / total)

    # D: the foot of the perpendicular from the incenter onto AB
    ux, uy = (b[0] - a[0]) / side_c, (b[1] - a[1]) / side_c
    proj = (incenter[0] - a[0]) * ux + (incenter[1] - a[1]) * uy
    d = (a[0] + proj * ux, a[1] + proj * uy)

    # circumcircle
    det = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    if abs(det) < 1e-12:
        return None
    sq = lambda p: p[0] * p[0] + p[1] * p[1]                    # noqa: E731
    ox = (sq(a) * (b[1] - c[1]) + sq(b) * (c[1] - a[1]) + sq(c) * (a[1] - b[1])) / det
    oy = (sq(a) * (c[0] - b[0]) + sq(b) * (a[0] - c[0]) + sq(c) * (b[0] - a[0])) / det
    centre = (ox, oy)
    radius = dist(a, centre)

    # P: the far crossing of the ray B → incenter with the circumcircle
    step = dist(b, incenter)
    if step < 1e-12:
        return None
    dx, dy = (incenter[0] - b[0]) / step, (incenter[1] - b[1]) / step
    fx, fy = b[0] - centre[0], b[1] - centre[1]
    beta = 2 * (fx * dx + fy * dy)
    gamma = fx * fx + fy * fy - radius * radius
    disc = beta * beta - 4 * gamma
    if disc < 0:
        return None
    t = max((-beta - math.sqrt(disc)) / 2, (-beta + math.sqrt(disc)) / 2)
    p = (b[0] + t * dx, b[1] + t * dy)

    bd = dist(b, d)
    if bd < 1e-12 or dist(a, p) < 1e-12:
        return None
    return side_b / dist(a, p), dist(b, incenter) / bd


def check(ac=15, ap=9):
    """Independent: sweep the apex until AC : AP matches, then measure BO : BD.

    Everything is coordinates — incenter from the side-length weights, D as a
    foot of a perpendicular, P as a line-circle intersection. The claim that
    BO : BD is 2·AP : AC is what is being tested, so it appears nowhere here.
    """
    if ac <= 0 or ap <= 0:
        return None
    wanted = ac / ap

    #: two unrelated arm lengths, so shape-independence is tested, not assumed
    results = []
    for arm in (0.8, 1.7):
        def residual(beta, arm=arm):
            got = _measure(beta, arm)
            return None if got is None else got[0] - wanted

        previous = None
        steps = 4000
        lo = hi = None
        for i in range(1, steps):
            beta = math.pi * i / steps
            value = residual(beta)
            if value is None:
                previous = None
                continue
            if value == 0.0:
                lo = hi = beta
                break
            if previous is not None and previous[1] * value < 0:
                lo, hi = previous[0], beta
                break
            previous = (beta, value)
        if lo is None:
            return None

        for _ in range(200):
            mid = (lo + hi) / 2
            a_mid, a_lo = residual(mid), residual(lo)
            if a_mid is None or a_lo is None:
                return None
            if a_mid * a_lo <= 0:
                hi = mid
            else:
                lo = mid
        got = _measure((lo + hi) / 2, arm)
        if got is None:
            return None
        results.append(got[1])

    if abs(results[0] - results[1]) > 1e-6 * max(1.0, results[0]):
        return None                # the ratio must not depend on the shape
    return results[0]
