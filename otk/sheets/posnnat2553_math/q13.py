"""วันที่สอง ข้อ 3 — (AB + AC)/BC = DE/MN + 1  (พิสูจน์)

Reflecting A in the bisector at B lands on BC, so D is the midpoint of A and
its reflection: D lies on the midline MN with MD = MA = c/2; likewise NE = b/2.
So DE = (b + c − a)/2 and MN = a/2. The solver returns DE (a, b, c = BC, CA, AB
= 5, 6, 4: 5/2).

``check`` builds the triangle, drops the perpendiculars from A to the two
bisectors and measures DE.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"a": 5, "b": 6, "c": 4}
ANSWER = Fraction(5, 2)
TOL = 1e-9
VARIANTS = [{"a": 7, "b": 9, "c": 5}, {"a": 12, "b": 13, "c": 6}, {"a": 4, "b": 5, "c": 3}]


def solve(a=5, b=6, c=4):
    return Fraction(b + c - a, 2)


def check(a=5, b=6, c=4):
    bp, cp = (0.0, 0.0), (float(a), 0.0)
    x = (c * c - b * b + a * a) / (2 * a)
    ap = (x, math.sqrt(c * c - x * x))

    def foot_on_bisector(vertex, p1, p2):
        u1 = ((p1[0] - vertex[0]) / math.dist(p1, vertex), (p1[1] - vertex[1]) / math.dist(p1, vertex))
        u2 = ((p2[0] - vertex[0]) / math.dist(p2, vertex), (p2[1] - vertex[1]) / math.dist(p2, vertex))
        d = (u1[0] + u2[0], u1[1] + u2[1])
        norm = math.hypot(*d)
        d = (d[0] / norm, d[1] / norm)
        t = (ap[0] - vertex[0]) * d[0] + (ap[1] - vertex[1]) * d[1]
        return (vertex[0] + t * d[0], vertex[1] + t * d[1])

    d_pt = foot_on_bisector(bp, ap, cp)
    e_pt = foot_on_bisector(cp, ap, bp)
    return math.dist(d_pt, e_pt)
