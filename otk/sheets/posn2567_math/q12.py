"""ข้อ 12 — ค่าของ ∠ACB + ∠ADO

จากรูป วงกลมสองวงตัดกันที่จุด A และจุด B โดยมีจุด O เป็นจุดศูนย์กลางของวงกลม
วงใหญ่  CD เป็นส่วนของเส้นตรงตัดผ่านวงกลมสองวงที่จุด C, A และ D ที่ทำให้ CA เป็น
เส้นผ่านศูนย์กลางของวงกลมวงเล็ก  CE เป็นส่วนของเส้นตรงตัดผ่านวงกลมสองวงที่จุด
C, B และ E  ถ้า ∠ODE = 15° และ ∠OBE = 25° แล้ว ∠ACB + ∠ADO เท่ากับกี่องศา

รูปประกอบ (extract/figures/item12.png), read as follows:

* C is outside both circles, to the left; the two secants from C are C–A–D and
  C–B–E, so **A lies between C and D** and **B lies between C and E**.
* D and E are on the big circle, O is its centre, and OD̅, OB̅ are drawn.

Two consequences do all the work:

* CA is a diameter of the small circle and B is on the small circle, so
  ∠ABC = 90°. Hence AB ⊥ CE, i.e. ∠ABE = 90°, an inscribed angle of the **big**
  circle — so **AE is a diameter of the big circle** and O is the midpoint of AE.
* AE being a diameter gives ∠ADE = 90°.

Write u = ∠ODE and v = ∠OBE. Both OD = OE and OB = OE are radii, so those
triangles are isosceles and ∠OED = u, ∠OEB = v. Then

    ∠ADO = ∠ADE - ∠ODE      = 90 - u
    ∠ACB = 180 - ∠CDE - ∠DEC = 90 - (u + v)      (∠DEC = ∠DEA + ∠AEB = u + v)

so the sum asked for is

    ∠ACB + ∠ADO = 180 - 2u - v

which is 180 - 30 - 25 = 125 for the sheet's numbers. Note the answer needs both
given angles but not the radii — nothing in the figure is measured.

The configuration exists only while u + v < 90 (otherwise C stops being outside
the circles and the secants no longer meet in the drawn order).
"""

from __future__ import annotations

import math
from fractions import Fraction

#: ∠ODE and ∠OBE, in degrees.
PARAMS = {"ode_deg": 15, "obe_deg": 25}
ANSWER = Fraction(125)
VARIANTS = [
    {"ode_deg": 20, "obe_deg": 20},
    {"ode_deg": 10, "obe_deg": 40},
    {"ode_deg": 35, "obe_deg": 15},
    {"ode_deg": 5, "obe_deg": 60},
    {"ode_deg": 50, "obe_deg": 50},        # degenerate: u + v > 90
]
TOL = 1e-6


def solve(ode_deg=15, obe_deg=25):
    """∠ACB + ∠ADO = 180 - 2·∠ODE - ∠OBE, in degrees."""
    u, v = Fraction(ode_deg), Fraction(obe_deg)
    if u <= 0 or v <= 0 or u + v >= 90:
        return None
    return 180 - 2 * u - v


def _ang(p, q, r) -> float:
    """Angle ∠pqr in degrees, from coordinates."""
    a = (p[0] - q[0], p[1] - q[1])
    b = (r[0] - q[0], r[1] - q[1])
    cos = (a[0] * b[0] + a[1] * b[1]) / (math.hypot(*a) * math.hypot(*b))
    return math.degrees(math.acos(max(-1.0, min(1.0, cos))))


def _figure(gamma_deg: float, delta: float):
    """The whole picture from two free parameters, using none of the theory.

    C sits at the origin, ray CE̅ along the x-axis and ray CD̅ at ``gamma_deg``
    above it, with A at unit distance along the second. B is then forced: it is
    on the small circle whose diameter is CA̅, so ∠ABC = 90° and B is the foot of
    the perpendicular from A to the x-axis. The big circle is any circle through
    A and B — its centre runs along their perpendicular bisector, which here is
    the horizontal line y = sin γ/2, so ``x`` is the second free parameter. D and
    E are then read off as the *second* intersections of the two rays with it.

    ``x`` is written as ``xmin·(1 + delta)`` because the drawn order (A between C
    and D, B between C and E) fails below an explicit xmin, and every configuration
    of interest is crowded just above it.
    """
    g = math.radians(gamma_deg)
    cg, sg = math.cos(g), math.sin(g)
    if cg <= 0:
        return None
    xmin = max((1 - sg * sg / 2) / cg, cg)
    o = (xmin * (1 + delta), sg / 2)
    a, b, c = (cg, sg), (cg, 0.0), (0.0, 0.0)
    td = 2 * (a[0] * o[0] + a[1] * o[1]) - 1.0    # |t·Â - O| = R, one root t = 1
    se = 2 * o[0] - cg                            # (s - Oₓ)² + Oᵧ² = R², root s = cos γ
    if td <= 1.0 or se <= cg:
        return None
    return c, a, b, (td * a[0], td * a[1]), (se, 0.0), o


def _measure(gamma_deg: float, delta: float):
    f = _figure(gamma_deg, delta)
    if f is None:
        return None
    return _ang(f[5], f[3], f[4]), _ang(f[5], f[2], f[4]), f


def _at_obe(gamma_deg: float, v: float):
    """The configuration at this ∠ACB whose ∠OBE is v — it falls as delta grows."""
    lo = hi = None
    d = 1e-12
    while d < 1e12:
        r = _measure(gamma_deg, d)
        if r is not None:
            if r[1] >= v:
                lo = d
            else:
                hi = d
                break
        d *= 1.5
    if lo is None or hi is None:
        return None
    for _ in range(120):                          # bisect in log space
        mid = math.sqrt(lo * hi)
        r = _measure(gamma_deg, mid)
        if r is None:
            return None
        if r[1] >= v:
            lo = mid
        else:
            hi = mid
    return _measure(gamma_deg, lo)


def check(ode_deg=15, obe_deg=25):
    """Independent: search the two-parameter family of figures for this one.

    Nothing here knows that AE is a diameter or that ∠ADE = 90° — those are what
    ``solve`` deduces. This builds arbitrary figures satisfying only the stated
    incidences, then solves the two given angles by nested bisection (∠OBE in the
    inner loop, ∠ODE in the outer) and measures ∠ACB + ∠ADO off the result.
    """
    u, v = float(ode_deg), float(obe_deg)
    if u <= 0 or v <= 0 or u + v >= 90:
        return None

    lo, hi = 1e-9, 90 - 1e-9                      # ∠ODE falls as ∠ACB grows
    for _ in range(60):
        mid = (lo + hi) / 2
        r = _at_obe(mid, v)
        if r is not None and r[0] >= u:
            lo = mid
        else:
            hi = mid
    r = _at_obe(lo, v)
    if r is None or abs(r[0] - u) > 1e-6 or abs(r[1] - v) > 1e-6:
        return None
    c, a, b, d, e, o = r[2]
    return Fraction(_ang(a, c, b) + _ang(a, d, o)).limit_denominator(10 ** 6)
