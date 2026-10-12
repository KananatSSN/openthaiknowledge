"""ข้อ 13 — ความยาว OA ในพีระมิดฐานสามเหลี่ยม

กำหนดให้ ABCD เป็นพีระมิดฐานสามเหลี่ยมซึ่งมีรูปสามเหลี่ยม BCD เป็นฐาน โดยที่
AB = AC = AD = 1 หน่วย และ ∠BAC = 60°, ∠BAD = 90°, ∠CAD = 120°
ถ้า O เป็นจุดบนฐานของพีระมิดที่ทำให้ ∠AOB = ∠AOC = ∠AOD = 90° แล้ว OA มีค่า
เท่ากับกี่หน่วย

∠AOB = ∠AOC = ∠AOD = 90° says OA̅ is perpendicular to three lines of the base
plane, so **OA̅ is the altitude from A** and O is its foot. (It also forces
OB = OC = OD, so O is the circumcentre of △BCD — a useful cross-check, not the
route.)

Take unit vectors u, v, w along AB̅, AC̅, AD̅ with u·v = cos 60°, u·w = cos 90°,
v·w = cos 120°. Their Gram determinant is 1/2, so

    V = (1/6)√(det G) = 1/(6√2)

and the base triangle has sides |BC| = 1, |BD| = √2, |CD| = √3 — a right triangle
at B, of area √2/2. The altitude is 3V/area:

    OA = 3·(1/(6√2)) / (√2/2) = **1/2**.

The value is irrational for most angle triples, so ``ANSWER`` is recorded as the
float ``solve`` returns and the sheet's exact 1/2 lives in ``sheet.json``'s note.
"""

from __future__ import annotations

import math

#: the three face angles at the apex, in degrees, and the common edge length.
PARAMS = {"bac": 60, "bad": 90, "cad": 120, "edge": 1}
ANSWER = 0.5
VARIANTS = [
    {"bac": 60, "bad": 60, "cad": 60},          # regular tetrahedron
    {"bac": 90, "bad": 90, "cad": 90},          # the corner of a cube
    {"bac": 60, "bad": 90, "cad": 120, "edge": 4},
    {"bac": 50, "bad": 70, "cad": 100},
    {"bac": 10, "bad": 10, "cad": 170},         # degenerate: flat at the apex
]
TOL = 1e-9


def solve(bac=60, bad=90, cad=120, edge=1):
    """OA = 3V / [BCD], the altitude from the apex."""
    if edge <= 0 or min(bac, bad, cad) <= 0 or max(bac, bad, cad) >= 180:
        return None
    ab, ac, ad = (math.cos(math.radians(a)) for a in (bac, bad, cad))
    gram = 1 - ab * ab - ac * ac - ad * ad + 2 * ab * ac * ad
    if gram <= 1e-12:                       # the three edges are coplanar
        return None
    volume = edge ** 3 * math.sqrt(gram) / 6

    def side(cos_theta):
        return edge * math.sqrt(2 - 2 * cos_theta)

    bc, bd, cd = side(ab), side(ac), side(ad)
    s = (bc + bd + cd) / 2
    area = math.sqrt(max(0.0, s * (s - bc) * (s - bd) * (s - cd)))
    if area <= 0:
        return None
    return 3 * volume / area


def check(bac=60, bad=90, cad=120, edge=1):
    """Independent: place the three edges in coordinates and drop a perpendicular.

    u, v and w are built by hand so their pairwise angles are the stated ones,
    the base plane's normal comes from a cross product, and OA is the distance
    from the apex to that plane. The construction asserts the three angles back,
    and asserts that the foot really is equidistant from B, C and D — the
    circumcentre fact ``solve`` never uses.
    """
    if edge <= 0 or min(bac, bad, cad) <= 0 or max(bac, bad, cad) >= 180:
        return None
    ab, ac, ad = (math.cos(math.radians(a)) for a in (bac, bad, cad))
    u = (1.0, 0.0, 0.0)
    v = (ab, math.sqrt(max(0.0, 1 - ab * ab)), 0.0)
    if v[1] < 1e-12:
        return None
    wx = ac
    wy = (ad - ab * ac) / v[1]
    wz2 = 1 - wx * wx - wy * wy
    if wz2 <= 1e-12:
        return None
    w = (wx, wy, math.sqrt(wz2))

    def dot(p, q):
        return sum(a * b for a, b in zip(p, q))

    for p, q, want in ((u, v, ab), (u, w, ac), (v, w, ad)):
        assert abs(dot(p, q) - want) < 1e-9

    b, c, d = (tuple(edge * t for t in vec) for vec in (u, v, w))
    e1 = tuple(c[i] - b[i] for i in range(3))
    e2 = tuple(d[i] - b[i] for i in range(3))
    normal = (e1[1] * e2[2] - e1[2] * e2[1],
              e1[2] * e2[0] - e1[0] * e2[2],
              e1[0] * e2[1] - e1[1] * e2[0])
    length = math.sqrt(dot(normal, normal))
    if length < 1e-12:
        return None
    dist = abs(dot(b, normal)) / length            # A is the origin
    foot = tuple(-dist * normal[i] / length if dot(b, normal) > 0
                 else dist * normal[i] / length for i in range(3))
    dists = [math.dist(foot, p) for p in (b, c, d)]
    assert max(dists) - min(dists) < 1e-6, dists   # O is the circumcentre
    return dist
