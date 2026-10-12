"""ข้อ 12 — ขนาดของ ∠ACD

ให้ ABC เป็นรูปสามเหลี่ยม โดยที่ BC > AB และมี D เป็นจุดกึ่งกลางด้าน AB
ถ้า ∠ADC = 45° และ ∠BCD = 15° แล้ว ∠ACD มีขนาดกี่องศา

D being the *midpoint* is the whole condition: AD = DB, and the sine rule in each
half writes both in terms of the common side DC̅.

    △BDC:  ∠BDC = 180° - δ,  ∠DBC = δ - γ,  so  BD = DC·sin γ / sin(δ - γ)
    △ADC:  ∠ADC = δ,  ∠ACD = x,  ∠DAC = 180° - δ - x,  so  AD = DC·sin x / sin(δ + x)

Setting them equal and expanding sin(δ + x) gives a closed form:

    tan x = k sin δ / (1 - k cos δ),      k = sin γ / sin(δ - γ)

For δ = 45° and γ = 15°, k = sin15°/sin30° so tan x = 1/√3 and

    ∠ACD = **30°**

(the whole triangle then reads ∠ACB = 45°, ∠ABC = 30°, ∠BAC = 105°, and
BC = AB·sin105°/sin45° > AB as the statement requires).

``check`` builds the triangle in coordinates and slides C until D is genuinely
the midpoint of AB̅, measuring the angles rather than solving for them.

**This one barely generalises.** Scanning every integer pair (δ, γ) turns up
exactly one more family with an exact answer in whole degrees — δ = 90°, where
CD̅ is the perpendicular bisector of AB̅ and x = γ falls out for free. So ``ask``
is the real tunable: the same triangle answers six different questions, and the
generator varies which angle it asks for rather than the constants.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: ∠ADC and ∠BCD in degrees, and which angle of the figure to report.
PARAMS = {"adc_deg": 45, "bcd_deg": 15, "ask": "acd"}
ANSWER = Fraction(30)
VARIANTS = [
    {"ask": "abc"},
    {"ask": "bac"},
    {"ask": "acb"},
    {"adc_deg": 90, "bcd_deg": 20, "ask": "bac"},
    {"adc_deg": 120, "bcd_deg": 20},
    {"adc_deg": 60, "bcd_deg": 30},        # BC < AB: not the stated figure
    {"adc_deg": 45, "bcd_deg": 45},        # ∠DBC = 0: no triangle
]
TOL = 1e-7


#: the angles of the figure, in terms of δ, γ and x = ∠ACD.
ANGLES = ("acd", "bcd", "adc", "abc", "bac", "acb")


def solve(adc_deg=45, bcd_deg=15, ask="acd"):
    """The named angle in degrees; x = ∠ACD comes from tan x = k sinδ/(1 - k cosδ)."""
    d, g = float(adc_deg), float(bcd_deg)
    if ask not in ANGLES or not 0 < g < d < 180:
        return None
    k = math.sin(math.radians(g)) / math.sin(math.radians(d - g))
    x = math.degrees(math.atan2(k * math.sin(math.radians(d)),
                                1 - k * math.cos(math.radians(d))))
    if x <= 0 or x >= 180 - d:
        return None
    # The statement says BC > AB, i.e. ∠BAC > ∠ACB, i.e. 180 - δ - x > x + γ.
    # Without it the figure exists but is not the one the question describes —
    # and ``check``, which builds it, rejects those outright.
    if 2 * x >= 180 - d - g - 1e-9:
        return None
    wanted = {"acd": x, "bcd": g, "adc": d, "abc": d - g,
              "bac": 180 - d - x, "acb": x + g}[ask]
    return Fraction(wanted).limit_denominator(10 ** 6)


def check(adc_deg=45, bcd_deg=15, ask="acd"):
    """Independent: place D and C, sweep A, and stop where DB = DA.

    Every reported angle is then measured off the finished triangle by dot
    products, so ``ask`` costs nothing here — which is the point: ``solve``
    computes the other five from x by angle arithmetic, and this one does not.
    """
    d, g = float(adc_deg), float(bcd_deg)
    if ask not in ANGLES or not 0 < g < d < 180:
        return None

    def ang(p, q, r) -> float:
        u = (p[0] - q[0], p[1] - q[1])
        v = (r[0] - q[0], r[1] - q[1])
        cos = (u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))
        return math.degrees(math.acos(max(-1.0, min(1.0, cos))))

    # D at the origin with C on the positive x-axis; A is then at angle δ from
    # DC̅ and B directly opposite it, at distance t on the other side.
    dd, c = (0.0, 0.0), (1.0, 0.0)
    ray = math.radians(d)

    def config(t: float):
        a = (t * math.cos(ray), t * math.sin(ray))
        b = (-t * math.cos(ray), -t * math.sin(ray))     # D is the midpoint
        return a, b

    def residual(t: float) -> float:
        a, b = config(t)
        return ang(b, c, dd) - g                          # ∠BCD as drawn

    lo, hi = 1e-9, 1e4
    if residual(lo) * residual(hi) > 0:
        return None
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if residual(lo) * residual(mid) <= 0:
            hi = mid
        else:
            lo = mid
    t = math.sqrt(lo * hi)
    a, b = config(t)
    assert abs(math.dist(dd, a) - math.dist(dd, b)) < 1e-9, "D is not the midpoint"
    assert abs(ang(a, dd, c) - d) < 1e-6
    if math.dist(b, c) <= math.dist(a, b):                # the stated BC > AB
        return None
    measured = {"acd": ang(a, c, dd), "bcd": ang(b, c, dd), "adc": ang(a, dd, c),
                "abc": ang(a, b, c), "bac": ang(b, a, c), "acb": ang(a, c, b)}
    return Fraction(measured[ask]).limit_denominator(10 ** 6)
