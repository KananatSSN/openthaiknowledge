"""ข้อ 3 — ระบายสีระนาบ 2 สี มีสามเหลี่ยมด้าน 1, 2, √3 สีเดียว  (พิสูจน์)

The proof works on a regular hexagon inscribed in a circle of radius 1: an
inscribed 30–60–90 triangle has a diameter (length 2) as hypotenuse and its
third vertex 60° along the circle from an end, giving sides 1, √3, 2. On a
regular n-gon (6 | n) that is n/2 diameters times 4 positions. The solver
returns that count (hexagon: 12).

``check`` places the vertices on the unit circle and tests every triple for
sides in the ratio 1 : √3 : 2.
"""

from __future__ import annotations

from itertools import combinations
from math import cos, pi, sin

PARAMS = {"sides": 6}
ANSWER = 12
VARIANTS = [{"sides": 12}, {"sides": 18}, {"sides": 24}, {"sides": 8}]


def solve(sides=6):
    return sides // 2 * 4 if sides % 6 == 0 else 0


def check(sides=6):
    pts = [(cos(2 * pi * i / sides), sin(2 * pi * i / sides)) for i in range(sides)]
    count = 0
    for p, q, s in combinations(pts, 3):
        d = sorted(((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2) for u, v in ((p, q), (q, s), (p, s)))
        if abs(d[1] - 3 * d[0]) < 1e-9 and abs(d[2] - 4 * d[0]) < 1e-9:
            count += 1
    return count
