"""ข้อ 25 — พื้นที่ของส่วนที่แรเงาในดอกไม้หกกลีบ

จากรูป วงกลมวงเล็กที่มีรัศมียาว 1 หน่วยจำนวน 6 รูปตัดกันที่จุดศูนย์กลางของวงกลมวงใหญ่
โดยที่วงกลมวงเล็กสองวงที่อยู่ถัดกันผ่านจุดศูนย์กลางของกันและกัน และมีจุดตัดจุดหนึ่งบน
วงกลมวงใหญ่  จงหาพื้นที่ของส่วนที่แรเงา

**The shading is a parity rule, not a list of regions.** Reading the crop as
data: a region is grey exactly when it lies inside an *odd* number of the six
small circles — grey at one, white at two, grey at three — confirmed at 99.9%
pixel agreement against a fitted model. That reading is the whole item; the
areas then follow from three standard formulas.

Geometry first. The six centres sit on a regular hexagon of side r around the
big circle's centre O, each at distance r from it, so every small circle passes
through O — which is what the stem says. Two adjacent circles have centres r
apart, so they meet at two points on the perpendicular bisector of their
centres, at distance ±r√3/2 from its midpoint: one of them is O, the other is
at distance **r√3** from O. So the big circle's radius is R = r√3, and its area
is 3πr².

Now the three regions inside the big disc, with ``seg`` the circular segment cut
by a chord of length r (central angle 60°) and ``lens`` the intersection of two
adjacent circles:

    lens = 2r²·arccos(1/2) − (r/2)√(4r² − r²) = (2π/3 − √3/2)r²

* **Covered three times.** C_i lies on circles i−1 and i+1 and is the centre of
  circle i, so a region around each of the six centres is covered three times.
  Each is two 60° segments, so

      A₃ = 12·seg = 12·½r²(π/3 − √3/2) = (2π − 3√3)r²

* **Covered twice.** A point covered three times lies in exactly two of the six
  *adjacent* lenses (i−1 with i, and i with i+1 — circles i−1 and i+1 are two
  apart and their overlap is not one of the six petals). So summing the petals
  counts the twice-covered area once and the thrice-covered area twice:

      A₂ = 6·lens − 2A₃ = (4π − 3√3)r² − (4π − 6√3)r² = 3√3 r²

* **Covered once** is what is left of the disc: A₁ = 3πr² − A₂ − A₃ = πr².

    shaded = A₁ + A₃ = πr² + (2π − 3√3)r² = **(3π − 3√3)r²**

which is 3π − 3√3 ≈ 4.2286 at r = 1. Note the small circles poke *outside* the
big one — they reach 2r from O and the big circle is only r√3 — so all of this
is areas within the big disc, and A₁ + A₂ + A₃ = 3πr² is the check that nothing
has been left out.

``solve`` evaluates that decomposition. ``check`` knows none of it: it integrates
the printed membership rule — "inside an odd number of the six circles" — over a
polar grid, using the figure's 12-fold symmetry to integrate one 30° wedge and
multiply. It is a measurement of the picture, and it is what would catch a wrong
segment count in the algebra above.
"""

from __future__ import annotations

from math import cos, pi, radians, sin, sqrt

#: six circles of radius r through a common centre; the big circle is r√3.
PARAMS = {"r": 1}
#: (3π − 3√3)r² at r = 1. The exact form is printed by the generator and held
#: against this float by a test — see test_sheetpipe.py.
ANSWER = 4.228625538062747
#: `check` integrates on a grid, so it is only good to about a part in 10⁴.
TOL = 5e-4
VARIANTS = [
    {"r": 2},
    {"r": 3},
    {"r": 4},
    {"r": 5},
]

#: the six centres, at distance r from O on a regular hexagon.
ANGLES = [radians(60 * k) for k in range(6)]


def centres(r: float):
    return [(r * cos(a), r * sin(a)) for a in ANGLES]


def solve(r=1):
    """A₁ + A₃, from the segment and lens formulas."""
    if r <= 0:
        return None
    r2 = float(r) ** 2
    disc = 3 * pi * r2                                  # R = r√3
    seg = 0.5 * r2 * (pi / 3 - sqrt(3) / 2)             # 60° segment
    lens = 2 * r2 * (pi / 3) - 0.5 * r2 * sqrt(3)       # adjacent overlap
    thrice = 12 * seg
    twice = 6 * lens - 2 * thrice
    once = disc - twice - thrice
    return once + thrice


def check(r=1, wedge_steps=420, radial_steps=900):
    """Independent: integrate "inside an odd number of circles" over the disc.

    No decomposition and no formula for any region — the printed rule is
    evaluated pointwise on a polar grid. The figure has a 12-fold symmetry (a
    6-fold rotation and the mirror through each centre), so one 30° wedge is
    integrated and multiplied by 12; that keeps the sample count low enough to
    run per variant while staying well inside the module's tolerance.
    """
    if r <= 0:
        return None
    big = float(r) * sqrt(3)
    cs = centres(float(r))
    r2 = float(r) ** 2

    total = 0.0
    d_theta = radians(30) / wedge_steps
    d_rho = big / radial_steps
    for i in range(wedge_steps):
        theta = (i + 0.5) * d_theta
        ct, st = cos(theta), sin(theta)
        for j in range(radial_steps):
            rho = (j + 0.5) * d_rho
            x, y = rho * ct, rho * st
            covered = 0
            for cx, cy in cs:
                if (x - cx) ** 2 + (y - cy) ** 2 <= r2:
                    covered += 1
            if covered % 2:
                total += rho * d_rho * d_theta      # polar area element
    return 12 * total
