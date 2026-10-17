"""วันที่สอง ข้อ 1 — AH·FH = GH²  (พิสูจน์)

BC is a diameter, so ∠BDC = ∠BEC = 90°: CD, BE are altitudes, F is the
orthocentre and AH ⟂ BC. Triangles BHF and AHC are similar, so
AH·FH = BH·HC, and G on the circle over the diameter BC gives GH² = BH·HC.
The solver computes FH = BH·HC/AH for given lengths (here BH = 3, HC = 4,
AH = 5: 12/5).

``check`` builds the circle, intersects AB and AC with it, crosses CD with BE,
and measures F's height above BC.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"bh": 3, "hc": 4, "ah": 5}
ANSWER = Fraction(12, 5)
TOL = 1e-9
VARIANTS = [{"bh": 1, "hc": 9, "ah": 4}, {"bh": 2, "hc": 2, "ah": 3}, {"bh": 5, "hc": 7, "ah": 12}]


def solve(bh=3, hc=4, ah=5):
    return Fraction(bh * hc, ah)


def check(bh=3, hc=4, ah=5):
    b, c, a = (-bh, 0.0), (hc, 0.0), (0.0, ah)
    centre, radius = ((hc - bh) / 2, 0.0), (bh + hc) / 2

    def second_point(p, q):
        dx, dy = q[0] - p[0], q[1] - p[1]
        s = -2 * ((p[0] - centre[0]) * dx + (p[1] - centre[1]) * dy) / (dx * dx + dy * dy)
        return (p[0] + s * dx, p[1] + s * dy)

    d, e = second_point(b, a), second_point(c, a)
    # F = C + s(D − C) = B + u(E − B)
    m11, m12, m21, m22 = d[0] - c[0], -(e[0] - b[0]), d[1] - c[1], -(e[1] - b[1])
    r1, r2 = b[0] - c[0], b[1] - c[1]
    s = (r1 * m22 - m12 * r2) / (m11 * m22 - m12 * m21)
    f = (c[0] + s * (d[0] - c[0]), c[1] + s * (d[1] - c[1]))
    assert abs(f[0]) < 1e-9
    g_height = math.sqrt(radius**2 - centre[0] ** 2)
    assert math.isclose(g_height**2, ah * f[1])
    return f[1]
