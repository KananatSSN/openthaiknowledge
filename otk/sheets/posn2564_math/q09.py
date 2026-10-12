"""ข้อ 9 — ขนาดของ ∠ACD เมื่อ AO ตัด BC ที่ D และตัดวงกลมที่ E

จากรูป ให้ A, B และ C อยู่บนเส้นรอบวงของวงกลมซึ่งมี O เป็นจุดศูนย์กลาง
เส้นตรง AO ตัดกับเส้นตรง BC และวงกลม ที่จุด D และ E ตามลำดับ
ถ้า ∠BAC = 30° และ ∠CDE = 10° แล้ว ∠ACD มีขนาดเท่าไร

**The unstated fact is that AE is a diameter** — the line is drawn through O, so
A and E are antipodal and ∠ACE = 90°. Everything follows from that one angle.

Writing γ = ∠ACB, and using B–C–D collinear so that ∠ACD = 180° − γ:

* in △CED:  ∠ECD = ∠ACD − 90° = 90° − γ, so ∠DEC = 180° − 10° − (90° − γ)
  = 90° + γ − 10°;
* A, E, D are collinear, so ∠AEC = 180° − ∠DEC = 90° − γ + 10°;
* ABCE is cyclic with B and E on **opposite** sides of the chord AC, so
  ∠ABC = 180° − ∠AEC = 90° + γ − 10°;
* the angle sum of △ABC then gives 30° + (90° + γ − 10°) + γ = 180°.

So γ = (90° + ∠CDE − ∠BAC)/2 = 35°, and **∠ACD = 145°**.

``solve`` evaluates that formula. ``check`` builds the picture instead: it walks
C around a unit circle, places B so that ∠BAC is right, intersects BC with the
diameter to find D, and keeps the position where ∠CDE really is the printed
angle — then measures ∠ACD with a dot product.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: the two printed angles, in degrees.
PARAMS = {"bac": 30, "cde": 10}
ANSWER = 145
TOL = 5e-3
VARIANTS = [
    {"bac": 40, "cde": 10},
    {"bac": 30, "cde": 20},
    {"bac": 20, "cde": 5},
    {"bac": 50, "cde": 30},
    {"bac": 35, "cde": 15},
    {"bac": 80, "cde": 5},
]


def solve(bac=30, cde=10):
    """∠ACD = 180° − γ with γ = (90° + ∠CDE − ∠BAC)/2."""
    if bac <= 0 or cde <= 0:
        return None
    gamma = Fraction(90 + cde - bac, 2)
    if not 0 < gamma < 90:
        return None            # D must fall outside the circle, past E
    value = 180 - gamma
    return int(value) if value.denominator == 1 else value


def _angle(p, q, r):
    """The angle at q, in degrees."""
    v = (p[0] - q[0], p[1] - q[1])
    w = (r[0] - q[0], r[1] - q[1])
    nv, nw = math.hypot(*v), math.hypot(*w)
    if nv < 1e-12 or nw < 1e-12:
        return None
    cosine = max(-1.0, min(1.0, (v[0] * w[0] + v[1] * w[1]) / (nv * nw)))
    return math.degrees(math.acos(cosine))


def _figure(tc, bac):
    """A, E antipodal on the unit circle; C at angle tc; B set by ∠BAC."""
    a = (-1.0, 0.0)
    e = (1.0, 0.0)
    c = (math.cos(tc), math.sin(tc))
    # an inscribed angle of `bac` at A subtends an arc of 2·bac, so B sits that
    # far around from C — the drawing puts it on the far side.
    tb = tc + math.radians(2 * bac)
    b = (math.cos(tb), math.sin(tb))
    if abs(c[1] - b[1]) < 1e-12:
        return None
    t = (0.0 - b[1]) / (c[1] - b[1])
    d = (b[0] + t * (c[0] - b[0]), 0.0)
    if d[0] <= 1.0:
        return None                       # D must lie beyond E, outside the circle
    return a, b, c, d, e


def check(bac=30, cde=10):
    """Independent: sweep C until ∠CDE is the printed angle, then measure ∠ACD.

    Nothing is assumed about AE being a diameter — it is one *because* A and E
    are placed antipodally, which is what "the line through O" means — and no
    angle chase happens anywhere. The sweep tests the exact hit before the
    bracketing one.
    """
    if bac <= 0 or cde <= 0:
        return None

    def residual(tc):
        fig = _figure(tc, bac)
        if fig is None:
            return None
        _, _, c, d, e = fig
        got = _angle(c, d, e)
        return None if got is None else got - cde

    previous = None
    steps = 6000
    for i in range(1, steps):
        tc = math.pi * i / steps          # C in the upper half, as drawn
        value = residual(tc)
        if value is None:
            previous = None
            continue
        if value == 0.0:
            lo = hi = tc
            break
        if previous is not None and previous[1] * value < 0:
            lo, hi = previous[0], tc
            break
        previous = (tc, value)
    else:
        return None

    for _ in range(200):
        mid = (lo + hi) / 2
        a_mid, a_lo = residual(mid), residual(lo)
        if a_mid is None or a_lo is None:
            return None
        if a_mid * a_lo <= 0:
            hi = mid
        else:
            lo = mid
    fig = _figure((lo + hi) / 2, bac)
    if fig is None:
        return None
    a, _, c, d, _ = fig
    return _angle(a, c, d)
