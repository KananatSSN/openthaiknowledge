"""วันที่สอง ข้อ 1 — MNOP เป็นรูปสี่เหลี่ยมขนมเปียกปูน  (พิสูจน์)

MN is a midline of triangle APB, so MN ∥ PB and MN = PB/2 = PA/2 = PM; the
construction makes NO ∥ PA with PO = PA/2, so MNOP is a rhombus with side t/2
and angle ∠APB. The solver returns its area c√(4t² − c²)/8 for PA = PB = t and
AB = c (t = 5, c = 6: 6).

``check`` carries out the whole construction in coordinates (M, N, C, D, O),
confirms the four sides are equal, and takes the area by the shoelace formula.
"""

from __future__ import annotations

import math
from fractions import Fraction
from math import isqrt

PARAMS = {"t": 5, "c": 6}
ANSWER = 6
TOL = 1e-8
VARIANTS = [{"t": 5, "c": 8}, {"t": 13, "c": 10}, {"t": 17, "c": 16}]


def solve(t=5, c=6):
    root = isqrt(4 * t * t - c * c)
    assert root * root == 4 * t * t - c * c
    return Fraction(c * root, 8)


def check(t=5, c=6):
    cos_a = c / (2 * t)
    alpha = math.acos(cos_a)
    r = t / math.tan(alpha)
    a, b = (r * math.cos(alpha), r * math.sin(alpha)), (r * math.cos(alpha), -r * math.sin(alpha))
    p = (r / math.cos(alpha), 0.0)

    def second_hit(start, direction):
        # start + s·direction on the circle x² + y² = r², the root other than s ≈ 0 side
        dx, dy = direction
        qa = dx * dx + dy * dy
        qb = 2 * (start[0] * dx + start[1] * dy)
        qc = start[0] ** 2 + start[1] ** 2 - r * r
        disc = math.sqrt(qb * qb - 4 * qa * qc)
        return [(start[0] + s * dx, start[1] + s * dy) for s in ((-qb + disc) / (2 * qa), (-qb - disc) / (2 * qa))]

    m = ((a[0] + p[0]) / 2, (a[1] + p[1]) / 2)
    n = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    hits = second_hit(m, (n[0] - m[0], n[1] - m[1]))
    cpt = max(hits, key=lambda h: (h[0] - m[0]) * (n[0] - m[0]) + (h[1] - m[1]) * (n[1] - m[1]))  # beyond N
    hits = second_hit(p, (cpt[0] - p[0], cpt[1] - p[1]))
    d = min(hits, key=lambda h: math.dist(h, p))
    # O = N + s(D − N) on line PB
    e1, e2 = (d[0] - n[0], d[1] - n[1]), (b[0] - p[0], b[1] - p[1])
    det = e1[0] * (-e2[1]) - (-e2[0]) * e1[1]
    s = ((p[0] - n[0]) * (-e2[1]) - (-e2[0]) * (p[1] - n[1])) / det
    o = (n[0] + s * e1[0], n[1] + s * e1[1])
    quad = [m, n, o, p]
    sides = [math.dist(quad[i], quad[(i + 1) % 4]) for i in range(4)]
    assert max(sides) - min(sides) < 1e-9
    return abs(sum(quad[i][0] * quad[(i + 1) % 4][1] - quad[(i + 1) % 4][0] * quad[i][1] for i in range(4))) / 2
