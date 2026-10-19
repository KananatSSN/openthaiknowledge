"""ข้อ 1 — CP² = AC·CQ − AP·PR  (พิสูจน์)

∠CQP = 90° gives CQ = CP·cos C, so AC·CQ = CP·BC; the power of A gives
AP·AR = AQ·AC, so AP·PR = AQ·AC − AP² = BP·PC; subtracting gives the identity.
The solver returns (AC·CQ, AP·PR, CP²) for BP, PC (3, 4).

``check`` builds the figure (B at the origin, A above it at an arbitrary
height), intersects ω with AC and AP, and multiplies the lengths.
"""

from __future__ import annotations

import math

PARAMS = {"bp": 3, "pc": 4}
ANSWER = (28, 12, 16)
TOL = 1e-9
VARIANTS = [{"bp": 1, "pc": 1}, {"bp": 5, "pc": 2}, {"bp": 7, "pc": 9}]


def solve(bp=3, pc=4):
    bc = bp + pc
    return (bc * pc, bp * pc, pc * pc)


def check(bp=3, pc=4):
    h = 4.7
    a, c, p = (0.0, h), (float(bp + pc), 0.0), (float(bp), 0.0)
    centre, radius = ((p[0] + c[0]) / 2, 0.0), pc / 2

    def hits(start, end):
        dx, dy = end[0] - start[0], end[1] - start[1]
        qa = dx * dx + dy * dy
        qb = 2 * ((start[0] - centre[0]) * dx + (start[1] - centre[1]) * dy)
        qc = (start[0] - centre[0]) ** 2 + (start[1] - centre[1]) ** 2 - radius**2
        disc = math.sqrt(qb * qb - 4 * qa * qc)
        return [(start[0] + t * dx, start[1] + t * dy) for t in ((-qb - disc) / (2 * qa), (-qb + disc) / (2 * qa))]

    q = min(hits(a, c), key=lambda pt: math.dist(pt, a))  # the hit other than C
    r = max(hits(a, p), key=lambda pt: math.dist(pt, a))  # beyond P
    ac, cq, ap, pr = math.dist(a, c), math.dist(c, q), math.dist(a, p), math.dist(p, r)
    return (ac * cq, ap * pr, math.dist(c, p) ** 2)
