"""ข้อ 1 — ขา AD ของรูปสี่เหลี่ยมคางหมูแนบในวงกลมรัศมี 1 ที่ AB เป็นเส้นผ่านศูนย์กลาง, DC = 4AD

With A = (−1, 0), B = (1, 0), D = (−c, s), C = (c, s): AD² = 2 − 2c and
DC = 2c = k·AD, so AD² + k·AD − 2 = 0 and AD = (√(k² + 8) − k)/2 = √6 − 2.

``check`` bisects on c for 2c = k·√(2 − 2c) and measures AD.
"""

from __future__ import annotations

import math

PARAMS = {"k": 4}
ANSWER = math.sqrt(6) - 2
VARIANTS = [{"k": 1}, {"k": 2}, {"k": 7}, {"k": 9}]


def solve(k=4):
    return (math.sqrt(k * k + 8) - k) / 2


def check(k=4):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        c = (lo + hi) / 2
        if 2 * c - k * math.sqrt(2 - 2 * c) > 0:
            hi = c
        else:
            lo = c
    return math.sqrt(2 - 2 * lo)
