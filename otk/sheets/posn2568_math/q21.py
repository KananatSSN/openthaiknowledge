"""ข้อ 21 — วงกลมสองวงกับเส้นสัมผัสร่วมสองเส้น

วงกลมเล็กรัศมี a วงกลมใหญ่รัศมี b  เส้นตรง l₁ สัมผัสวงกลมเล็กที่ A และวงกลมใหญ่ที่ B
เส้นตรง l₂ สัมผัสวงกลมเล็กที่ C และวงกลมใหญ่ที่ D  โดยที่ AB = 16 และ CD = 20
ถ้า b − a = 2 แล้วค่าของ a² + b² เท่ากับเท่าใด

Method (this is what the figure has to be read for): l₂ is the *external* common
tangent — both circles sit on the same side of it — while l₁ crosses between
them and is the *internal* one. Their tangent-segment lengths in the centre
distance d are
    CD² = d² − (b−a)²        (external)
    AB² = d² − (a+b)²        (internal)
Eliminating d gives (a+b)² = CD² − AB² + (b−a)², so
    a² + b² = ((a+b)² + (b−a)²) / 2 = (CD² − AB² + 2(b−a)²) / 2 = 76.

``check`` writes down no tangent-length formula. It puts the circles in
coordinates, builds each common tangent from its unit normal u (the tangent
points are then literally c ± r·u), measures the distance between the two touch
points, and bisects on the radius until the constructed |AB| equals the given
one.
"""

from __future__ import annotations

import math
from fractions import Fraction

TOL = 1e-7

PARAMS = {"ab": 16, "cd": 20, "diff": 2}
ANSWER = 76
VARIANTS = [
    {"ab": 6, "cd": 10, "diff": 1},
    {"ab": 8, "cd": 17, "diff": 3},
    {"ab": 12, "cd": 13, "diff": 0},
    {"ab": 16, "cd": 20, "diff": 5},
    {"ab": 5, "cd": 30, "diff": 4},
]


def radii(ab=16, cd=20, diff=2):
    """(a, b) — the small and the large radius."""
    sum_sq = cd * cd - ab * ab + diff * diff         # (a+b)²
    if sum_sq <= diff * diff:
        raise ValueError("no such pair of circles: internal tangent too long")
    total = math.sqrt(sum_sq)
    return ((total - diff) / 2, (total + diff) / 2)


def solve(ab=16, cd=20, diff=2):
    """a² + b², kept exact — every step is rational in the given lengths."""
    value = Fraction(cd * cd - ab * ab + 2 * diff * diff, 2)
    if value <= 0:
        raise ValueError("no such pair of circles")
    return value


def tangent_span(d: float, r1: float, r2: float, internal: bool) -> float:
    """Distance between the two touch points of one common tangent.

    Built from the tangent's unit normal u: for the external tangent both
    centres lie r away on the *same* side (u·(c₁−c₂) = r₂−r₁), for the internal
    one on opposite sides (u·(c₁−c₂) = r₁+r₂). The touch points then are just
    c ± r·u, and the answer is the distance between them.
    """
    offset = (r1 + r2) if internal else (r2 - r1)
    ux = -offset / d                                  # from u·(−d, 0) = offset
    if abs(ux) > 1:
        raise ValueError("circles admit no such common tangent")
    uy = math.sqrt(1 - ux * ux)
    if internal:
        p1 = (-r1 * ux, -r1 * uy)                     # c₁ is +r₁ along u
        p2 = (d + r2 * ux, r2 * uy)                   # c₂ is −r₂ along u
    else:
        p1 = (r1 * ux, r1 * uy)
        p2 = (d + r2 * ux, r2 * uy)
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def check(ab=16, cd=20, diff=2):
    """Independent: construct both tangents, then bisect the radius to fit."""
    # The external tangent involves only d and the radius difference, so d is
    # read straight off CD — but measured, not assumed.
    d = math.sqrt(cd * cd + diff * diff)
    probe = 1.0
    assert abs(tangent_span(d, probe, probe + diff, internal=False) - cd) < 1e-9,\
        "constructed external tangent does not reproduce CD"

    def residual(a: float) -> float:
        return tangent_span(d, a, a + diff, internal=True) - ab

    lo, hi = 1e-9, (d - diff) / 2 - 1e-9              # a + b < d
    if residual(lo) * residual(hi) > 0:
        raise ValueError("no radius reproduces the given AB")
    for _ in range(300):
        mid = (lo + hi) / 2
        if residual(lo) * residual(mid) <= 0:
            hi = mid
        else:
            lo = mid
    a = (lo + hi) / 2
    return a * a + (a + diff) ** 2
