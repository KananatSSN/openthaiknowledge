"""ข้อ 5 — ความยาวรัศมี r ของทรงกลม

กล่องทรงสี่เหลี่ยมมุมฉากใบหนึ่งบรรจุแนบในทรงกลมที่มีรัศมี r หน่วย ถ้ากล่องใบนี้มี
พื้นที่ผิวทั้ง 6 ด้านรวมกันเท่ากับ 384 ตารางหน่วย และผลรวมของความยาวสันกล่องทั้ง
12 สัน เท่ากับ 112 หน่วย จงหาความยาวรัศมี r

A box inscribed in a sphere has the sphere's *diameter* as its space diagonal, so
``(2r)² = a² + b² + c²`` — and that is exactly the combination the two printed
totals hand over:

    12 edges:  4(a + b + c) = 112  ⟹  a + b + c  = 28
    6 faces:   2(ab+bc+ca) = 384   ⟹  ab+bc+ca   = 192
    a² + b² + c² = 28² − 2·192 = 784 − 384 = 400

so ``2r = 20`` and **r = 10**. The individual edges are never needed — and are
not even determined; many boxes fit both totals and they all share a diagonal,
which is precisely why the question can ask for r.

``solve`` uses the identity. ``check`` refuses to: it constructs actual edge
lengths matching both printed totals from several different starting points and
measures the diagonal of each box it builds.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt, sqrt

#: total area over all 6 faces, and total length over all 12 edges.
PARAMS = {"surface": 384, "edges": 112}
ANSWER = 10
VARIANTS = [
    {"surface": 208, "edges": 96},
    {"surface": 96, "edges": 48},            # the cube of side 4
    {"surface": 550, "edges": 120},
    {"surface": 784, "edges": 112},          # a² + b² + c² = 0: degenerate
    {"surface": 1000, "edges": 112},         # would need a negative sum of squares
    {"surface": 384, "edges": 113},
]


def solve(surface=384, edges=112):
    """r = √(a² + b² + c²)/2, read off the two symmetric totals."""
    if edges <= 0 or surface < 0:
        return None
    perimeter = Fraction(edges, 4)          # a + b + c
    pairwise = Fraction(surface, 2)         # ab + bc + ca
    squares = perimeter * perimeter - 2 * pairwise
    if squares <= 0:
        return None
    value = squares / 4
    if value.denominator == 1:
        root = isqrt(value.numerator)
        if root * root == value.numerator:
            return root
    return sqrt(float(value))


def check(surface=384, edges=112):
    """Independent: build real edge lengths that fit, then measure the diagonal.

    One edge is fixed at a share of the total, the other two come from solving
    the quadratic their sum and product force, and both printed totals are
    verified on the box that results. Several shares are used; a radius is
    reported only if every admissible box gives the same one — which is the claim
    the closed form makes.
    """
    if edges <= 0 or surface < 0:
        return None
    total = edges / 4
    pairwise = surface / 2

    radii = []
    for share in (1 / 6, 0.25, 1 / 3, 0.5, 0.7):
        a = total * share
        rest = total - a                       # b + c
        product = pairwise - a * rest          # bc
        disc = rest * rest - 4 * product
        if disc < -1e-9:
            continue
        disc = max(disc, 0.0)          # a cube lands exactly on the double root
        b = (rest + sqrt(disc)) / 2
        c = rest - b
        if min(a, b, c) <= 0:
            continue
        if (abs(4 * (a + b + c) - edges) > 1e-7
                or abs(2 * (a * b + b * c + c * a) - surface) > 1e-6):
            continue
        radii.append(sqrt(a * a + b * b + c * c) / 2)
    if not radii or max(radii) - min(radii) > 1e-7:
        return None
    got = sum(radii) / len(radii)
    return round(got) if abs(got - round(got)) < 1e-9 else got
