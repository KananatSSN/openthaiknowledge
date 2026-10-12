"""ข้อ 18 — สัดส่วนพื้นที่แรเงาในสี่เหลี่ยมจัตุรัส

จากรูป สี่เหลี่ยมจัตุรัสรูปนี้มี AC : CB = 2 : 1 จงหาสัดส่วนของพื้นที่ที่แรเงาต่อพื้นที่
สี่เหลี่ยมจัตุรัสรูปนี้

**What the figure says and the text does not:** A and B are the two ends of the
*top* side and C sits between them; the two drawn lines run from A to the
bottom-right corner and from C to the bottom-left corner, and the shaded region
is the pair of triangles above and below their crossing point — the top one
spanning AC, the bottom one spanning the whole bottom side.

With side S = m + k, A = (0, S), C = (m, S), and the corners L = (0, 0),
R = (S, 0), the two lines are ``y = S − x`` and ``y = Sx/m``. They meet at

    x = Sm/(m + S)      y = S²/(m + S)

The upper triangle has base m and height S − y = Sm/(m + S); the lower has base S
and height y. Adding and dividing by S²,

    ratio = (m² + S²) / (2S(m + S))

and for m : k = 2 : 1, S = 3, that is (4 + 9)/(2·3·5) = **13/30**.

``solve`` evaluates that fraction. ``check`` never uses it: it locates the
crossing point by Cramer's rule on the two line equations, takes both shaded
areas by shoelace, and — the part that actually guards the reading of the
figure — asserts that the four regions the two lines cut the square into add back
up to S² exactly.
"""

from __future__ import annotations

from fractions import Fraction

#: AC : CB = m : k along the top side.
PARAMS = {"m": 2, "k": 1}
ANSWER = Fraction(13, 30)
VARIANTS = [
    {"m": 1, "k": 1},
    {"m": 3, "k": 1},
    {"m": 1, "k": 3},
    {"m": 3, "k": 2},
    {"m": 5, "k": 4},
    {"m": 7, "k": 2},
]


def _shoelace(points) -> Fraction:
    total = Fraction(0)
    for i, (x0, y0) in enumerate(points):
        x1, y1 = points[(i + 1) % len(points)]
        total += x0 * y1 - x1 * y0
    return abs(total) / 2


def solve(m=2, k=1):
    """The closed fraction (m² + S²) / (2S(m + S)) with S = m + k."""
    if m <= 0 or k <= 0:
        return None
    side = Fraction(m + k)
    return (Fraction(m) ** 2 + side ** 2) / (2 * side * (Fraction(m) + side))


def check(m=2, k=1):
    """Independent: intersect the lines by Cramer, then shoelace every region.

    The two lines through A→R and C→L are written as ``px + qy = t`` and solved
    by determinants. All four regions are measured, and their total is compared
    with the square before the shaded pair is reported — a misread of *which*
    regions are shaded cannot survive that.
    """
    if m <= 0 or k <= 0:
        return None
    side = Fraction(m + k)
    a = (Fraction(0), side)
    b = (side, side)
    c = (Fraction(m), side)
    lo_left = (Fraction(0), Fraction(0))
    lo_right = (side, Fraction(0))

    def line(p, q):
        # px + qy = t through the two points
        return (q[1] - p[1], p[0] - q[0], p[0] * q[1] - q[0] * p[1])

    a1, b1, t1 = line(a, lo_right)
    a2, b2, t2 = line(c, lo_left)
    determinant = a1 * b2 - a2 * b1
    if determinant == 0:
        return None
    cross = ((t1 * b2 - t2 * b1) / determinant,
             (a1 * t2 - a2 * t1) / determinant)

    top = _shoelace([a, c, cross])
    bottom = _shoelace([lo_left, lo_right, cross])
    left = _shoelace([a, cross, lo_left])
    right = _shoelace([c, b, lo_right, cross])
    if top + bottom + left + right != side * side:
        return None
    return (top + bottom) / (side * side)
