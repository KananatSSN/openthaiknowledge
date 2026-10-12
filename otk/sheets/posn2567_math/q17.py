"""ข้อ 17 — ปริมาตรของ cuboctahedron

นำลูกบาศก์ลูกหนึ่งมาตัดมุมของลูกบาศก์ทั้งแปดมุมออกด้วยระนาบให้ผ่านขอบ 3 ขอบของ
ลูกบาศก์ที่ประกอบเป็นมุมแต่ละมุม จะได้รูปทรงสิบสี่หน้าที่เรียกว่า cuboctahedron
ที่มีหน้า 6 หน้าเป็นรูปสี่เหลี่ยมจัตุรัส อีก 8 หน้าเป็นรูปสามเหลี่ยมด้านเท่า และมี 24 ขอบ
ถ้าขอบแต่ละขอบยาว 1 หน่วย แล้วรูปทรงนี้มีปริมาตรเท่ากับเท่าใด (เขียนคำตอบเป็น
เศษส่วนอย่างต่ำ)

The cutting planes pass through the *midpoints* of the cube's edges — each one
runs through three edges meeting at a corner — so a cuboctahedron of edge a comes
from a cube of side a√2, and each of the eight removed corners is a right
tetrahedron with three legs of a√2/2:

    V = (a√2)³ - 8·(1/6)(a√2/2)³ = 2√2a³ - √2a³/3 = (5√2/3)a³

which is 5√2/3 at a = 1. Note the sheet's "เขียนคำตอบเป็นเศษส่วนอย่างต่ำ" refers
to the rational coefficient, not to the whole value: the volume is irrational.

So ``solve`` returns **the coefficient of √2**, exactly, as a Fraction — the
generator multiplies the √2 back on when it writes the TeX. ``ANSWER`` is 5/3 for
that reason; the volume itself is 5√2/3 ≈ 2.357.

``check`` never uses the cube. It takes the twelve vertices — all permutations of
(±a/√2, ±a/√2, 0) — finds the supporting planes by brute force (so it also proves
the solid really is their convex hull, with 6 square and 8 triangular faces), and
sums the cones from the centre to each face.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

#: the cuboctahedron's own edge length.
PARAMS = {"edge": 1}
ANSWER = Fraction(5, 3)
VARIANTS = [
    {"edge": 2},
    {"edge": 3},
    {"edge": 5},
    {"edge": 10},
    {"edge": 0},           # degenerate
]
TOL = 1e-9


def solve(edge=1):
    """The coefficient of √2 in the volume: V = (5/3)·a³·√2."""
    if edge <= 0:
        return None
    return Fraction(5, 3) * Fraction(edge) ** 3


def _vertices(a: float) -> list[tuple[float, float, float]]:
    """All permutations of (±a/√2, ±a/√2, 0) — the twelve edge midpoints."""
    h = a / math.sqrt(2)
    out = set()
    for zero in range(3):
        for s1 in (h, -h):
            for s2 in (h, -h):
                p = [s1, s2]
                p.insert(zero, 0.0)
                out.add(tuple(p))
    return sorted(out)


def check(edge=1):
    """Independent: convex hull of the twelve vertices, summed cone by cone.

    Every triple of vertices spanning a plane is tested as a supporting plane of
    the point set; the ones that keep all twelve on one side are the faces. Their
    vertices are ordered by angle within the plane, their areas come from cross
    products, and the volume is Σ (1/3)·area·(distance from the centre). The face
    census is asserted — 6 squares and 8 triangles, 24 edges — so a wrong vertex
    set could not slip through as a plausible number.
    """
    if edge <= 0:
        return None
    a = float(edge)
    pts = _vertices(a)

    def sub(p, q):
        return (p[0] - q[0], p[1] - q[1], p[2] - q[2])

    def cross(p, q):
        return (p[1] * q[2] - p[2] * q[1],
                p[2] * q[0] - p[0] * q[2],
                p[0] * q[1] - p[1] * q[0])

    def dot(p, q):
        return p[0] * q[0] + p[1] * q[1] + p[2] * q[2]

    eps = 1e-9 * max(1.0, a)
    faces: dict[tuple, list] = {}
    for tri in itertools.combinations(pts, 3):
        nrm = cross(sub(tri[1], tri[0]), sub(tri[2], tri[0]))
        ln = math.sqrt(dot(nrm, nrm))
        if ln < eps:                                  # collinear triple
            continue
        nrm = (nrm[0] / ln, nrm[1] / ln, nrm[2] / ln)
        off = dot(nrm, tri[0])
        if off < 0:                                   # orient outward from 0
            nrm, off = (-nrm[0], -nrm[1], -nrm[2]), -off
        if any(dot(nrm, p) > off + eps for p in pts):
            continue                                  # not a supporting plane
        key = tuple(round(x, 9) for x in (*nrm, off))
        faces.setdefault(key, [p for p in pts if abs(dot(nrm, p) - off) < eps])

    sizes = sorted(len(v) for v in faces.values())
    assert sizes.count(3) == 8 and sizes.count(4) == 6 and len(sizes) == 14, sizes

    total = 0.0
    for (nx, ny, nz, off), verts in faces.items():
        nrm = (nx, ny, nz)
        centre = tuple(sum(v[i] for v in verts) / len(verts) for i in range(3))
        # order the face's vertices by angle around its own centre
        u = sub(verts[0], centre)
        ul = math.sqrt(dot(u, u))
        u = (u[0] / ul, u[1] / ul, u[2] / ul)
        w = cross(nrm, u)
        ring = sorted(verts, key=lambda p: math.atan2(dot(sub(p, centre), w),
                                                      dot(sub(p, centre), u)))
        area = 0.0
        for i in range(1, len(ring) - 1):
            area += math.sqrt(dot(cross(sub(ring[i], ring[0]),
                                        sub(ring[i + 1], ring[0])),
                                  cross(sub(ring[i], ring[0]),
                                        sub(ring[i + 1], ring[0])))) / 2
        total += area * off / 3                       # off is the plane's distance

    edges = sum(len(v) for v in faces.values()) // 2
    assert edges == 24, edges
    return Fraction(total / math.sqrt(2)).limit_denominator(10 ** 6)
