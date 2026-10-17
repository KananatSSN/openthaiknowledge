"""ข้อ 6 — BC/BA เมื่อ M กึ่งกลาง BC, ∠MAC = 20° และ ∠ABC มากที่สุด

A runs over an arc through M and C; ∠ABC is largest when BA is tangent to it,
so BA² = BM·BC and BC/BA = √(BC/BM) = √2 (for BM : MC = m : n, √((m + n)/m)).

``check`` scans the locus arc (inscribed angle 20° over MC) for the point with
the largest angle at B and measures BC/BA there.
"""

from __future__ import annotations

import math

PARAMS = {"m": 1, "n": 1}
ANSWER = math.sqrt(2)
TOL = 1e-6
VARIANTS = [{"m": 2, "n": 5}, {"m": 3, "n": 1}, {"m": 4, "n": 3}]


def solve(m=1, n=1):
    return math.sqrt((m + n) / m)


def check(m=1, n=1):
    bm, bc = m, m + n
    cx, cy = (bm + bc) / 2, (n / 2) / math.tan(math.radians(20))
    rad = math.hypot(n / 2, cy)
    low = math.atan2(-cy, n / 2)

    def angle(th):
        return math.atan2(cy + rad * math.sin(th), cx + rad * math.cos(th))

    lo, hi = low, math.pi - low
    for _ in range(300):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if angle(m1) < angle(m2):
            lo = m1
        else:
            hi = m2
    th = (lo + hi) / 2
    return bc / math.hypot(cx + rad * math.cos(th), cy + rad * math.sin(th))
