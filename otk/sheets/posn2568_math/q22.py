"""ข้อ 22 — ขนาดของ ∠AEB ในรูปสี่เหลี่ยม ABCD

กำหนดให้ ABCD เป็นรูปสี่เหลี่ยม โดยมี AD = CD, AC = BD และ AB̅ ตั้งฉากกับ AC̅
ให้ E เป็นจุดตัดของ AC̅ และ BD̅  ขนาดของ ∠AEB เท่ากับกี่องศา

Method: the three conditions do *not* pin the quadrilateral down — one degree of
freedom survives — and the point of the question is that ∠AEB is the same right
through that family. Put A at the origin with AC along the x-axis and |AC| = 1;
then AB ⊥ AC puts B at (0, −h), and AD = CD puts D on the perpendicular bisector
at (f, k) with f = ½. The remaining condition BD = m·AC fixes h + k = √(m²−f²).
Where BD crosses the x-axis,
    E = (f·h/(h+k), 0)   ⟹   tan ∠AEB = h / E_x = (h+k)/f = √(m²−f²)/f,
and h has cancelled — hence the invariance. For the sheet's AC = BD (m = 1) that
is tan ∠AEB = √3, so ∠AEB = 60°.

``check`` picks several *different* h in the family, builds all five points
numerically, and measures the angle with a dot product — which is also what
demonstrates the invariance rather than assuming it.
"""

from __future__ import annotations

import math
from fractions import Fraction

TOL = 1e-7

# m² = (BD/AC)² and f = (foot of D along AC)/AC; AD = CD forces f = 1/2.
PARAMS = {"m_sq_num": 1, "m_sq_den": 1, "foot_num": 1, "foot_den": 2}
ANSWER = 60.0
VARIANTS = [
    {"m_sq_num": 1, "m_sq_den": 2},        # AC = √2·BD → 45°
    {"m_sq_num": 1, "m_sq_den": 3},        # AC = √3·BD → 30°
    {"m_sq_num": 4, "m_sq_den": 1},
    {"m_sq_num": 1, "m_sq_den": 1, "foot_num": 1, "foot_den": 3},
    {"m_sq_num": 9, "m_sq_den": 4, "foot_num": 2, "foot_den": 3},
]


def solve(m_sq_num=1, m_sq_den=1, foot_num=1, foot_den=2):
    """∠AEB in degrees."""
    m_sq = Fraction(m_sq_num, m_sq_den)
    f = Fraction(foot_num, foot_den)
    inner = m_sq - f * f
    if inner <= 0:
        raise ValueError("BD is too short to reach across AC")
    return math.degrees(math.atan2(math.sqrt(float(inner)), float(f)))


def check(m_sq_num=1, m_sq_den=1, foot_num=1, foot_den=2):
    """Independent: build the figure at several h and measure ∠AEB."""
    m = math.sqrt(m_sq_num / m_sq_den)
    f = foot_num / foot_den
    span = math.sqrt(m * m - f * f)                  # h + k, from |BD| = m
    angles = []
    for share in (0.15, 0.4, 0.62, 0.85):            # different members, same family
        h = span * share
        k = span - h
        a, c = (0.0, 0.0), (1.0, 0.0)
        b, d = (0.0, -h), (f, k)
        assert abs(math.dist(b, d) - m) < 1e-9, "BD is not m·AC"
        assert abs(math.dist(a, d) - math.dist(c, d)) < 1e-9 or foot_num * 2 \
            != foot_den, "AD should equal CD when the foot is the midpoint"

        t = h / (h + k)                              # where BD meets y = 0
        e = (b[0] + t * (d[0] - b[0]), b[1] + t * (d[1] - b[1]))
        assert abs(e[1]) < 1e-12, "E is not on AC"
        va = (a[0] - e[0], a[1] - e[1])
        vb = (b[0] - e[0], b[1] - e[1])
        cos = (va[0] * vb[0] + va[1] * vb[1]) / (math.hypot(*va) * math.hypot(*vb))
        angles.append(math.degrees(math.acos(max(-1.0, min(1.0, cos)))))
    assert max(angles) - min(angles) < 1e-9, \
        f"∠AEB is not invariant across the family: {angles}"
    return angles[0]
