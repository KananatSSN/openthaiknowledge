"""ข้อ 15 — ขนาดของ ∠ADE

จากรูป AB เป็นเส้นผ่านศูนย์กลางของวงกลม  DE⃡ สัมผัสวงกลมที่จุด D
BF เป็นส่วนของเส้นตรงที่ลากต่อจาก AB ออกไปทางจุด B และตัด DE⃡ ที่จุด C
โดยที่จุด D อยู่ระหว่างจุด C และจุด E
ถ้า ∠DCF = 2(∠ADE - ∠BAD) แล้ว ∠ADE มีขนาดกี่องศา

รูปประกอบ (extract/figures/item15.png), read as follows:

* the tangent line is horizontal, touching the circle at D at its lowest point;
  E is to the **right** of D and C to the left, with D between them as stated;
* A is up and to the right on the circle, B is down and to the left — AB̅ passes
  through the centre — and the ray AB continued past B leaves the circle and meets
  the tangent at C, going on to F. So **C is beyond B**, and F beyond C;
* the marked angle at D is ∠ADE, between chord DA̅ and the tangent towards E.

Write θ = ∠ADE and α = ∠BAD. Two facts:

* AB is a diameter, so ∠ADB = 90°, and in △ABD, ∠ABD = 90 - α;
* tangent–chord: ∠ADE equals the inscribed angle in the alternate segment,
  ∠ABD. Hence **θ + α = 90**.

For the angle at C, use △ACD: ∠CAD = α (ray AC is ray AB) and ∠ADC = 180 - θ
(C is on the far side of D from E), so ∠ACD = θ - α, and since F is beyond C,

    ∠DCF = 180 - (θ - α).

The condition ∠DCF = k(θ - α) therefore reads 180 = (k+1)(θ - α), so
θ - α = 180/(k+1), and with θ + α = 90,

    θ = 45 + 90/(k+1)

which is 45 + 30 = **75°** at the sheet's k = 2.

The configuration needs 0 < α < θ < 90, i.e. k > 1: at k = 1 the angle at C would
force θ = 90 and the chord DA̅ would become the tangent itself.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: the multiplier k in ∠DCF = k(∠ADE - ∠BAD).
PARAMS = {"mult": 2}
ANSWER = Fraction(75)
VARIANTS = [
    {"mult": 3},
    {"mult": 4},
    {"mult": 5},
    {"mult": 9},
    {"mult": 1},          # degenerate: θ would be 90° and DA̅ would be the tangent
]
TOL = 1e-6


def solve(mult=2):
    """∠ADE = 45 + 90/(k+1) degrees."""
    k = Fraction(mult)
    if k <= 1:
        return None
    return 45 + Fraction(90) / (k + 1)


def _ang(p, q, r) -> float:
    a = (p[0] - q[0], p[1] - q[1])
    b = (r[0] - q[0], r[1] - q[1])
    cos = (a[0] * b[0] + a[1] * b[1]) / (math.hypot(*a) * math.hypot(*b))
    return math.degrees(math.acos(max(-1.0, min(1.0, cos))))


def _figure(phi_deg: float):
    """The figure with A at angle φ on the unit circle, D at the bottom.

    B is the antipode of A, so line AB passes through the centre; C is where that
    line meets the tangent y = -1, and F is further along it. Nothing here uses
    the tangent–chord relation — the angles are measured afterwards.
    """
    phi = math.radians(phi_deg)
    a = (math.cos(phi), math.sin(phi))
    if a[1] <= 1e-12:
        return None
    b = (-a[0], -a[1])
    d, e = (0.0, -1.0), (1.0, -1.0)
    t = -1.0 / a[1]                               # line through the origin, y = -1
    c = (t * a[0], -1.0)
    if c[0] >= d[0]:                              # D must lie between C and E
        return None
    f = (c[0] + (b[0] - a[0]), c[1] + (b[1] - a[1]))
    return a, b, c, d, e, f


def check(mult=2):
    """Independent: sweep A around the circle and measure the stated condition.

    ∠ADE, ∠BAD and ∠DCF all come out of coordinates by dot products, and φ is
    bisected until ∠DCF - k(∠ADE - ∠BAD) vanishes. The tangent–chord identity
    and the 90° in a semicircle — the two facts ``solve`` runs on — are asserted
    here as consequences, not assumed.
    """
    k = float(mult)
    if k <= 1:
        return None

    def residual(phi: float):
        fig = _figure(phi)
        if fig is None:
            return None
        a, b, c, d, e, f = fig
        theta, alpha = _ang(a, d, e), _ang(b, a, d)
        return _ang(d, c, f) - k * (theta - alpha)

    lo, hi = 1e-9, 180 - 1e-9
    if residual(lo) is None:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        r = residual(mid)
        if r is None:                             # past φ = 90°, where C crosses D
            hi = mid
        elif r > 0:
            lo = mid
        else:
            hi = mid
    fig = _figure((lo + hi) / 2)
    if fig is None:
        return None
    a, b, c, d, e, f = fig
    assert abs(_ang(a, d, b) - 90) < 1e-6, "AB is not a diameter"
    assert abs(_ang(a, d, e) + _ang(b, a, d) - 90) < 1e-6, "tangent–chord broken"
    return Fraction(_ang(a, d, e)).limit_denominator(10 ** 6)
