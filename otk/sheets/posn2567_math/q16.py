"""ข้อ 16 — ขนาดของ ∠BND ในรูปหกเหลี่ยมด้านเท่ามุมเท่า

จากรูป ABCDEF เป็นรูปหกเหลี่ยมด้านเท่ามุมเท่า  BN̅ ตัด AC̅ ที่จุด M และพบกับ CE̅
ที่จุด N และ ND̅ พบกับ CE̅ ที่จุด N  ถ้า AM = CN แล้วขนาดของ ∠BND เท่ากับกี่องศา

รูปประกอบ (extract/figures/item16.png), read as follows: the hexagon is lettered
A, B, C, D, E, F **going clockwise** from the top left, the drawn segments are
AC̅, CE̅, the line from B through M to N, and ND̅ — so M is inside the hexagon on
AC̅, N is on CE̅, and the order along the line is B, M, N.

The answer is a rotation, not a computation. Let ρ be the rotation about the
centre by two vertices' worth of turn, 2·(360/n). On the hexagon that is 120°,
and it maps

    A → C,   B → D,   C → E

so it maps the segment AC̅ onto CE̅ and, because it preserves distance, it takes
the point M (at distance AM from A) to the point at distance AM from C — which
is exactly N, since AM = CN. So ρ takes the vector M→B to N→D, and

    ∠BND = ∠(N→B, N→D) = ∠(M→B, N→D) = 2·(360/n) = 720/n degrees

using that B, M, N are collinear in that order, which makes N→B and M→B the same
direction. **AM never appears** — the answer is the same wherever M sits, and the
collinearity condition is only what pins the figure down.

That generalises: A…E may be five consecutive vertices of any regular n-gon with
n ≥ 5, and the answer is 720/n. ``check`` builds such an n-gon, finds the M that
actually makes AM = CN, and measures the angle.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: number of sides of the regular polygon; the sheet's is a hexagon.
PARAMS = {"sides": 6}
ANSWER = Fraction(120)
VARIANTS = [
    {"sides": 5},
    {"sides": 8},
    {"sides": 9},
    {"sides": 12},
    {"sides": 20},
    {"sides": 4},          # degenerate: with only four vertices there is no E
]
TOL = 1e-6


def solve(sides=6):
    """∠BND = 720/n degrees — independent of where M lies on AC̅."""
    if sides < 5:
        return None
    return Fraction(720, sides)


def _ang(p, q, r) -> float:
    a = (p[0] - q[0], p[1] - q[1])
    b = (r[0] - q[0], r[1] - q[1])
    cos = (a[0] * b[0] + a[1] * b[1]) / (math.hypot(*a) * math.hypot(*b))
    return math.degrees(math.acos(max(-1.0, min(1.0, cos))))


def _meet(p1, p2, p3, p4):
    """Where line p1p2 meets line p3p4."""
    d1 = (p2[0] - p1[0], p2[1] - p1[1])
    d2 = (p4[0] - p3[0], p4[1] - p3[1])
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-15:
        return None
    t = ((p3[0] - p1[0]) * d2[1] - (p3[1] - p1[1]) * d2[0]) / den
    return (p1[0] + t * d1[0], p1[1] + t * d1[1])


def check(sides=6):
    """Independent: build the polygon, hunt for the M that makes AM = CN, measure.

    Nothing here knows about the rotation. N is slid along CE̅ until the line BN
    cuts AC̅ at a point M with AM = CN — the figure's own condition — and then
    ∠BND is read off the coordinates.

    Sliding N rather than M matters: as M crosses AC̅ the line BM passes through
    the direction parallel to CE̅, so CN has a pole in the middle of the range and
    a bisection can converge on the wrong branch. Along CE̅ the same difference is
    monotone and finite.
    """
    if sides < 5:
        return None
    n = int(sides)
    v = [(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n))
         for k in range(n)]
    a, b, c, d, e = v[0], v[1], v[2], v[3], v[4]

    def gap(u: float):
        """CN - AM for N a fraction u of the way along CE̅."""
        nn = (c[0] + u * (e[0] - c[0]), c[1] + u * (e[1] - c[1]))
        m = _meet(b, nn, a, c)
        if m is None:
            return None, None, None
        return math.dist(c, nn) - math.dist(a, m), m, nn

    lo, hi = 1e-9, 1 - 1e-9
    g_lo, *_ = gap(lo)
    g_hi, *_ = gap(hi)
    if g_lo is None or g_hi is None or g_lo > 0 or g_hi < 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        g, *_ = gap(mid)
        if g is None:
            return None
        if g < 0:
            lo = mid
        else:
            hi = mid
    g, m, nn = gap((lo + hi) / 2)
    assert abs(g) < 1e-9, "AM = CN was not reached"
    # B, M, N collinear, and N really is on CE̅ — the figure's own claims.
    cross = ((m[0] - b[0]) * (nn[1] - b[1]) - (m[1] - b[1]) * (nn[0] - b[0]))
    assert abs(cross) < 1e-9
    assert abs(_ang(c, nn, e) - 180) < 1e-6
    return Fraction(_ang(b, nn, d)).limit_denominator(10 ** 6)
