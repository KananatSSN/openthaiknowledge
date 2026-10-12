"""ข้อ 24 — จำนวนรูปสี่เหลี่ยมจากจุด 24 จุดบนเส้นรอบรูปครึ่งวงกลม

กำหนดจุด 24 จุดเป็นจุดสีแดง 20 จุด และจุดสีเขียว 4 จุด บนเส้นรอบรูปของรูปครึ่งวงกลม
โดยมีจุดสีแดงเท่านั้นที่อยู่บนเส้นผ่านศูนย์กลางของวงกลม  ต้องการสร้างรูปสี่เหลี่ยมโดยใช้
จุด 4 จุดจากจุด 24 จุดนี้เป็นจุดยอด จะได้รูปสี่เหลี่ยมที่แตกต่างกันทั้งหมดกี่รูป

**The wording is load-bearing**: "มีจุดสีแดงเท่านั้นที่อยู่บนเส้นผ่านศูนย์กลาง" says the
points on the diameter are exactly the red ones — all 20 of them — so the greens
are all on the arc and no three of them are collinear.

A quadrilateral needs no three of its vertices collinear, so at most two vertices
may come from the diameter:

    C(g,4) + C(g,3)·r + C(g,2)·C(r,2)

= 1 + 4·20 + 6·190 = **1221** for g = 4 green and r = 20 red. Note the third term
dominates and the "1 green, 3 red" case contributes nothing.

``check`` builds the 24 points in coordinates and counts the 4-subsets with no
collinear triple, which is the definition rather than the formula.
"""

from __future__ import annotations

import itertools
import math

#: red points on the diameter, green points on the arc.
PARAMS = {"red": 20, "green": 4}
ANSWER = 1221
VARIANTS = [
    {"red": 5, "green": 5},
    {"red": 10, "green": 3},
    {"red": 2, "green": 6},
    {"red": 30, "green": 4},
    {"red": 20, "green": 1},           # too few arc points for any quadrilateral
]


def solve(red=20, green=4):
    """C(g,4) + C(g,3)·r + C(g,2)·C(r,2) — at most two vertices off the arc."""
    if red < 0 or green < 0:
        return None
    return (math.comb(green, 4)
            + math.comb(green, 3) * red
            + math.comb(green, 2) * math.comb(red, 2))


def check(red=20, green=4):
    """Independent: place the points and count 4-subsets with no collinear triple."""
    if red < 0 or green < 0:
        return None
    if math.comb(red + green, 4) > 4 * 10 ** 5:
        return None
    pts = [(-1 + 2 * (i + 1) / (red + 1), 0.0) for i in range(red)]
    for j in range(green):                        # strictly inside the upper arc
        t = math.pi * (j + 1) / (green + 1)
        pts.append((math.cos(t), math.sin(t)))

    def collinear(p, q, r) -> bool:
        return abs((q[0] - p[0]) * (r[1] - p[1])
                   - (q[1] - p[1]) * (r[0] - p[0])) < 1e-12

    n = 0
    for quad in itertools.combinations(pts, 4):
        if not any(collinear(*tri) for tri in itertools.combinations(quad, 3)):
            n += 1
    return n
