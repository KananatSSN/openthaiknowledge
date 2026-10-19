"""วันที่สอง ข้อ 2 — AB/BC = (AR/RC)²  (พิสูจน์)

The bisector gives AR/RC = QA/QC. P is the pole of AC, so QP is the symmedian
of triangle QAC and AB : BC = QA² : QC². The solver returns AB for AC = L and
AR : RC = p : q: L·p²/(p² + q²) (L = 10, 2 : 3 → 40/13).

``check`` builds the figure: A, C on the unit circle, P the pole of AC, Q moved
along the far arc until QA/QC = p/q, B = PQ ∩ AC, scaled to AC = L.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"length": 10, "p": 2, "q": 3}
ANSWER = Fraction(40, 13)
TOL = 1e-8
VARIANTS = [{"length": 12, "p": 2, "q": 5}, {"length": 7, "p": 3, "q": 1}, {"p": 1, "q": 1}]


def solve(length=10, p=2, q=3):
    return Fraction(length * p * p, p * p + q * q)


def check(length=10, p=2, q=3):
    ta, tc = 0.4, 2.2
    a, c = (math.cos(ta), math.sin(ta)), (math.cos(tc), math.sin(tc))
    mid = ((a[0] + c[0]) / 2, (a[1] + c[1]) / 2)
    m2 = mid[0] ** 2 + mid[1] ** 2
    pole = (mid[0] / m2, mid[1] / m2)

    def ratio(t):
        qt = (math.cos(t), math.sin(t))
        return math.dist(qt, a) / math.dist(qt, c), qt

    lo, hi = tc + 1e-6, ta + 2 * math.pi - 1e-6  # QA/QC falls from ∞ to 0 along this arc
    for _ in range(200):
        mid_t = (lo + hi) / 2
        if ratio(mid_t)[0] > p / q:
            lo = mid_t
        else:
            hi = mid_t
    qt = ratio((lo + hi) / 2)[1]
    # B = A + s(C − A) on line pole→Q
    dx, dy = c[0] - a[0], c[1] - a[1]
    ex, ey = qt[0] - pole[0], qt[1] - pole[1]
    det = dx * (-ey) - (-ex) * dy
    s = ((pole[0] - a[0]) * (-ey) - (-ex) * (pole[1] - a[1])) / det
    return s * length
