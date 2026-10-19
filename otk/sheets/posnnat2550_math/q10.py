"""ข้อ 10 — n น้อยสุดที่ √3 zⁿ⁺¹ − zⁿ − 1 = 0 มีรากขนาดหนึ่งหน่วย

For a = 2cos(π/m): |z| = 1 forces |az − 1| = 1, so z = e^{±iπ/m} and
az − 1 = e^{±2iπ/m}; then zⁿ = e^{∓2iπ/m} gives n ≡ −2 (mod 2m). For √3
(m = 6) the least n is 10.

``check`` searches n upward and, for each, minimises |a·zⁿ⁺¹ − zⁿ − 1| over
z = e^{iθ} on a fine grid with local refinement.
"""

from __future__ import annotations

import cmath
import math

PARAMS = {"m": 6, "above": 0}
ANSWER = 10
VARIANTS = [{"m": 3}, {"m": 4}, {"m": 5}, {"m": 6, "above": 11}]


def solve(m=6, above=0):
    n = (-2) % (2 * m) or 2 * m
    while n <= above:
        n += 2 * m
    return n


def check(m=6, above=0):
    a = 2 * math.cos(math.pi / m)
    for n in range(above + 1, above + 4 * m + 2):
        def g(th, n=n):
            z = cmath.exp(1j * th)
            return abs(a * z ** (n + 1) - z**n - 1)

        steps = 4000
        th = min((2 * math.pi * i / steps for i in range(steps)), key=g)
        lo, hi = th - 2 * math.pi / steps, th + 2 * math.pi / steps
        for _ in range(100):
            m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
            if g(m1) < g(m2):
                hi = m2
            else:
                lo = m1
        if g((lo + hi) / 2) < 1e-9:
            return n
    return None
