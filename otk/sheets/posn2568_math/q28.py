"""ข้อ 28 — ความยาวส่วนโค้งของสายพานชุดล้อตีนตะขาบ

วงล้อใหญ่ 2 วง รัศมี 3 + 2√2  วงล้อเล็ก 3 วง รัศมี 1 ระยะห่างระหว่างวงล้อเล็กแต่ละคู่
เท่ากับ 1  จงหาความยาวรวมของสายพานเฉพาะส่วนที่เป็นส่วนโค้งของวงกลม

The figure fixes the layout, and two thin dashed lines in it are the whole
specification: one horizontal line tangent to the *bottoms* of both big wheels
and the *tops* of all three small wheels, and vertical lines tangent to the
inner side of each big wheel and the outer side of the outer small wheel. So
with that horizontal line as y = 0:
    small wheels at y = −r, spaced 2r + gap apart;
    big wheels at y = R, at x = ±(R + gap_to_edge) — see :func:`wheels`.

Method: the belt is the boundary of the convex hull of the discs. For a
direction φ the belt touches whichever disc maximises c·u(φ) + r, so the arc
carried by disc i is exactly the set of φ where i wins, and
    total arc = Σ rᵢ · measure{φ : i wins}   with Σ measure = 2π.
Disc i beats j precisely when u·(cᵢ−cⱼ) ≥ rⱼ − rᵢ, which is an *arc* of
directions; intersecting those arcs over all j gives disc i's wrap angle in
closed form. For the sheet's numbers the design makes every angle rational in
degrees — 165° on each big wheel, 15° on each outer small wheel, 0° on the
middle one — giving (17 + 11√2)π/3 ≈ 34.09.

``check`` never intersects an arc: it scans φ, finds which disc actually wins,
and bisects each changeover.
"""

from __future__ import annotations

import math

TOL = 1e-7

TWO_PI = 2 * math.pi

# big_r = 3 + 2√2, the value that makes the tangent angles come out whole.
PARAMS = {"big_r": 5.82842712474619, "small_r": 1, "n_small": 3, "gap": 1}
ANSWER = 34.0929291435895              # (17 + 11√2)π/3
VARIANTS = [
    {"n_small": 2},
    {"n_small": 5},
    {"big_r": 4, "small_r": 1, "n_small": 3, "gap": 1},
    {"big_r": 8, "small_r": 2, "n_small": 4, "gap": 0.5},
    {"big_r": 3, "small_r": 3, "n_small": 3, "gap": 2},
]


def wheels(big_r=5.82842712474619, small_r=1, n_small=3, gap=1):
    """(x, y, r) for every wheel, big ones first.

    The horizontal tangent line is y = 0: big wheels rest their bottoms on it,
    small wheels hang their tops from it. The big wheels are pushed out until a
    vertical line touches both a big wheel's inner side and the outer small
    wheel's outer side — which is what the thin dashed lines in the figure say.
    """
    if n_small < 1:
        raise ValueError("need at least one small wheel")
    step = 2 * small_r + gap
    xs = [(i - (n_small - 1) / 2) * step for i in range(n_small)]
    offset = big_r - xs[0] + small_r
    return ([(-offset, big_r, big_r), (offset, big_r, big_r)]
            + [(x, -small_r, small_r) for x in xs])


def _intersect(spans, arc):
    """Intersect a list of [lo, hi] ⊂ [0, 2π) with one more (possibly wrapping)."""
    lo, hi = arc
    pieces = ([(lo % TWO_PI, hi % TWO_PI)] if (hi - lo) < TWO_PI
              and (lo % TWO_PI) <= (hi % TWO_PI)
              else [(lo % TWO_PI, TWO_PI), (0.0, hi % TWO_PI)])
    if hi - lo >= TWO_PI:
        return spans
    out = []
    for a, b in spans:
        for c, d in pieces:
            left, right = max(a, c), min(b, d)
            if right > left:
                out.append((left, right))
    return out


def wrap_angles(disks) -> list[float]:
    """Wrap angle of each disc on the belt, in radians."""
    angles = []
    for i, (xi, yi, ri) in enumerate(disks):
        spans = [(0.0, TWO_PI)]
        for j, (xj, yj, rj) in enumerate(disks):
            if i == j:
                continue
            wx, wy = xi - xj, yi - yj
            width = math.hypot(wx, wy)
            need = rj - ri
            if width == 0:                     # concentric: the larger wins all
                spans = spans if ri >= rj else []
                continue
            ratio = need / width
            if ratio > 1:
                spans = []
            elif ratio >= -1:
                alpha = math.atan2(wy, wx)
                delta = math.acos(ratio)
                spans = _intersect(spans, (alpha - delta, alpha + delta))
            if not spans:
                break
        angles.append(sum(b - a for a, b in spans))
    return angles


def solve(big_r=5.82842712474619, small_r=1, n_small=3, gap=1):
    """Total belt length that runs along wheel arcs."""
    disks = wheels(big_r, small_r, n_small, gap)
    angles = wrap_angles(disks)
    total_turn = sum(angles)
    if abs(total_turn - TWO_PI) > 1e-7:
        raise ValueError(f"wrap angles sum to {total_turn}, not 2π — the belt "
                         "is not a simple convex loop for these wheels")
    return sum(r * theta for (_, _, r), theta in zip(disks, angles))


def check(big_r=5.82842712474619, small_r=1, n_small=3, gap=1, samples=20000):
    """Independent: scan directions, find the winner, bisect each changeover."""
    disks = wheels(big_r, small_r, n_small, gap)

    def winner(phi: float) -> int:
        ux, uy = math.cos(phi), math.sin(phi)
        return max(range(len(disks)),
                   key=lambda k: disks[k][0] * ux + disks[k][1] * uy + disks[k][2])

    edges, previous = [], winner(0.0)
    for s in range(1, samples + 1):
        phi = TWO_PI * s / samples
        here = winner(phi)
        if here != previous:
            lo, hi = TWO_PI * (s - 1) / samples, phi
            for _ in range(80):
                mid = (lo + hi) / 2
                if winner(mid) == previous:
                    lo = mid
                else:
                    hi = mid
            edges.append(((lo + hi) / 2, previous, here))
            previous = here
    if not edges:                              # a single disc swallows the rest
        return TWO_PI * max(r for _, _, r in disks)

    total = 0.0
    for idx, (phi, leaving, _) in enumerate(edges):
        start = edges[idx - 1][0] if idx else edges[-1][0] - TWO_PI
        total += disks[leaving][2] * (phi - start)
    return total
