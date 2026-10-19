"""ข้อ 1 — ∠ADO เมื่อ ∠B = 70°, ∠C = 50° และเส้นแบ่งครึ่งมุม A ตัดวงกลมล้อมที่ D

D is the midpoint of arc BC, so OD ⟂ BC and OA = OD makes ∠ADO = ∠OAD;
∠BAO = 90° − C and ∠BAD = A/2 give ∠OAD = |B − C|/2 = 10°.

``check`` places A, B, C, D on the unit circle by central angles and measures.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"angle_b": 70, "angle_c": 50}
ANSWER = 10
VARIANTS = [{"angle_b": 43, "angle_c": 71}, {"angle_b": 80, "angle_c": 40}, {"angle_b": 55, "angle_c": 85}, {"angle_c": 70}]


def solve(angle_b=70, angle_c=50):
    return Fraction(abs(angle_b - angle_c), 2)


def check(angle_b=70, angle_c=50):
    a_, c_ = math.radians(180 - angle_b - angle_c), math.radians(angle_c)

    def pt(t):
        return (math.cos(t), math.sin(t))

    a, d = pt(0.0), pt(2 * c_ + a_)  # arc AB = 2C, arc BC = 2A; D bisects arc BC
    v, w = (a[0] - d[0], a[1] - d[1]), (-d[0], -d[1])
    cos_angle = (v[0] * w[0] + v[1] * w[1]) / (math.hypot(*v) * math.hypot(*w))
    return math.degrees(math.acos(max(-1.0, min(1.0, cos_angle))))
