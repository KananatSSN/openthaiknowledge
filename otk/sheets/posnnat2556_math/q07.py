"""ข้อ 7 — มีสามเหลี่ยมพื้นที่น้อยกว่า 1/1700  (พิสูจน์)

Triangulate the hexagon with the 2556 interior points as vertices. The angle
sum gives T·180° = (h − 2)·180° + N·360°, so T = 2N + h − 2 = 5116 triangles
sharing the area 3√3/2 ≈ 2.598, and one has area at most 2.598/5116 < 1/1700.
The solver returns T.

``check`` builds a triangulation: a fan of the convex h-gon, then each interior
point inserted inside an existing triangle (taken round-robin) and joined to its
corners. It counts the triangles, confirms their areas add up to the polygon's,
and for the source checks the area bound.
"""

from __future__ import annotations

from collections import deque
from math import cos, pi, sin, sqrt

PARAMS = {"corners": 6, "interior": 2556}
ANSWER = 5116
VARIANTS = [{"corners": 6, "interior": 10}, {"corners": 4, "interior": 100},
            {"corners": 8, "interior": 37}, {"corners": 3, "interior": 1}]


def solve(corners=6, interior=2556):
    return 2 * interior + corners - 2


def _area(p, q, r):
    return abs((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1])) / 2


def check(corners=6, interior=2556):
    poly = [(cos(2 * pi * i / corners), sin(2 * pi * i / corners)) for i in range(corners)]
    queue = deque((poly[0], poly[i], poly[i + 1]) for i in range(1, corners - 1))
    for j in range(interior):
        p, q, r = queue.popleft()
        u, v = 0.2 + 0.6 * ((j * 0.618034) % 1), 0.0
        v = (1 - u) * (0.2 + 0.6 * ((j * 0.414214) % 1))
        w = 1 - u - v
        x = (u * p[0] + v * q[0] + w * r[0], u * p[1] + v * q[1] + w * r[1])
        queue.extend(((p, q, x), (q, r, x), (r, p, x)))
    count = len(queue)
    total = sum(_area(*t) for t in queue)
    hull = corners * sin(2 * pi / corners) / 2
    assert abs(total - hull) < 1e-9
    if (corners, interior) == (6, 2556):
        side_one = 3 * sqrt(3) / 2  # the source hexagon of side 1
        assert side_one / count < 1 / 1700
    return count
