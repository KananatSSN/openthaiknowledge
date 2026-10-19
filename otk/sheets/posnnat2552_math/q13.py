"""วันที่สอง ข้อ 3 — เส้นแบ่งครึ่งมุม ACD ตัดรังสี BA ที่ K: พิสูจน์ BK = AB + AC  (พิสูจน์)

The condition MA·MC + MA·CD = MB·MD forces AB ∥ CD (see the bank note); then
∠AKC = ∠KCD = ∠ACK, so AK = AC and K lies beyond A on ray BA:
BK = AB + AC (AB = 5, AC = 7: 12).

``check`` builds a trapezoid with AB ∥ CD, draws the bisector of ∠ACD, meets it
with line AB and measures BK.
"""

from __future__ import annotations

import math

PARAMS = {"ab": 5, "ac": 7}
ANSWER = 12
TOL = 1e-9
VARIANTS = [{"ab": 3, "ac": 4}, {"ab": 20, "ac": 9}, {"ab": 11, "ac": 30}]


def solve(ab=5, ac=7):
    return ab + ac


def check(ab=5, ac=7):
    h = ac / 2
    a, b = (0.0, h), (float(ab), h)
    c = (math.sqrt(ac * ac - h * h), 0.0)
    u = ((a[0] - c[0]) / ac - 1.0, (a[1] - c[1]) / ac)  # bisector of ∠ACD, CD along −x
    t = (h - c[1]) / u[1]
    k = (c[0] + t * u[0], h)
    assert k[0] < a[0] + 1e-9
    return math.dist(b, k)
