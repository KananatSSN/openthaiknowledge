"""ข้อ 9 — AB/BC เมื่อ D, E กึ่งกลาง BC, AC; P = AD ∩ BE; ∠CAD = 15°, ∠APB = 60°

P is the centroid. With A at the origin, AD = 3 on the x-axis, P = (2, 0), C at
angle α and B = 2D − C, the angle at P gives AC = 4 sin β/sin(β − α); then
AB² = 36 − 12·AC cos α + AC² and BC² = 36 − 24·AC cos α + 4AC², so
AB/BC = √((4 − √3)/13).

``check`` bisects on AC until the measured angle APB equals β.
"""

from __future__ import annotations

import math

PARAMS = {"alpha": 15, "beta": 60}
ANSWER = math.sqrt((4 - math.sqrt(3)) / 13)
TOL = 1e-9
VARIANTS = [{"alpha": 30, "beta": 90}, {"alpha": 45, "beta": 135}, {"alpha": 30, "beta": 75}]


def solve(alpha=15, beta=60):
    al, be = math.radians(alpha), math.radians(beta)
    ac = 4 * math.sin(be) / math.sin(be - al)
    ab2 = 36 - 12 * ac * math.cos(al) + ac * ac
    bc2 = 36 - 24 * ac * math.cos(al) + 4 * ac * ac
    return math.sqrt(ab2 / bc2)


def check(alpha=15, beta=60):
    al = math.radians(alpha)

    def points(t):
        c = (t * math.cos(al), t * math.sin(al))
        b = (6 - c[0], -c[1])
        return b, c

    def angle_p(t):
        b, _ = points(t)
        u, v = (-2.0, 0.0), (b[0] - 2, b[1])
        return math.degrees(math.acos((u[0] * v[0] + u[1] * v[1]) / (2 * math.hypot(*v))))

    lo, hi = 1e-6, 200.0
    for _ in range(300):
        mid = (lo + hi) / 2
        if (angle_p(lo) - beta) * (angle_p(mid) - beta) <= 0:
            hi = mid
        else:
            lo = mid
    b, c = points((lo + hi) / 2)
    return math.hypot(*b) / math.dist(b, c)
