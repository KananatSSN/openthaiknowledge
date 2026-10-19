"""ข้อ 3 — MR = MC เมื่อ ∠BRP = ∠PRC  (พิสูจน์)

With concurrent cevians, RC and RP are harmonic with RA, RB, so RP bisecting
∠BRC makes RQ bisect ∠CRA and ∠PRQ = 90°. With ∠PCQ = 90° too, R and C lie on
the circle with diameter PQ, so MR = MC = PQ/2. The solver returns PQ/2 for
CP, CQ (3, 4: 5/2).

``check`` places C at the origin, P and Q on the legs, and measures MC.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"cp": 3, "cq": 4}
ANSWER = 2.5
TOL = 1e-9
VARIANTS = [{"cp": 5, "cq": 12}, {"cp": 1, "cq": 1}, {"cp": 8, "cq": 15}]


def solve(cp=3, cq=4):
    return math.sqrt(cp * cp + cq * cq) / 2


def check(cp=3, cq=4):
    m = (Fraction(cp, 2), Fraction(cq, 2))
    return math.hypot(float(m[0]), float(m[1]))
