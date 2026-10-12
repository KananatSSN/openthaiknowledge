"""ข้อ 22 — ความยาวรอบรูปสามเหลี่ยม EFG ที่เกิดจากเส้นตั้งฉากสามเส้น

จากรูป ให้ ABC เป็นรูปสามเหลี่ยมที่มีด้าน AC ยาว 16 หน่วย ด้าน BC ยาว 14 หน่วย
ลากเส้นตั้งฉากกับด้านทั้งสามทำให้เกิดรูปสามเหลี่ยม EFG ภายใน โดย FG = 2, GD = 8
และ AD = 4  จุด M เป็นจุดกึ่งกลางของส่วนของเส้นตรง GB โดย MD = 5
จงหาความยาวรอบรูปสามเหลี่ยม EFG

Two steps, and the first is the one that is easy to miss.

**AB is not given — MD is what pins it.** GD ⊥ AB makes GDB right-angled at D,
and M is the midpoint of the hypotenuse GB, so DM is the median to the
hypotenuse and

    GB = 2·MD = 10   ⟹   DB = √(GB² − GD²) = √(100 − 64) = 6
    AB = AD + DB = 4 + 6 = **10**

**Then the perpendiculars.** Three lines, each perpendicular to one side of ABC,
bound a triangle *similar* to ABC — each of its sides is perpendicular to one
side of ABC, so the angles carry over. The correspondence is the natural one:
the side lying on the line perpendicular to AB corresponds to AB. FG is that
side, so the ratio is

    k = FG : AB = 2 : 10 = 1/5

and the perimeter scales with it:

    perimeter(EFG) = (16 + 14 + 10)/5 = **8**

Note what the ratio does *not* need: where along each side the three
perpendiculars are drawn. Slide any of them and the bounded triangle only
changes size, never shape — which is why FG alone fixes everything.

``solve`` follows that. ``check`` assumes no similarity: it puts ABC in
coordinates, drops the three perpendiculars at several genuinely different
offsets, measures the triangle they bound, rescales it so its own AB-side is FG,
and reports the perimeter only when the different offsets agree — so the
shape-independence above is measured rather than taken on trust.
"""

from __future__ import annotations

from math import hypot, sqrt

#: FG, GD, AD and MD as printed, plus the two sides the stem gives.
PARAMS = {"fg": 2, "gd": 8, "ad": 4, "md": 5, "ac": 16, "bc": 14}
ANSWER = 8
TOL = 1e-7
VARIANTS = [
    {"fg": 3},
    {"fg": 1, "ac": 13, "bc": 11},
    {"gd": 6, "md": 5, "ad": 3, "ac": 15, "bc": 13},
    {"ad": 6, "gd": 8, "md": 5, "ac": 20, "bc": 18},
    {"fg": 4, "ac": 17, "bc": 15},
    {"gd": 12, "md": 6.5, "ad": 2, "ac": 12, "bc": 11},
]


def _base(gd, ad, md):
    """AB, from the median to the hypotenuse of the right triangle GDB."""
    gb = 2 * md
    if gb <= gd:
        return None
    return ad + sqrt(gb * gb - gd * gd)


def solve(fg=2, gd=8, ad=4, md=5, ac=16, bc=14):
    """perimeter(EFG) = (FG / AB) · perimeter(ABC)."""
    if min(fg, gd, ad, md, ac, bc) <= 0:
        return None
    ab = _base(gd, ad, md)
    if ab is None or ab <= 0:
        return None
    if not (abs(ac - bc) < ab < ac + bc):
        return None                       # no such triangle
    if fg > ab:
        return None                       # EFG would not be inside ABC
    value = (fg / ab) * (ab + ac + bc)
    return round(value) if abs(value - round(value)) < 1e-9 else value


def _intersect(l1, l2):
    (x1, y1, dx1, dy1), (x2, y2, dx2, dy2) = l1, l2
    den = dx1 * dy2 - dy1 * dx2
    if abs(den) < 1e-12:
        return None
    s = ((x2 - x1) * dy2 - (y2 - y1) * dx2) / den
    return (x1 + s * dx1, y1 + s * dy1)


def _perp_at(p, q, t):
    """The line through the point t of the way from p to q, perpendicular to pq."""
    px, py = p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])
    dx, dy = q[0] - p[0], q[1] - p[1]
    return (px, py, -dy, dx)


def check(fg=2, gd=8, ad=4, md=5, ac=16, bc=14):
    """Independent: build the figure and measure it, at several offsets.

    Nothing here knows that the bounded triangle is similar to ABC. Each offset
    triple gives a different pair of perpendicular positions; the triangle they
    cut out is measured, scaled so that its side on the AB-perpendicular is FG,
    and its perimeter recorded. A value is returned only if every offset agrees,
    which is what turns "slide the perpendiculars and only the size changes"
    into an observation.
    """
    if min(fg, gd, ad, md, ac, bc) <= 0:
        return None
    ab = _base(gd, ad, md)
    if ab is None or ab <= 0:
        return None
    if not (abs(ac - bc) < ab < ac + bc):
        return None
    if fg > ab:
        return None

    a = (0.0, 0.0)
    b = (ab, 0.0)
    cx = (ac * ac - bc * bc + ab * ab) / (2 * ab)
    inside = ac * ac - cx * cx
    if inside <= 0:
        return None
    c = (cx, sqrt(inside))

    values = []
    for offs in ((0.4, 0.3, 0.5), (0.2, 0.8, 0.15), (0.6, 0.55, 0.35),
                 (0.75, 0.25, 0.65)):
        on_ab = _perp_at(a, b, offs[0])       # the line FG lies on
        on_bc = _perp_at(b, c, offs[1])
        on_ca = _perp_at(c, a, offs[2])
        p_ab_bc = _intersect(on_ab, on_bc)
        p_bc_ca = _intersect(on_bc, on_ca)
        p_ca_ab = _intersect(on_ca, on_ab)
        if None in (p_ab_bc, p_bc_ca, p_ca_ab):
            return None
        side_on_ab = hypot(p_ca_ab[0] - p_ab_bc[0], p_ca_ab[1] - p_ab_bc[1])
        if side_on_ab < 1e-9:
            return None
        perimeter = (hypot(p_ab_bc[0] - p_bc_ca[0], p_ab_bc[1] - p_bc_ca[1])
                     + hypot(p_bc_ca[0] - p_ca_ab[0], p_bc_ca[1] - p_ca_ab[1])
                     + side_on_ab)
        values.append(perimeter * fg / side_on_ab)

    if max(values) - min(values) > 1e-7 * max(1.0, abs(values[0])):
        return None
    value = sum(values) / len(values)
    return round(value) if abs(value - round(value)) < 1e-9 else value
