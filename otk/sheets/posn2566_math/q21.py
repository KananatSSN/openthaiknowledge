"""ข้อ 21 — ความยาว AF จากวงกลมสามวง

จากรูป วงกลม C₁ มีรัศมียาว 3 หน่วย และวงกลม C₂ มีรัศมียาว 5 หน่วย  วงกลม C₁ และ
วงกลม C₂ สัมผัสกันที่จุด B และวงกลม C₂ ผ่านจุด O₃  AD เป็นส่วนของเส้นตรงที่ทำให้ AB
และ BD เป็นเส้นผ่านศูนย์กลางของวงกลม C₁ และวงกลม C₂ ตามลำดับ  วงกลม C₃ ผ่านจุด O₂
และตัดกับวงกลม C₁ ที่จุด B และจุด E  AF เป็นส่วนของเส้นตรงที่ตัดวงกลม C₁ และวงกลม C₃
ที่จุด A, E และ F  จงหาความยาวของ AF

**C₃ is not a free circle — the two conditions pin it exactly.** Its centre O₃
lies on C₂, so |O₂O₃| = r₂; and it passes through O₂ *and* through B, which is
itself on C₂, so |O₃B| = |O₃O₂| = r₂ = r₃. Since |O₂B| = r₂ as well, the
triangle O₂O₃B is **equilateral** and the whole picture is a function of r₁ and
r₂ alone.

Put A at the origin along the line AD:

    O₁ = (r₁, 0)   B = (2r₁, 0)   O₂ = (2r₁ + r₂, 0)
    O₃ = (2r₁ + r₂/2, r₂√3/2)    r₃ = r₂

The line A–E–F meets C₃ twice, so the power of A with respect to C₃ gives one
equation. A's power is easiest read off the line through B and O₂, both of which
are on C₃:

    AE · AF = AB · AO₂ = 2r₁(2r₁ + r₂)        (= 6·11 = 66 on the sheet)

For the second equation, subtract the two circle equations: C₁ is
``x² + y² = 2r₁x`` and C₃ is ``x² + y² − 2O₃·X + |O₃|² − r₂² = 0``, and their
radical axis — the line BE — comes out as

    (2r₁ + r₂)x + √3 r₂ y = 2r₁(2r₁ + r₂)

Substituting back into C₁ and dividing out the root x = 2r₁ (which is B) leaves
E, and ``AE² = 2r₁x_E`` because A is on C₁ too:

    AE² = 4r₁²(2r₁ + r₂)² / ((2r₁ + r₂)² + 3r₂²)

Dividing the power by that collapses everything:

    AF = √((2r₁ + r₂)² + 3r₂²) = **2√(r₁² + r₁r₂ + r₂²)**

— a law-of-cosines expression with a 120° angle in it, which is the equilateral
triangle showing through. At r₁ = 3, r₂ = 5 that is 2√49 = **14**, and
AE = 66/14 = 33/7 as a by-product.

``solve`` evaluates the closed form. ``check`` derives nothing: it builds the
five points as coordinates, intersects C₁ with C₃ to find E, intersects the ray
AE with C₃ to find F, and measures — then confirms the power of the point as a
second reading before returning.
"""

from __future__ import annotations

from math import hypot, isqrt, sqrt

#: radii of C₁ and C₂; C₃'s radius is r₂ and its centre is on C₂.
PARAMS = {"r1": 3, "r2": 5}
ANSWER = 14
TOL = 1e-7
VARIANTS = [
    {"r1": 4, "r2": 6},
    {"r1": 2, "r2": 7},
    {"r1": 5, "r2": 8},
    {"r1": 3, "r2": 4},
    {"r1": 7, "r2": 8},          # another perfect square: 2√169 = 26
    {"r1": 5, "r2": 16},         # 2√361 = 38
]


def solve(r1=3, r2=5):
    """AF = 2√(r₁² + r₁r₂ + r₂²)."""
    if r1 <= 0 or r2 <= 0:
        return None
    inner = r1 * r1 + r1 * r2 + r2 * r2
    if isinstance(inner, int):
        root = isqrt(inner)
        if root * root == inner:
            return 2 * root
    return 2 * sqrt(inner)


def _circle_intersections(c1, rad1, c2, rad2):
    """The two points where the circles meet, or None."""
    dx, dy = c2[0] - c1[0], c2[1] - c1[1]
    d = hypot(dx, dy)
    if d < 1e-12 or d > rad1 + rad2 or d < abs(rad1 - rad2):
        return None
    a = (rad1 * rad1 - rad2 * rad2 + d * d) / (2 * d)
    h2 = rad1 * rad1 - a * a
    if h2 < 0:
        return None
    h = sqrt(h2)
    mx, my = c1[0] + a * dx / d, c1[1] + a * dy / d
    ux, uy = -dy / d, dx / d
    return [(mx + h * ux, my + h * uy), (mx - h * ux, my - h * uy)]


def check(r1=3, r2=5):
    """Independent: build the figure, find E and F by intersection, measure AF.

    No power of a point and no radical axis — the circles are intersected
    numerically. The power identity AE·AF = AB·AO₂ is then used only as an
    audit of the construction, so a wrong C₃ would be caught rather than
    measured.
    """
    if r1 <= 0 or r2 <= 0:
        return None
    a = (0.0, 0.0)
    o1 = (float(r1), 0.0)
    b = (2.0 * r1, 0.0)
    o2 = (2.0 * r1 + r2, 0.0)
    o3 = (2.0 * r1 + r2 / 2, r2 * sqrt(3) / 2)     # equilateral on O₂B
    r3 = float(r2)

    if abs(hypot(o3[0] - o2[0], o3[1] - o2[1]) - r2) > 1e-9:
        return None                                 # O₃ must sit on C₂
    if abs(hypot(o3[0] - b[0], o3[1] - b[1]) - r3) > 1e-9:
        return None                                 # ... and C₃ pass through B

    hits = _circle_intersections(o1, float(r1), o3, r3)
    if hits is None:
        return None
    e = max(hits, key=lambda p: hypot(p[0] - b[0], p[1] - b[1]))
    ae = hypot(e[0] - a[0], e[1] - a[1])
    if ae < 1e-9:
        return None

    dx, dy = (e[0] - a[0]) / ae, (e[1] - a[1]) / ae
    fx, fy = a[0] - o3[0], a[1] - o3[1]
    beta = 2 * (fx * dx + fy * dy)
    gamma = fx * fx + fy * fy - r3 * r3
    disc = beta * beta - 4 * gamma
    if disc < 0:
        return None
    af = max((-beta - sqrt(disc)) / 2, (-beta + sqrt(disc)) / 2)
    if af <= 0:
        return None

    power = 2 * r1 * (2 * r1 + r2)                  # AB · AO₂
    if abs(ae * af - power) > 1e-6 * max(1.0, power):
        return None                                 # the figure does not close
    return round(af) if abs(af - round(af)) < 1e-9 else af
