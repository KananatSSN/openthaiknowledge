"""ข้อ 29 — พื้นที่ผิวของทรงกลมที่ล้อมรอบทรงสี่หน้า

ให้ ABCD เป็นทรงสี่หน้า มีด้าน AD, BD และ CD ตั้งฉากซึ่งกันและกัน
สมมุติว่า AD = 12, BD = 16 และ CD = 5  จงหาพื้นที่ผิวของทรงกลมที่ผ่านจุดยอดทั้งสี่

Method: three mutually perpendicular edges at D make ABCD the corner of a
rectangular box with sides AD, BD, CD. The box's circumscribed sphere is the
tetrahedron's, and its diameter is the space diagonal, so
    2R = √(a² + b² + c²)   ⟹   surface = 4πR² = π(a² + b² + c²),
which for 12, 16, 5 is π·425 = 425π ≈ 1335.2. Note the answer is π times the sum
of squares — no square root survives.

``check`` places the four vertices in a *rotated and translated* frame — so the
equidistance equations do not decouple and cannot be read off — solves the
resulting 3×3 linear system by elimination, and squares the distance it gets. It
never mentions a box.
"""

from __future__ import annotations

import math

TOL = 1e-9

PARAMS = {"ad": 12, "bd": 16, "cd": 5}
ANSWER = 1335.1768777756622             # 425π
VARIANTS = [
    {"ad": 1, "bd": 1, "cd": 1},
    {"ad": 3, "bd": 4, "cd": 12},
    {"ad": 2, "bd": 3, "cd": 6},
    {"ad": 20, "bd": 1, "cd": 1},
    {"ad": 7, "bd": 24, "cd": 60},
]


def radius(ad=12, bd=16, cd=5) -> float:
    """Circumradius: half the space diagonal of the implied box."""
    return math.sqrt(ad * ad + bd * bd + cd * cd) / 2


def solve(ad=12, bd=16, cd=5):
    """Surface area of the circumscribed sphere."""
    return math.pi * (ad * ad + bd * bd + cd * cd)


def _rotation():
    """A fixed, thoroughly generic rotation matrix (three Euler turns)."""
    ca, sa = math.cos(0.7), math.sin(0.7)
    cb, sb = math.cos(1.1), math.sin(1.1)
    cc, sc = math.cos(0.3), math.sin(0.3)
    rz = ((ca, -sa, 0.0), (sa, ca, 0.0), (0.0, 0.0, 1.0))
    ry = ((cb, 0.0, sb), (0.0, 1.0, 0.0), (-sb, 0.0, cb))
    rx = ((1.0, 0.0, 0.0), (0.0, cc, -sc), (0.0, sc, cc))
    def mul(m, n):
        return tuple(tuple(sum(m[i][k] * n[k][j] for k in range(3))
                           for j in range(3)) for i in range(3))
    return mul(mul(rz, ry), rx)


def check(ad=12, bd=16, cd=5):
    """Independent: solve the equidistance system in a generic frame."""
    rot, shift = _rotation(), (-4.3, 9.1, 2.7)

    def place(v):
        return tuple(shift[i] + sum(rot[i][k] * v[k] for k in range(3))
                     for i in range(3))

    d = place((0.0, 0.0, 0.0))
    a, b, c = (place((ad, 0.0, 0.0)), place((0.0, bd, 0.0)),
               place((0.0, 0.0, cd)))
    # Edges at D are still mutually perpendicular — rotation preserves that.
    for u, v in ((a, b), (b, c), (a, c)):
        dot = sum((u[i] - d[i]) * (v[i] - d[i]) for i in range(3))
        assert abs(dot) < 1e-6, "the three edges at D are not perpendicular"

    # |P−V|² = |P−D|² ⟹ 2P·(V−D) = |V|² − |D|², one row per vertex.
    rows = [[2 * (v[i] - d[i]) for i in range(3)]
            + [sum(v[i] ** 2 - d[i] ** 2 for i in range(3))]
            for v in (a, b, c)]
    for col in range(3):                                   # Gaussian elimination
        pivot = max(range(col, 3), key=lambda r: abs(rows[r][col]))
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(3):
            if r != col and rows[col][col]:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [rows[r][k] - factor * rows[col][k] for k in range(4)]
    centre = tuple(rows[i][3] / rows[i][i] for i in range(3))

    dists = [math.dist(centre, v) for v in (a, b, c, d)]
    assert max(dists) - min(dists) < 1e-6, f"no common circumcentre: {dists}"
    return 4 * math.pi * dists[0] ** 2
