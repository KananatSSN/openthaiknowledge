"""ข้อ 20 — ความยาว CE เมื่อ EF ขนานกับ BC ผ่านจุดตัดของเส้นแบ่งครึ่งมุม

กำหนดให้ ABC เป็นรูปสามเหลี่ยม โดยมีเส้นแบ่งครึ่งมุมภายในของมุม ∠ABC ตัดกับ
เส้นแบ่งครึ่งมุมภายนอกของมุม ∠ACB ที่จุด D ให้เส้นตรงที่ขนานกับด้าน BC และผ่าน
จุด D ตัดด้าน AC ที่จุด E และตัดด้าน AB ที่จุด F ถ้า EF = 9 หน่วย และ BF = 16
หน่วย แล้ว CE มีค่ากี่หน่วย

Both isosceles triangles come from the same one-line argument — **a bisector plus
a parallel makes two equal angles at the same vertex**:

* FD ∥ BC gives ∠FDB = ∠DBC, and BD bisects ∠ABC so ∠DBC = ∠DBF. Hence △FBD is
  isosceles and **FD = FB = 16**.
* At C the bisected angle is the *external* one, and the same alternate-angle
  step gives ∠EDC = ∠DCE, so **ED = EC**.

With F, E, D in that order along the parallel, CE = ED = FD − FE = 16 − 9 = **7**.

**That order is not automatic, and the stem is what fixes it.** For some
triangles the parallel through D meets the *extensions* of AC and AB instead, and
then E lies beyond F, giving CE = BF + EF = 25. The printed "ตัด**ด้าน** AC ที่
จุด E และตัดด้าน AB ที่จุด F" says both points are on the sides themselves, and
that is exactly the configuration with F, E, D in order — so the answer is 7, not
25. Read the word ด้าน and the item has one answer; ignore it and it has two.

Neither the triangle's shape nor AE, AF, or the angles are ever needed — which is
why two lengths are enough data.

``solve`` returns BF − EF. ``check`` builds actual triangles: it sweeps the apex
until the *measured* EF : BF matches the printed ratio, rescales the figure so
BF is exactly the printed length, and measures CE — with D found by intersecting
the two bisectors, not by assuming anything about them.
"""

from __future__ import annotations

#: the two printed lengths on the parallel line.
PARAMS = {"ef": 9, "bf": 16}
ANSWER = 7
TOL = 1e-6
VARIANTS = [
    {"ef": 5, "bf": 12},
    {"ef": 1, "bf": 4},
    {"ef": 10, "bf": 25},
    {"ef": 3, "bf": 20},
    {"ef": 16, "bf": 9},        # EF longer than BF: E is not between F and D
    {"ef": 7, "bf": 8},
]


def solve(ef=9, bf=16):
    """CE = ED = FD − FE, and FD = FB."""
    if ef <= 0 or bf <= 0 or ef >= bf:
        return None
    return bf - ef


def _figure(apex):
    """B = (0,0), C = (1,0), apex A — returns (EF, BF, CE) measured."""
    a = complex(*apex)
    b = complex(0.0, 0.0)
    c = complex(1.0, 0.0)
    if abs(a.imag) < 1e-9:
        return None

    def unit(z):
        return z / abs(z)

    dir_b = unit(unit(a - b) + unit(c - b))            # internal bisector at B
    dir_c = unit(unit(a - c) - unit(b - c))            # external bisector at C

    def meet(p, dp, q, dq):
        det = dp.real * (-dq.imag) - (-dq.real) * dp.imag
        if abs(det) < 1e-12:
            return None
        rx, ry = q.real - p.real, q.imag - p.imag
        t = (rx * (-dq.imag) - (-dq.real) * ry) / det
        return p + t * dp

    d = meet(b, dir_b, c, dir_c)
    if d is None:
        return None
    along = unit(c - b)
    e = meet(d, along, a, unit(c - a))
    f = meet(d, along, a, unit(b - a))
    if e is None or f is None:
        return None
    # the stem says the parallel cuts the *sides*, so both points must lie
    # strictly inside their segment — otherwise this is the other configuration
    if not 0 < ((e - a) / (c - a)).real < 1:
        return None
    if not 0 < ((f - a) / (b - a)).real < 1:
        return None
    return abs(e - f), abs(b - f), abs(c - e), abs(d - f)


def check(ef=9, bf=16):
    """Independent: find a real triangle with the printed EF : BF and measure CE.

    The apex slides along a ray; for each position the two bisectors are
    intersected and the parallel through D is cut against the two sides, all by
    coordinates. The figure is then scaled so BF matches, and CE is read off it.
    FD = FB and ED = EC are never assumed — if the construction disagreed, the
    measured CE would too.
    """
    if ef <= 0 or bf <= 0 or ef >= bf:
        return None
    wanted = ef / bf

    def measure(height):
        """Slide the apex across at a fixed height until EF : BF matches."""
        def residual(x):
            got = _figure((x, height))
            return None if got is None else got[0] / got[1] - wanted

        previous = None
        steps = 3000
        lo = hi = None
        for i in range(1, steps):
            x = 0.5 + 12.0 * i / steps
            value = residual(x)
            if value is None:
                previous = None
                continue
            if value == 0.0:
                lo = hi = x
                break
            if previous is not None and previous[1] * value < 0:
                lo, hi = previous[0], x
                break
            previous = (x, value)
        if lo is None:
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
        got = _figure(((lo + hi) / 2, height))
        if got is None:
            return None
        measured_ef, measured_bf, measured_ce, measured_fd = got
        if measured_bf < 1e-9:
            return None
        if abs(measured_fd - measured_bf) > 1e-7 * measured_bf:
            return None                  # FD = FB comes out of the figure
        scale = bf / measured_bf
        if abs(measured_ef * scale - ef) > 1e-6 * ef:
            return None
        return measured_ce * scale

    # Several apex heights, so nothing depends on the shape chosen. They have to
    # be flat ones: with BC = 1 the achievable EF : BF is 1 − AC/AB, and a tall
    # apex cannot push that ratio near 1 however far it slides sideways.
    found = [m for m in (measure(h) for h in (0.03, 0.08, 0.2, 0.5, 1.2))
             if m is not None]
    if len(found) < 2:
        return None
    if max(found) - min(found) > 1e-6 * max(1.0, max(found)):
        return None
    return found[0]
