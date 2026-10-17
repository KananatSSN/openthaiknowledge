"""ข้อ 2 — เส้นแบ่งครึ่งตั้งฉากของ BC แบ่งครึ่ง IJ  (พิสูจน์)

With B at the origin, A = (a, 0), C = (0, c), D = (d, 0) and E = (−d, 0), the
incentre I of ACE and the A-excentre J of ACD have heights summing to c, so the
midpoint of IJ lies on y = c/2. J's height is c(AC + CD)/(AC + CD + a + d)
(AB, BD, BC = 9, 5, 12: 8). The solver returns it.

``check`` builds I and J from their barycentric weights, asserts their heights
add to c, and returns J's height.
"""

from __future__ import annotations

from math import hypot

PARAMS = {"a": 9, "d": 5, "c": 12}
ANSWER = 8.0
VARIANTS = [{"a": 16, "d": 9, "c": 12}, {"a": 20, "d": 8, "c": 15}, {"a": 40, "d": 16, "c": 30}]
TOL = 1e-9


def solve(a=9, d=5, c=12):
    ac, cd = hypot(a, c), hypot(d, c)
    return c * (ac + cd) / (ac + cd + a + d)


def check(a=9, d=5, c=12):
    A, C, D, E = (a, 0.0), (0.0, c), (d, 0.0), (-d, 0.0)

    def length(p, q):
        return hypot(p[0] - q[0], p[1] - q[1])

    # incentre of ACE: weights = opposite sides
    wa, wc, we = length(C, E), length(A, E), length(A, C)
    inc = ((wa * A[0] + wc * C[0] + we * E[0]) / (wa + wc + we), (wa * A[1] + wc * C[1] + we * E[1]) / (wa + wc + we))
    # A-excentre of ACD: weights (−a', c', d')
    wa, wc, wd = length(C, D), length(A, D), length(A, C)
    s = -wa + wc + wd
    J = ((-wa * A[0] + wc * C[0] + wd * D[0]) / s, (-wa * A[1] + wc * C[1] + wd * D[1]) / s)
    assert abs(inc[1] + J[1] - c) < 1e-9
    return J[1]
