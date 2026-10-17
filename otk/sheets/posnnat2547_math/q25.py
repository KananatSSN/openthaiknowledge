"""วันที่สอง ข้อ 4 — พื้นที่สี่เหลี่ยมนูน ≤ (AB² + BC² + CD² + DA²)/4  (พิสูจน์)

Area = [ABC] + [CDA] ≤ AB·BC/2 + CD·DA/2 ≤ (AB² + BC²)/4 + (CD² + DA²)/4.
The solver computes the largest area for given sides (Brahmagupta: the cyclic
quadrilateral), √((s − a)(s − b)(s − c)(s − d)); for the unit square, the
equality case of the source, it is 1 = Σ side²/4.

``check`` searches the shape: the angle at B fixes the diagonal AC, Heron gives
the far triangle, and the best total area is kept.
"""

from __future__ import annotations

import math

PARAMS = {"sides": (1, 1, 1, 1)}
ANSWER = 1.0
TOL = 1e-6
VARIANTS = [{"sides": (3, 4, 5, 6)}, {"sides": (2, 7, 7, 4)}, {"sides": (5, 5, 6, 8)}]


def solve(sides=(1, 1, 1, 1)):
    s = sum(sides) / 2
    return math.sqrt(math.prod(s - x for x in sides))


def check(sides=(1, 1, 1, 1)):
    a, b, c, d = sides
    best = 0.0
    lo, hi = 1e-6, math.pi - 1e-6

    def area(angle):
        e = math.sqrt(a * a + b * b - 2 * a * b * math.cos(angle))
        if not abs(c - d) < e < c + d:
            return -1.0
        s = (c + d + e) / 2
        return a * b * math.sin(angle) / 2 + math.sqrt(max(s * (s - c) * (s - d) * (s - e), 0.0))

    grid = [lo + (hi - lo) * i / 20000 for i in range(20001)]
    x0 = max(grid, key=area)
    lo, hi = max(1e-6, x0 - 1e-3), min(math.pi - 1e-6, x0 + 1e-3)
    for _ in range(200):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if area(m1) < area(m2):
            lo = m1
        else:
            hi = m2
    best = area((lo + hi) / 2)
    return best
