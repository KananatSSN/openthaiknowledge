"""ข้อ 23 — พื้นที่บริเวณที่แรเงา (สามเหลี่ยมมุมฉากกับครึ่งวงกลมแนบใน)

จากรูป ให้ ABC เป็นรูปสามเหลี่ยมมุมฉาก โดยมีมุม C เป็นมุมฉาก ให้ DE เป็นเส้นผ่าน
ศูนย์กลางของครึ่งวงกลมแนบในรูปสามเหลี่ยม ABC (D และ E อยู่บนด้าน AB) ให้ G และ F
เป็นจุดบนด้าน AC และ BC ตามลำดับ โดยที่ DG ตั้งฉากกับ AC และ EF ตั้งฉากกับ BC
ถ้า DG = 6 หน่วย และ EF = 12 หน่วย แล้วบริเวณที่แรเงามีพื้นที่เท่ากับกี่ตารางหน่วย

The shaded region is the one at C, bounded by the two legs and the arc.

Put C at the origin with the legs on the axes. The semicircle is tangent to both
legs, so its centre is O = (r, r) and the tangency points are P = (r, 0) and
Q = (0, r): **CPOQ is a square of side r**, and the shaded region is that square
minus a quarter disk,

    shaded = r² − πr²/4 = r²(1 − π/4).

Only r is missing. With ∠A = α, the foot D sits at distance ``AO − r`` from A, so
``DG = AD·sin α = r(1 − sin α)``, and likewise ``EF = r(1 − cos α)``. Then
``(r − p)² + (r − q)² = r²`` — the two legs of the same right angle — which is

    r² − 2(p + q)r + (p² + q²) = 0,   r = p + q + √(2pq)

(the larger root; the smaller one gives sin α > 1). For p = 6 and q = 12,
r = 18 + 12 = **30**, sin α = 4/5, the legs are 52.5 and 70, and

    shaded = 900 − 225π ≈ **193.1417**

``check`` never touches that quadratic. It searches for the two legs directly by
bisection until the printed perpendiculars come out as p and q, then peels the
triangle apart as
``[ABC] − ½πr² − (corner at A) − (corner at B)``, each corner being a triangle
minus a circular sector.
"""

from __future__ import annotations

from math import atan2, hypot, isqrt, pi, sqrt

#: DG = p and EF = q, the two perpendiculars printed on the figure.
PARAMS = {"p": 6, "q": 12}
ANSWER = 193.14165294229656
TOL = 1e-6
VARIANTS = [
    {"p": 2, "q": 4},
    {"p": 12, "q": 6},          # mirror image: same area
    {"p": 1, "q": 8},
    {"p": 9, "q": 2},
    {"p": 5, "q": 5},           # isosceles: r = 10 + 5√2
    {"p": 0, "q": 12},          # D on the tangency point: degenerate
]


def radius(p=6, q=12):
    """r = p + q + √(2pq), the radius forced by the two perpendiculars."""
    if p <= 0 or q <= 0:
        return None
    return p + q + sqrt(2 * p * q)


def exact_radius(p=6, q=12):
    """r as a whole number when 2pq is a perfect square, else None."""
    if p <= 0 or q <= 0:
        return None
    root = isqrt(2 * p * q)
    return p + q + root if root * root == 2 * p * q else None


def solve(p=6, q=12):
    """Area of the region at C: the square CPOQ less a quarter disk."""
    r = radius(p, q)
    if r is None:
        return None
    return r * r * (1 - pi / 4)


def check(p=6, q=12):
    """Independent: find the legs numerically, then subtract the pieces.

    The triangle is rebuilt from scratch — a bisection on the shape of the
    triangle makes DG/EF match p/q, a scaling makes DG equal p — and the shaded
    area is then what is left of the triangle after removing the half disk and
    the two corner regions at A and B, each computed as a triangle minus a
    circular sector. Nothing here knows r = p + q + √(2pq).
    """
    if p <= 0 or q <= 0:
        return None

    def perpendiculars(ratio: float, scale: float = 1.0):
        """(DG, EF, geometry) for legs CA = scale, CB = ratio·scale."""
        a, b = scale, ratio * scale
        c = hypot(a, b)
        r = a * b / (a + b)                      # centre at (r, r) lies on AB
        return r * (1 - b / c), r * (1 - a / c), (a, b, c, r)

    # ratio ↦ DG/EF is monotone; bracket it, then bisect.
    def gap(ratio: float) -> float:
        dg, ef, _ = perpendiculars(ratio)
        return dg / ef - p / q

    lo, hi = 1e-6, 1e6
    if gap(lo) * gap(hi) > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        if gap(lo) * gap(mid) <= 0:
            hi = mid
        else:
            lo = mid
    ratio = (lo + hi) / 2

    dg_unit, ef_unit, _ = perpendiculars(ratio)
    if dg_unit <= 0:
        return None
    scale = p / dg_unit
    dg, ef, (a, b, c, r) = perpendiculars(ratio, scale)
    if abs(dg - p) > 1e-7 * p or abs(ef - q) > 1e-6 * q:
        return None

    # coordinates: C at the origin, A = (a, 0), B = (0, b), centre O = (r, r)
    o = (r, r)
    ux, uy = -a / c, b / c                        # unit vector A → B
    d = (o[0] - r * ux, o[1] - r * uy)
    e = (o[0] + r * ux, o[1] + r * uy)
    tangent_a, tangent_b = (r, 0.0), (0.0, r)     # feet on the two legs

    def sector(u, v) -> float:
        """Area of the circular sector of the disk between two boundary points."""
        angle = abs(atan2(u[1] - o[1], u[0] - o[0])
                    - atan2(v[1] - o[1], v[0] - o[0]))
        angle = min(angle, 2 * pi - angle)
        return 0.5 * r * r * angle

    def triangle(u, v, w) -> float:
        return abs((v[0] - u[0]) * (w[1] - u[1])
                   - (w[0] - u[0]) * (v[1] - u[1])) / 2

    corner_a = triangle((a, 0.0), o, tangent_a) - sector(d, tangent_a)
    corner_b = triangle((0.0, b), o, tangent_b) - sector(e, tangent_b)
    return a * b / 2 - pi * r * r / 2 - corner_a - corner_b
