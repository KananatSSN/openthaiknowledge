"""ข้อ 25 — ขนาดของ ∠ABC ในรูปสามเหลี่ยมมุมฉาก

ABC เป็นรูปสามเหลี่ยมมุมฉากที่มี ∠BCA = 90°  ให้ P เป็นจุดบน AB̅ ที่ทำให้
    1/AP + 1/BP = 2/CP
ถ้า ∠ACP = 41° แล้วขนาดของ ∠ABC เท่ากับกี่องศา

Method: write α = ∠ACP and β = ∠ABC. The sine rule in the two sub-triangles
gives AP = CP·sin α / cos β and BP = CP·cos α / sin β, so the condition becomes
    cos β / sin α + sin β / cos α = 2   ⟺   cos(β − α) = sin 2α,
whose solutions are β = 90° − α and β = 3α − 90°.

**Both are genuine.** β = 90° − α is the degenerate branch: it makes P the
midpoint of the hypotenuse, where CP = AP = BP and the condition holds in *any*
right triangle — so it carries no information about α at all. The intended
answer is the other branch, 3α − 90° = 33°. A generator built on this must say
"P ไม่ใช่จุดกึ่งกลางของ AB̅" out loud, or the item has two correct choices;
:data:`SHEET_NOTE` records that, and ``solutions()`` returns both.

``check`` constructs the triangle for candidate β, locates P by intersecting the
ray at α from C with AB, evaluates 1/AP + 1/BP − 2/CP numerically, and scans for
sign changes — then discards the midpoint branch by testing P against the
midpoint rather than by using the formula.
"""

from __future__ import annotations

import math

TOL = 1e-6

SHEET_NOTE = ("the condition also holds for β = 90° − α (P the midpoint of the "
              "hypotenuse); the non-degenerate branch needs P ≠ midpoint stated")

PARAMS = {"alpha_deg": 41}
ANSWER = 33.0
VARIANTS = [
    {"alpha_deg": 50},
    {"alpha_deg": 35},
    {"alpha_deg": 55},
    {"alpha_deg": 44},        # not 45: there the two branches coincide
    {"alpha_deg": 38},
]


def solutions(alpha_deg=41) -> tuple[float, float]:
    """(non-degenerate β, degenerate β) in degrees."""
    return (3 * alpha_deg - 90.0, 90.0 - alpha_deg)


def solve(alpha_deg=41):
    """∠ABC in degrees, on the branch where P is not the midpoint of AB."""
    beta = 3 * alpha_deg - 90.0
    if not 0 < beta < 90:
        raise ValueError(f"α = {alpha_deg}° puts β outside a right triangle")
    if abs(beta - (90 - alpha_deg)) < 1e-9:
        raise ValueError("the two branches coincide at α = 45°")
    return beta


def _geometry(beta_deg: float, alpha_deg: float):
    """Build the triangle and P; return (AP, BP, CP)."""
    beta = math.radians(beta_deg)
    c = (0.0, 0.0)                                   # right angle at C
    a = (math.tan(beta), 0.0)                        # CA along x, CB along y
    b = (0.0, 1.0)
    ray = math.radians(alpha_deg)                    # ∠ACP measured off CA
    # P = intersection of the ray from C with the segment AB
    #   AB: (x, y) = A + t(B − A);  ray: y = x·tan(ray)
    dx, dy = b[0] - a[0], b[1] - a[1]
    denom = dy - math.tan(ray) * dx
    t = (math.tan(ray) * a[0] - a[1]) / denom
    p = (a[0] + t * dx, a[1] + t * dy)
    return (math.dist(a, p), math.dist(b, p), math.dist(c, p), p, a, b)


def check(alpha_deg=41):
    """Independent: numeric sweep of β for roots of 1/AP + 1/BP − 2/CP."""
    def residual(beta_deg: float) -> float:
        ap, bp, cp, *_ = _geometry(beta_deg, alpha_deg)
        return 1 / ap + 1 / bp - 2 / cp

    roots, step, lo = [], 0.05, 1.0
    while lo < 89.0:
        hi = lo + step
        try:
            f_lo, f_hi = residual(lo), residual(hi)
        except (ZeroDivisionError, ValueError):
            lo = hi
            continue
        if f_lo == 0 or f_lo * f_hi < 0:
            a, b = lo, hi
            for _ in range(200):
                mid = (a + b) / 2
                if residual(a) * residual(mid) <= 0:
                    b = mid
                else:
                    a = mid
            roots.append((a + b) / 2)
        lo = hi

    # Drop the branch whose P is the hypotenuse midpoint — tested on the point,
    # not on the formula.
    keep = []
    for beta in roots:
        _, _, _, p, a, b = _geometry(beta, alpha_deg)
        midpoint = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        if math.dist(p, midpoint) > 1e-6:
            keep.append(beta)
    if len(keep) != 1:
        raise ValueError(f"expected one non-degenerate β, got {keep}")
    return keep[0]
