"""ข้อ 2 — r₁/r₂ เมื่อวงกลม O₁, O₂ รัศมีเท่ากันมีคอร์ดร่วม AD, AB = 15, AD = 13, BC = 18

Equal circles give ∠ABD = ∠ACD, so AB = AC. With the altitude h = 12 from A and
its foot at the midpoint of BC (half-base m = 9), D sits e = 5 from the foot:
BD = 14, CD = 4. Both triangles share the height, so r = area/semiperimeter
gives r₁/r₂ = 8/3 (taking BD > DC; the statement is symmetric in B and C).

``check`` builds the points, confirms the circumcircles of ABD and ACD have equal
radii, and divides the inradii.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"h": 12, "m": 9, "e": 5}
ANSWER = Fraction(8, 3)
TOL = 1e-9
VARIANTS = [{"m": 16, "e": 9}, {"m": 35, "e": 16}, {"h": 24, "m": 45, "e": 7}]


def solve(h=12, m=9, e=5):
    ab, ad = math.isqrt(h * h + m * m), math.isqrt(h * h + e * e)
    bd, cd = m + e, m - e
    s1, s2 = Fraction(ab + ad + bd, 2), Fraction(ab + ad + cd, 2)
    return Fraction(bd) / s1 / (Fraction(cd) / s2)


def check(h=12, m=9, e=5):
    a, b, c, d = (0.0, float(h)), (-float(m), 0.0), (float(m), 0.0), (float(e), 0.0)

    def area(p, q, r):
        return abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) / 2

    def inradius(p, q, r):
        return area(p, q, r) / ((math.dist(p, q) + math.dist(q, r) + math.dist(r, p)) / 2)

    def circumradius(p, q, r):
        return math.dist(p, q) * math.dist(q, r) * math.dist(r, p) / (4 * area(p, q, r))

    assert math.isclose(circumradius(a, b, d), circumradius(a, c, d))
    return inradius(a, b, d) / inradius(a, c, d)
