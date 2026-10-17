"""ข้อ 4 — พื้นที่ O₁O₂O₃O₄ ≤ 1  (พิสูจน์)

∠AO₁B = 135° puts O₁ on the square's circumcircle (R² = 1/2), at arc α₁ = ∠EAB
from B; the arcs between consecutive incentres are 90° + αᵢ − αᵢ₊₁, so the area
is ¼Σcos(αᵢ − αᵢ₊₁) ≤ 1. The solver returns that area (all α = 30°: 1).

``check`` builds E, F, G, H outside the unit square, computes each incentre by
the side-weighted average, and takes the shoelace area.
"""

from __future__ import annotations

import math

PARAMS = {"angles": (30, 30, 30, 30)}
ANSWER = 1.0
TOL = 1e-9
VARIANTS = [{"angles": (30, 60, 30, 60)}, {"angles": (60, 60, 30, 30)}, {"angles": (45, 20, 70, 35)}]


def solve(angles=(30, 30, 30, 30)):
    return sum(math.cos(math.radians(a - b)) for a, b in zip(angles, angles[1:] + angles[:1])) / 4


def check(angles=(30, 30, 30, 30)):
    square = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]  # A, B, C, D counter-clockwise
    centres = []
    for i, alpha in enumerate(angles):
        p, q = square[i], square[(i + 1) % 4]
        side = (q[0] - p[0], q[1] - p[1])
        outward = (side[1], -side[0])  # right of p→q is outside for a ccw square
        al = math.radians(alpha)
        pe = math.cos(al)  # PE = side·cos α (right angle at E)
        e = (p[0] + pe * (math.cos(al) * side[0] + math.sin(al) * outward[0]),
             p[1] + pe * (math.cos(al) * side[1] + math.sin(al) * outward[1]))
        la, lb, lc = math.dist(q, e), math.dist(p, e), 1.0
        t = la + lb + lc
        centres.append(((la * p[0] + lb * q[0] + lc * e[0]) / t, (la * p[1] + lb * q[1] + lc * e[1]) / t))
    return abs(sum(centres[i][0] * centres[(i + 1) % 4][1] - centres[(i + 1) % 4][0] * centres[i][1] for i in range(4))) / 2
