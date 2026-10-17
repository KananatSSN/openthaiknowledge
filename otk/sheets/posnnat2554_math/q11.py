"""ข้อ 11 — incenter, centroid ของ IₐI_bI_c และ orthocenter ของ XYZ อยู่บนเส้นตรงเดียวกัน  (พิสูจน์)

I is the circumcentre of XYZ, so IH lies on the Euler line of XYZ. The sides of
the excentral triangle are parallel to those of XYZ (both perpendicular to the
bisectors), so the triangles are homothetic and their centroids lie on that
line. The solver returns IG/IH = abc/(3(s − a)(s − b)(s − c)) (5, 6, 7: 35/18).

``check`` computes I, the excentres, their centroid G, the contact triangle and
its orthocentre H in coordinates, asserts collinearity and divides IG by IH.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"a": 5, "b": 6, "c": 7}
ANSWER = Fraction(35, 12)
TOL = 1e-9
VARIANTS = [{"a": 3, "b": 4, "c": 5}, {"a": 7, "b": 8, "c": 9}, {"a": 4, "b": 4, "c": 7}]


def solve(a=5, b=6, c=7):
    s2 = a + b + c
    return Fraction(8 * a * b * c, 3 * (s2 - 2 * a) * (s2 - 2 * b) * (s2 - 2 * c))


def check(a=5, b=6, c=7):
    bp, cp = (0.0, 0.0), (float(a), 0.0)
    x = (c * c - b * b + a * a) / (2 * a)
    ap = (x, math.sqrt(c * c - x * x))

    def weighted(wa, wb, wc):
        t = wa + wb + wc
        return ((wa * ap[0] + wb * bp[0] + wc * cp[0]) / t, (wa * ap[1] + wb * bp[1] + wc * cp[1]) / t)

    incentre = weighted(a, b, c)
    ia, ib, ic = weighted(-a, b, c), weighted(a, -b, c), weighted(a, b, -c)
    g = ((ia[0] + ib[0] + ic[0]) / 3, (ia[1] + ib[1] + ic[1]) / 3)
    s = (a + b + c) / 2

    def along(p, q, dist):
        d = math.dist(p, q)
        return (p[0] + (q[0] - p[0]) * dist / d, p[1] + (q[1] - p[1]) * dist / d)

    xp, yp, zp = along(bp, cp, s - b), along(cp, ap, s - c), along(ap, bp, s - a)

    def orthocentre(p, q, r):
        # p + u·(perp of q − r) = q + v·(perp of r − p)
        d1 = (-(q[1] - r[1]), q[0] - r[0])
        d2 = (-(r[1] - p[1]), r[0] - p[0])
        det = d1[0] * (-d2[1]) - (-d2[0]) * d1[1]
        u = ((q[0] - p[0]) * (-d2[1]) - (-d2[0]) * (q[1] - p[1])) / det
        return (p[0] + u * d1[0], p[1] + u * d1[1])

    h = orthocentre(xp, yp, zp)
    cross = (g[0] - incentre[0]) * (h[1] - incentre[1]) - (g[1] - incentre[1]) * (h[0] - incentre[0])
    assert abs(cross) < 1e-7 * max(1.0, math.dist(g, incentre) * math.dist(h, incentre))
    return math.dist(g, incentre) / math.dist(h, incentre)
