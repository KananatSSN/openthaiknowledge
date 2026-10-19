"""ข้อ 11 — QS แบ่งครึ่งมุม DSE  (พิสูจน์)

QR is the A-altitude, so S is its foot and BS = c·cos B = (a² + c² − b²)/(2a);
S sees the chord of contact DE symmetrically. The solver returns BS
(a, b, c = 13, 14, 15: 99/13).

``check`` carries out the construction: tangents from A to the circle on BC,
M and N on line BC, Q = CP ∩ DE, R = ME ∩ ND, S = QR ∩ BC; it asserts that QS
bisects ∠DSE and measures BS.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"a": 13, "b": 14, "c": 15}
ANSWER = Fraction(99, 13)
TOL = 1e-7
VARIANTS = [{"a": 7, "b": 8, "c": 9}, {"a": 10, "b": 11, "c": 9}, {"a": 6, "b": 5, "c": 7}]


def solve(a=13, b=14, c=15):
    return Fraction(a * a + c * c - b * b, 2 * a)


def _meet(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


def check(a=13, b=14, c=15):
    bp, cp = (0.0, 0.0), (float(a), 0.0)
    x = (c * c - b * b + a * a) / (2 * a)
    ap = (x, math.sqrt(c * c - x * x))
    centre, r = (a / 2, 0.0), a / 2
    dist = math.dist(ap, centre)
    base = math.atan2(ap[1] - centre[1], ap[0] - centre[0])
    half = math.acos(r / dist)
    d = (centre[0] + r * math.cos(base + half), centre[1] + r * math.sin(base + half))
    e = (centre[0] + r * math.cos(base - half), centre[1] + r * math.sin(base - half))
    m = _meet(ap, d, bp, cp)
    n = _meet(ap, e, bp, cp)
    # foot P of the altitude from C on AB
    ux, uy = ap[0] - bp[0], ap[1] - bp[1]
    t = ((cp[0] - bp[0]) * ux + (cp[1] - bp[1]) * uy) / (ux * ux + uy * uy)
    p = (bp[0] + t * ux, bp[1] + t * uy)
    q = _meet(cp, p, d, e)
    rr = _meet(m, e, n, d)
    s = _meet(q, rr, bp, cp)

    def angle(u, o, v):
        a1 = math.atan2(u[1] - o[1], u[0] - o[0])
        a2 = math.atan2(v[1] - o[1], v[0] - o[0])
        return abs((a1 - a2 + math.pi) % (2 * math.pi) - math.pi)

    assert abs(angle(d, s, q) - angle(q, s, e)) < 1e-7
    return math.dist(bp, s)
