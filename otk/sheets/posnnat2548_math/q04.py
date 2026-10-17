"""ข้อ 4 — BO·OC เมื่อ BC เป็นเส้นผ่านศูนย์กลาง, AB = 3, AC = 4, O จุดศูนย์กลางวงกลมแนบใน

BC is a diameter, so A = 90°, BC = 5 and r = (3 + 4 − 5)/2 = 1. ∠BOC =
90° + A/2 = 135°, and the area of BOC is r·BC/2 = BO·OC·sin 135°/2, so
BO·OC = √2·r·BC = 5√2.

``check`` places the right angle at the origin, finds the incentre as the
side-weighted average of the vertices, and multiplies the two distances.
"""

from __future__ import annotations

import math

PARAMS = {"ab": 3, "ac": 4}
ANSWER = 5 * math.sqrt(2)
VARIANTS = [{"ab": 5, "ac": 12}, {"ab": 8, "ac": 15}, {"ab": 1, "ac": 1}, {"ab": 2, "ac": 7}]


def solve(ab=3, ac=4):
    bc = math.hypot(ab, ac)
    r = (ab + ac - bc) / 2
    return math.sqrt(2) * r * bc


def check(ab=3, ac=4):
    a, b, c = (0.0, 0.0), (float(ab), 0.0), (0.0, float(ac))
    la, lb, lc = math.dist(b, c), math.dist(a, c), math.dist(a, b)
    total = la + lb + lc
    o = ((la * a[0] + lb * b[0] + lc * c[0]) / total, (la * a[1] + lb * b[1] + lc * c[1]) / total)
    return math.dist(o, b) * math.dist(o, c)
