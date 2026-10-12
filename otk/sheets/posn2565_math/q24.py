"""ข้อ 24 — ค่าของ sin(∠ADG/2)·cos(∠AED/2)

กำหนดให้ ABCD เป็นรูปสี่เหลี่ยมจัตุรัสที่มี E และ F เป็นจุดกึ่งกลางด้าน BC และ CD
และให้เส้นตรง AE และเส้นตรง BF ตัดกันที่จุด G  จงหาค่าของ
sin(∠ADG/2)·cos(∠AED/2)

Two facts do all the work, and the second is the surprise.

Put A = (0,1), B = (1,1), C = (1,0), D = (0,0) and let E = (1, 1−m),
F = (1−m, 0) — the sheet's midpoints are m = 1/2. Then ``AE`` has direction
(1, −m) and ``BF`` has direction (−m, −1): the two lines are **perpendicular for
every m**, because BF is AE turned a quarter turn.

Intersecting them gives G = (1/(1+m²), (1+m²−m)/(1+m²)), and then

* **∠ADG = ∠AED**, again for every m. At m = 1/2 both are the 3-4-5 angle
  (cos = 3/5), and |DG| = 1 = the side, so ADG is isosceles.
* with θ for that common angle, ``cos θ = (1 − m + m²)/(L₁L₂)`` and
  ``sin θ = 1/(L₁L₂)`` where ``L₁ = √(1+m²)``, ``L₂ = √(1+(1−m)²)`` — the cross
  product of the two vectors at E is exactly 1.

So the requested product is ``sin(θ/2)cos(θ/2) = ½ sin θ = 1/(2L₁L₂)``, and at
m = 1/2 that is ``1/(2·5/4)`` = **2/5**.

m = 1/2 is the only ratio with denominator up to 15 for which ``L₁L₂`` is
rational, so the generator varies **which product is asked** rather than the
point — the other three (``sin·sin``, ``cos·cos``, ``tan``) are 1/5, 4/5 and 1/2.

``solve`` uses the closed forms above. ``check`` builds the square as plain
coordinates, intersects the two lines by solving the 2×2 system, measures both
angles with ``atan2`` (and refuses to answer unless they really are equal), and
takes the half-angles numerically.
"""

from __future__ import annotations

from fractions import Fraction
from math import acos, atan2, cos, hypot, isqrt, sin, sqrt

#: E and F cut BC and CD at the fraction num/den; ``ask`` picks the product.
PARAMS = {"num": 1, "den": 2, "ask": "sin_cos"}
ANSWER = Fraction(2, 5)
TOL = 1e-9
VARIANTS = [
    {"num": 1, "den": 2, "ask": "sin_sin"},
    {"num": 1, "den": 2, "ask": "cos_cos"},
    {"num": 1, "den": 2, "ask": "tan"},
    {"num": 1, "den": 3, "ask": "sin_cos"},      # irrational: a float
    {"num": 2, "den": 5, "ask": "cos_cos"},
    {"num": 1, "den": 1, "ask": "sin_cos"},      # E = C, F = D
    {"num": 3, "den": 2, "ask": "sin_cos"},      # E beyond C: still a line
]
ASKS = ("sin_cos", "sin_sin", "cos_cos", "tan")


def _exact(value: Fraction):
    """√value as a Fraction when it is one, else None."""
    n, d = value.numerator, value.denominator
    rn, rd = isqrt(n), isqrt(d)
    return Fraction(rn, rd) if rn * rn == n and rd * rd == d else None


def trig(num=1, den=2):
    """(cos θ, sin θ) for the common angle θ = ∠ADG = ∠AED, exact when possible."""
    if den == 0:
        return None
    m = Fraction(num, den)
    if m <= 0:
        return None
    product = (1 + m * m) * (1 + (1 - m) ** 2)
    root = _exact(product)
    if root is None:
        root = sqrt(float(product))
        return float(1 - m + m * m) / root, 1.0 / root
    return (1 - m + m * m) / root, 1 / root


def solve(num=1, den=2, ask="sin_cos"):
    """The requested half-angle product, exact where the geometry allows."""
    got = trig(num, den)
    if got is None or ask not in ASKS:
        return None
    c, s = got
    half_sin_sq = (1 - c) / 2               # sin²(θ/2)
    half_cos_sq = (1 + c) / 2               # cos²(θ/2)
    if ask == "sin_cos":
        return s / 2                        # sin(θ/2)cos(θ/2)
    if ask == "sin_sin":
        return half_sin_sq
    if ask == "cos_cos":
        return half_cos_sq
    return half_sin_sq * 2 / s              # tan(θ/2) = (1 - cos θ)/sin θ


def check(num=1, den=2, ask="sin_cos"):
    """Independent: lay out the square, intersect the lines, measure the angles.

    Both angles are measured with ``atan2`` from the actual coordinates and
    compared — the claim that ∠ADG = ∠AED is tested, not assumed — and the
    half-angles are then taken with the library's own ``sin``/``cos``. The
    result is snapped back to a fraction only when the exact route produced one.
    """
    if den == 0 or ask not in ASKS:
        return None
    m = num / den
    if m <= 0:
        return None
    a, b, c_, d = (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0)
    e = (c_[0], b[1] + m * (c_[1] - b[1]))
    f = (c_[0] + m * (d[0] - c_[0]), c_[1])

    # AE: a + t(e - a);  BF: b + u(f - b).  Solve the 2×2 system for t.
    p, q = (e[0] - a[0], e[1] - a[1]), (f[0] - b[0], f[1] - b[1])
    det = p[0] * (-q[1]) - (-q[0]) * p[1]
    if abs(det) < 1e-12:
        return None
    rhs = (b[0] - a[0], b[1] - a[1])
    t = (rhs[0] * (-q[1]) - (-q[0]) * rhs[1]) / det
    g = (a[0] + t * p[0], a[1] + t * p[1])

    def angle(vertex, u, v) -> float:
        first = atan2(u[1] - vertex[1], u[0] - vertex[0])
        second = atan2(v[1] - vertex[1], v[0] - vertex[0])
        out = abs(first - second)
        return min(out, 2 * 3.141592653589793 - out)

    adg = angle(d, a, g)
    aed = angle(e, a, d)
    if abs(adg - aed) > 1e-9:
        return None
    if abs(hypot(g[0] - d[0], g[1] - d[1])) < 1e-12:
        return None

    values = {"sin_cos": sin(adg / 2) * cos(aed / 2),
              "sin_sin": sin(adg / 2) * sin(aed / 2),
              "cos_cos": cos(adg / 2) * cos(aed / 2),
              "tan": sin(adg / 2) / cos(aed / 2)}
    got = values[ask]
    exact = solve(num, den, ask)
    if isinstance(exact, Fraction):
        snapped = Fraction(got).limit_denominator(10 ** 6)
        return snapped if abs(float(snapped) - got) < 1e-12 else got
    # a sanity anchor that does not go through solve()
    assert abs(acos(max(-1.0, min(1.0, cos(adg)))) - adg) < 1e-9
    return got
