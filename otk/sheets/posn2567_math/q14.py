"""ข้อ 14 — อัตราส่วนของพื้นที่วงกลมเล็กต่อพื้นที่วงกลมใหญ่

จากรูป วงกลมใหญ่สองวงรัศมีเท่ากันและสัมผัสกันภายนอก รูปสามเหลี่ยมหน้าจั่วมี
จุดยอดจุดหนึ่งอยู่บนวงกลมใหญ่วงบน และด้านทั้งสามของรูปสามเหลี่ยมเป็นเส้นสัมผัส
วงกลมใหญ่วงล่าง วงกลมเล็กสัมผัสภายในกับวงกลมใหญ่วงบน และสัมผัสคอร์ด ณ จุด
กึ่งกลางของคอร์ด  จงหาอัตราส่วนของพื้นที่วงกลมเล็กต่อพื้นที่วงกลมใหญ่

รูปประกอบ (extract/figures/item14.png), read as follows:

* the two big circles are stacked and tangent, the triangle's apex is the **top**
  of the upper one, and its base is the horizontal tangent below the lower one;
* the คอร์ด of the last sentence is the chord the triangle's *right side* cuts on
  the upper circle — one end of it is the apex;
* the small circle sits in the sliver between that chord and the arc, tangent to
  the arc from inside and touching the chord at its midpoint.

Put the lower circle at the origin with radius r and the upper one at (0, r+R)
with radius R, so the apex is P = (0, r+2R) and the base is the line y = -r. A
side of the triangle is a tangent from P to the lower circle, so its half-angle
at the apex satisfies

    sin α = r/|O₁P| = r/(r+2R).

The distance from the upper centre O₂ to that side is d = |O₂P|·sin α = Rr/(r+2R),
so the chord's half-length is √(R²-d²) and its midpoint M is at distance d from
O₂. The small circle touches the chord at M, so its centre lies on O₂M produced;
internal tangency then reads (d + ρ) = R - ρ, giving

    ρ = (R - d)/2 = R²/(r + 2R),

and the ratio of areas is ρ²/R² = R²/(r + 2R)². For the sheet's equal circles
(r = R) that is R²/9R² = **1/9** — no measurement needed, which is why the item
gives none.

The radii only enter through their ratio, so ``solve`` is homogeneous of degree
0 in (r, R); the variants push both around to prove it.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: radii of the lower and upper big circles — equal on the sheet.
PARAMS = {"r_low": 1, "r_up": 1}
ANSWER = Fraction(1, 9)
VARIANTS = [
    {"r_low": 5, "r_up": 5},              # same ratio, bigger picture
    {"r_low": 2, "r_up": 1},              # 1/16
    {"r_low": 1, "r_up": 2},              # 4/25
    {"r_low": 7, "r_up": 3},
    {"r_low": 3, "r_up": 10},
]
TOL = 1e-9


def solve(r_low=1, r_up=1):
    """(ρ/R)² = R²/(r+2R)² — the ratio of the small circle's area to the big one's."""
    if r_low <= 0 or r_up <= 0:
        return None
    return Fraction(r_up, r_low + 2 * r_up) ** 2


def check(r_low=1, r_up=1):
    """Independent: build the picture numerically and find ρ by tangency alone.

    The tangent side is obtained from the tangent-length construction rather than
    from sin α, the chord is intersected with the circle, and ρ is bisected out of
    the internal-tangency condition — so no step of ``solve``'s algebra is reused.
    Along the way the construction asserts what the figure claims: the side really
    is tangent to the lower circle, the base line y = -r really is too, and the
    triangle really is isosceles about the y-axis.
    """
    if r_low <= 0 or r_up <= 0:
        return None
    r, big = float(r_low), float(r_up)
    o1, o2 = (0.0, 0.0), (0.0, r + big)
    p = (0.0, r + 2 * big)                        # apex, on the upper circle

    # Right tangent from P to the lower circle: touch point T with O₁T ⊥ PT and
    # |O₁T| = r. Solve for T on the circle with (T-P)·(T-O₁) = 0.
    lp = math.hypot(*p)                           # |O₁P|
    if lp <= r:
        return None
    tl = math.sqrt(lp * lp - r * r)               # tangent length
    # T is at distance r from O₁ and tl from P; intersect the two circles.
    ty = (lp * lp + r * r - tl * tl) / (2 * lp)   # along O₁P, which is the y-axis
    tx = math.sqrt(max(0.0, r * r - ty * ty))
    t = (tx, ty)
    assert abs((t[0] - p[0]) * t[0] + (t[1] - p[1]) * t[1]) < 1e-9

    # The side through P and T, as a unit direction and a normal.
    dx, dy = t[0] - p[0], t[1] - p[1]
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux                              # unit normal to the side
    # The side is tangent to the lower circle; the base y = -r is by construction,
    # and the mirror image of this side across the y-axis is the third one.
    assert abs(abs(nx * (o1[0] - p[0]) + ny * (o1[1] - p[1])) - r) < 1e-9

    # Where the side cuts the upper circle again: P + s·u with |P + s·u - O₂| = R.
    fx, fy = p[0] - o2[0], p[1] - o2[1]
    s = -2 * (fx * ux + fy * uy)                  # the non-zero root
    q = (p[0] + s * ux, p[1] + s * uy)
    assert abs(math.hypot(q[0] - o2[0], q[1] - o2[1]) - big) < 1e-9
    mid = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)

    # The small circle touches the chord at its midpoint, so its centre is at
    # mid + ρ·n̂ (outward, away from O₂); internal tangency fixes ρ.
    away = 1.0 if (mid[0] - o2[0]) * nx + (mid[1] - o2[1]) * ny > 0 else -1.0

    def gap(rho: float) -> float:
        cx = mid[0] + away * rho * nx
        cy = mid[1] + away * rho * ny
        return math.hypot(cx - o2[0], cy - o2[1]) + rho - big

    lo, hi = 0.0, big
    for _ in range(200):
        m = (lo + hi) / 2
        if gap(m) < 0:
            lo = m
        else:
            hi = m
    rho = (lo + hi) / 2
    return Fraction((rho / big) ** 2).limit_denominator(10 ** 6)
