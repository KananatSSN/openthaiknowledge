"""วันที่สอง ข้อ 4 — P เป็นจุดศูนย์กลางของวงกลมที่สัมผัสสามวงแรก  (พิสูจน์)

With R = AB/2: O₂ = (0, R/2) has radius R/2; the side semicircle O₃ = (d, 0) of
radius ρ needs d + ρ = R and √(d² + R²/4) = R/2 + ρ, so d = 2R/3 and ρ = R/3.
P = (2R/3, R/2) has O₁P = 5R/6, O₂P = 2R/3 and O₃P = R/2, so the circle at P of
radius R/6 touches all three. The solver returns that radius (AB = 12: 1).

``check`` finds d by bisection on the two tangency conditions, places P, and
reads the radius off the distance to O₁.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"ab": 12}
ANSWER = 1
TOL = 1e-9
VARIANTS = [{"ab": 4}, {"ab": 37}, {"ab": 60}]


def solve(ab=12):
    return Fraction(ab, 12)


def check(ab=12):
    r = ab / 2

    def gap(d):
        rho = r - d
        return math.hypot(d, r / 2) - (r / 2 + rho)

    lo, hi = 0.0, r
    for _ in range(200):
        mid = (lo + hi) / 2
        if gap(mid) < 0:
            lo = mid
        else:
            hi = mid
    d = (lo + hi) / 2
    rho = r - d
    p = (d, r / 2)
    radius = r - math.hypot(*p)
    assert math.isclose(math.hypot(p[0], p[1] - r / 2), r / 2 + radius)
    assert math.isclose(r / 2, rho + radius)  # O₃P = R/2
    return radius
