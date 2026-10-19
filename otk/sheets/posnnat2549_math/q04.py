"""ข้อ 4 — sin∠CAQ เมื่อ 3QA = 2AP

With QA = 2t, AP = PB = 3t, triangle QBP is right-angled at B, so QB = 4t;
QA² = QC·QB gives QC = t and BC = 3t; ∠CAQ = ∠ABC and AC/AB = QA/QB = 1/2, so
sin∠CAQ = AC/BC = 1/√5. In general sin² = p/(2(p + q)) for QA : AP = p : q.

``check`` builds the figure on the unit circle: it bisects on A's position until
QA/AP = p/q, then measures the angle CAQ.
"""

from __future__ import annotations

import math

PARAMS = {"p": 2, "q": 3}
ANSWER = 1 / math.sqrt(5)
TOL = 1e-8
VARIANTS = [{"p": 1, "q": 1}, {"p": 3, "q": 2}, {"p": 5, "q": 7}, {"p": 1, "q": 9}]


def solve(p=2, q=3):
    return math.sqrt(p / (2 * (p + q)))


def check(p=2, q=3):
    def build(theta):
        a = (math.cos(theta), math.sin(theta))
        pnt = ((1 + a[1]) / a[0], -1.0)  # tangents at A and at B = (0, −1)
        qnt = (0.0, 1 / a[1])  # tangent at A meets line BO (x = 0)
        return a, pnt, qnt

    lo, hi = 0.01, math.pi / 2 - 0.01
    for _ in range(200):
        mid = (lo + hi) / 2
        a, pnt, qnt = build(mid)
        if math.dist(qnt, a) / math.dist(pnt, a) > p / q:
            lo = mid
        else:
            hi = mid
    a, pnt, qnt = build(lo)
    c = (0.0, 1.0)
    v, w = (c[0] - a[0], c[1] - a[1]), (qnt[0] - a[0], qnt[1] - a[1])
    cross = abs(v[0] * w[1] - v[1] * w[0])
    return cross / (math.hypot(*v) * math.hypot(*w))
