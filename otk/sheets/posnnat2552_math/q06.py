"""ข้อ 6 — [DEF]/[ABC] เมื่อ DE เป็นเส้นผ่านศูนย์กลางวงกลมแนบใน และ F = AE ∩ BC

The homothety at A taking the incircle to the excircle sends E to the extouch
point, so F is it: BF = s − c, BD = s − b, DF = c − b. Triangle DEF is right at
D with legs 2r and c − b, and [ABC] = rs: the ratio is 2(c − b)/(a + b + c).
PARAMS fixes a = BC = 7, b = CA = 5, c = AB = 8: 3/10.

``check`` builds the triangle, its incircle, the antipode E, F = AE ∩ BC, and
divides the shoelace areas.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"a": 7, "b": 5, "c": 8}
ANSWER = Fraction(3, 10)
TOL = 1e-9
VARIANTS = [{"a": 5, "b": 4, "c": 6}, {"a": 9, "b": 7, "c": 12}, {"a": 13, "b": 5, "c": 12}]


def solve(a=7, b=5, c=8):
    return Fraction(2 * (c - b), a + b + c)


def check(a=7, b=5, c=8):
    bp, cp = (0.0, 0.0), (float(a), 0.0)
    x = (c * c - b * b + a * a) / (2 * a)
    ap = (x, math.sqrt(c * c - x * x))
    s = (a + b + c) / 2
    area = a * ap[1] / 2
    r = area / s
    d = (s - b, 0.0)
    e = (d[0], 2 * r)
    # F = A + t(E − A) on y = 0
    t = ap[1] / (ap[1] - e[1])
    f = (ap[0] + t * (e[0] - ap[0]), 0.0)

    def tri(p, q, w):
        return abs((q[0] - p[0]) * (w[1] - p[1]) - (q[1] - p[1]) * (w[0] - p[0])) / 2

    return tri(d, e, f) / tri(ap, bp, cp)
