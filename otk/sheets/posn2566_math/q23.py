"""ข้อ 23 — ค่าของ EG/ED เมื่อ A เป็นจุดศูนย์กลางของวงกลมวงเล็ก

จากรูป กำหนด A เป็นจุดศูนย์กลางของวงกลมวงเล็ก ถ้า AB = 3 และ BC = CD = 2 และ
GD ตั้งฉากกับ CF  จงหาค่าของ EG/ED  (เขียนคำตอบเป็นเศษส่วนอย่างต่ำ)

**Everything here is in the drawing, and the drawing had to be read as data.**
Pulling the page's vector art apart (``page.get_drawings()``) gives two conics
and six segments, and testing each labelled point against each conic settles the
incidences that the text never states:

* the small circle is centred at **A**, and **A itself lies on the big circle**;
* **B** is on *both* circles — it is their intersection;
* **C** is on the small circle only, so AC = AB and ABC is isosceles;
* **E, F, G** are on the big circle;
* the drawn segments are AB, AE, AF, EG, BG, FG — so **A, C, D, F are
  collinear** (C and D lie on AF) and **B, C, G are collinear** (BG passes
  through C). D is where EG crosses AF, and the right angle is marked there.

That collinearity of B, C, G is the constraint the stem never spells out, and
without it the big circle's radius is free and EG/ED is not a number at all.

With it, three steps:

**1. GC = GF.** ∠GFC = ∠GFA and ∠GBA are inscribed in the big circle on the same
arc GA, so they are equal; ∠GCF is vertical to ∠BCA; and AB = AC makes
∠BCA = ∠CBA = ∠GBA. So ∠GCF = ∠GFC and triangle GCF is isosceles.

**2. Hence D is the midpoint of CF**, because GD ⊥ CF drops from the apex of an
isosceles triangle — so CF = 2·CD, and with A–C–D–F collinear, AF = AB + 2·CD.
(On the sheet: CF = 4, AF = 7, DF = CD = 2.)

**3. Two powers of a point finish it.** C is inside the big circle on the chords
A–F and B–G, so

    CA·CF = CB·CG   ⟹   GC = GF = 2·AB·CD / BC          (= 6 on the sheet)

and D is inside it on the chords A–F and E–G, so

    ED·DG = DA·DF = (AB + CD)·CD                        (= 10 on the sheet)

Then GD² = GF² − DF² by Pythagoras at D, and

    EG/ED = 1 + DG/ED = 1 + DG²/(ED·DG)
          = 1 + CD(4·AB² − BC²) / (BC²(AB + CD))

At AB = 3, BC = CD = 2 that is 1 + 2·32/(4·5) = 1 + 16/5 = **21/5**.

Note what is *not* needed: the big circle's radius never appears, even though it
is what the collinearity pins down (it comes out ≈ 4.0039 — not a nice number,
which is why the closed form goes through the powers instead).

``solve`` evaluates that formula in exact fractions. ``check`` knows none of it:
it puts A at the origin, treats the big radius as an unknown, **bisects it until
GD really is perpendicular to CF**, and then measures EG and ED off the figure it
built. It never assumes GC = GF or that D is a midpoint — those come out of the
construction, and it audits both before returning.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: AB is the small circle's radius, BC the chord to C, CD the step along CF.
PARAMS = {"ab": 3, "bc": 2, "cd": 2}
ANSWER = Fraction(21, 5)
TOL = 1e-6
VARIANTS = [
    {"ab": 4, "bc": 3, "cd": 3},
    {"ab": 5, "bc": 4, "cd": 4},
    {"ab": 2, "bc": 1, "cd": 1},
    {"ab": 6, "bc": 5, "cd": 5},
    {"ab": 5, "bc": 2, "cd": 3},
    {"ab": 4, "bc": 3, "cd": 1},
]


def solve(ab=3, bc=2, cd=2):
    """1 + CD(4·AB² − BC²) / (BC²(AB + CD))."""
    ab, bc, cd = Fraction(ab), Fraction(bc), Fraction(cd)
    if min(ab, bc, cd) <= 0 or bc > 2 * ab:
        return None                       # BC is a chord of the small circle
    if 2 * ab * cd <= bc * cd:
        return None                       # GF must exceed DF
    gf = 2 * ab * cd / bc
    if gf <= cd:
        return None
    return 1 + (gf * gf - cd * cd) / (cd * (ab + cd))


def _configuration(radius, ab, bc, cd):
    """The whole figure for a candidate big-circle radius, or None.

    A is at the origin and the big circle's centre on the +x axis, so A lies on
    it by construction. B is the upper intersection of the two circles, C is B
    turned about A by the chord BC, F is where the ray AC meets the big circle
    again, D is CD further along, and G is where the line BC meets the big
    circle again. Nothing is assumed about where D lands.
    """
    if radius <= 0:
        return None
    centre = (radius, 0.0)
    bx = ab * ab / (2 * radius)
    if ab * ab - bx * bx <= 0:
        return None
    b = (bx, math.sqrt(ab * ab - bx * bx))
    half = bc / (2 * ab)
    if half >= 1:
        return None
    turn = -2 * math.asin(half)                    # C is clockwise from B
    c = (b[0] * math.cos(turn) - b[1] * math.sin(turn),
         b[0] * math.sin(turn) + b[1] * math.cos(turn))
    ux, uy = c[0] / ab, c[1] / ab
    af = 2 * (centre[0] * ux + centre[1] * uy)     # A is on the circle
    if af <= ab + cd:
        return None
    f = (af * ux, af * uy)
    d = (c[0] + cd * ux, c[1] + cd * uy)

    dx, dy = c[0] - b[0], c[1] - b[1]
    length = math.hypot(dx, dy)
    if length < 1e-12:
        return None
    dx, dy = dx / length, dy / length
    ox, oy = b[0] - centre[0], b[1] - centre[1]
    beta = 2 * (ox * dx + oy * dy)
    gamma = ox * ox + oy * oy - radius * radius
    disc = beta * beta - 4 * gamma
    if disc < 0:
        return None
    step = max((-beta - math.sqrt(disc)) / 2, (-beta + math.sqrt(disc)) / 2)
    g = (b[0] + step * dx, b[1] + step * dy)
    residual = (g[0] - d[0]) * ux + (g[1] - d[1]) * uy   # 0 ⟺ GD ⊥ CF
    return {"centre": centre, "b": b, "c": c, "f": f, "d": d, "g": g,
            "u": (ux, uy), "af": af, "residual": residual}


def check(ab=3, bc=2, cd=2):
    """Independent: find the radius that makes GD ⊥ CF, then measure EG and ED.

    The perpendicularity is the *equation*, not an assumption — the radius is
    bisected until it holds. Afterwards GC = GF and CF = 2·CD are audited rather
    than used, so a wrong angle chase in `solve` would show up here as a figure
    that fails its own audit.
    """
    ab, bc, cd = float(ab), float(bc), float(cd)
    if min(ab, bc, cd) <= 0 or bc >= 2 * ab:
        return None

    lo = hi = None
    previous = None
    radius = ab / 2 + 1e-6
    while radius < 400 * ab:
        cfg = _configuration(radius, ab, bc, cd)
        if cfg is not None:
            if abs(cfg["residual"]) < 1e-14:
                lo = hi = radius
                break
            if previous is not None and previous[1] * cfg["residual"] < 0:
                lo, hi = previous[0], radius
                break
            previous = (radius, cfg["residual"])
        radius += ab / 200
    if lo is None:
        return None

    for _ in range(200):
        mid = (lo + hi) / 2
        a_mid = _configuration(mid, ab, bc, cd)
        a_lo = _configuration(lo, ab, bc, cd)
        if a_mid is None or a_lo is None:
            return None
        if a_mid["residual"] * a_lo["residual"] <= 0:
            hi = mid
        else:
            lo = mid
    cfg = _configuration((lo + hi) / 2, ab, bc, cd)
    if cfg is None:
        return None

    dist = lambda p, q: math.hypot(p[0] - q[0], p[1] - q[1])   # noqa: E731
    # audit: the two facts solve leans on must hold in the built figure
    if abs(dist(cfg["g"], cfg["c"]) - dist(cfg["g"], cfg["f"])) > 1e-6 * ab:
        return None
    if abs(dist(cfg["c"], cfg["f"]) - 2 * cd) > 1e-6 * ab:
        return None

    ux, uy = cfg["u"]
    px, py = -uy, ux
    ox = cfg["d"][0] - cfg["centre"][0]
    oy = cfg["d"][1] - cfg["centre"][1]
    radius = math.hypot(cfg["centre"][0], cfg["centre"][1])     # |O − A|
    beta = 2 * (ox * px + oy * py)
    gamma = ox * ox + oy * oy - radius * radius
    disc = beta * beta - 4 * gamma
    if disc < 0:
        return None
    ends = [(cfg["d"][0] + t * px, cfg["d"][1] + t * py)
            for t in ((-beta - math.sqrt(disc)) / 2,
                      (-beta + math.sqrt(disc)) / 2)]
    e = max(ends, key=lambda p: dist(p, cfg["g"]))
    ed = dist(e, cfg["d"])
    if ed < 1e-12:
        return None
    return dist(e, cfg["g"]) / ed
