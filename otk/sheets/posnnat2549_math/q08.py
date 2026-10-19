"""ข้อ 8 — s⁴ − 18s² − 8s เมื่อ s = √a + √b + √c และ a, b, c เป็นรากของ x³ − 9x² + 11x − 1

With t = √ab + √bc + √ca: s² = p + 2t and t² = q + 2√(abc)·s, so
(s² − p)² = 4q + 8ws and s⁴ − 2ps² − 8ws = 4q − p² = −37.

``check`` finds the three positive roots by bisection between the critical
points, takes the square roots and evaluates the polynomial in s.
"""

from __future__ import annotations

import math

PARAMS = {"p": 9, "q": 11, "w": 1}
ANSWER = -37
TOL = 1e-8
VARIANTS = [{"p": 16, "q": 16, "w": 2}, {"p": 10, "q": 20, "w": 1}, {"p": 20, "q": 50, "w": 3}]


def solve(p=9, q=11, w=1):
    return 4 * q - p * p


def check(p=9, q=11, w=1):
    r = w * w

    def f(x):
        return ((x - p) * x + q) * x - r

    disc = math.sqrt(p * p - 3 * q)
    c1, c2 = (p - disc) / 3, (p + disc) / 3
    roots = []
    for lo, hi in ((0.0, c1), (c1, c2), (c2, float(p + 1))):
        for _ in range(200):
            mid = (lo + hi) / 2
            if (f(lo) < 0) == (f(mid) < 0):
                lo = mid
            else:
                hi = mid
        roots.append((lo + hi) / 2)
    s = sum(math.sqrt(x) for x in roots)
    return s**4 - 2 * p * s * s - 8 * w * s
