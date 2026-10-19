"""ข้อ 2 — AB เมื่อ ABCD แนบในวงกลม ส่วนโค้ง AB = ส่วนโค้ง BC, AD = 6, BD = 4, CD = 1

DB bisects ∠ADC; the law of cosines in ABD and CBD with AB = BC gives
cos∠ADB = (AD + CD)/(2BD) and AB² = BD² − AD·CD = 10, so AB = √10.

``check`` puts D at the origin with DB on the x-axis, A and C at angles ±θ, and
bisects on θ until A, B, C, D are concyclic; then it measures AB.
"""

from __future__ import annotations

import math

PARAMS = {"ad": 6, "bd": 4, "cd": 1}
ANSWER = math.sqrt(10)
TOL = 1e-8
VARIANTS = [{"ad": 5, "bd": 8, "cd": 1}, {"ad": 3, "bd": 3, "cd": 2}, {"ad": 7, "bd": 6, "cd": 4}]


def solve(ad=6, bd=4, cd=1):
    return math.sqrt(bd * bd - ad * cd)


def check(ad=6, bd=4, cd=1):
    b = (float(bd), 0.0)

    def concyclic_gap(theta):
        a = (ad * math.cos(theta), ad * math.sin(theta))
        c = (cd * math.cos(theta), -cd * math.sin(theta))
        # circle through D = (0, 0), A, C: x² + y² + ex + fy = 0
        m = [[a[0], a[1]], [c[0], c[1]]]
        r = [-(a[0] ** 2 + a[1] ** 2), -(c[0] ** 2 + c[1] ** 2)]
        det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
        e = (r[0] * m[1][1] - m[0][1] * r[1]) / det
        return b[0] ** 2 + e * b[0]  # power of B (f·0 drops out)

    lo, hi = 1e-6, math.pi / 2 - 1e-6
    for _ in range(200):
        mid = (lo + hi) / 2
        if (concyclic_gap(lo) < 0) == (concyclic_gap(mid) < 0):
            lo = mid
        else:
            hi = mid
    theta = (lo + hi) / 2
    return math.dist((ad * math.cos(theta), ad * math.sin(theta)), b)
