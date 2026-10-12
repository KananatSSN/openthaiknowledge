"""ข้อ 24 — ค่าของ AD² เมื่อ AD เป็นเส้นผ่านศูนย์กลาง

กำหนดให้วงกลมมี AD เป็นเส้นผ่านศูนย์กลาง และ AC ตัดกับ BD ที่จุด E ดังรูป
ถ้า AE = √13 หน่วย, BE = 2 หน่วย และ CD − CE = 3 หน่วย แล้วจงหาค่าของ AD²

AD is a diameter, so **both B and C see it at a right angle** — that is the only
fact the figure adds, and it is used twice.

* In △ABE the right angle is at B, so AB² = AE² − BE² = 13 − 4, giving AB = 3.
* Write CE = c, so CD = c + 3. The power of the point E gives AE·EC = BE·ED,
  i.e. ED = √13·c/2, while the right angle at C gives ED² = EC² + CD². Together

      13c²/4 = c² + (c+3)²   ⟹   5c² − 24c − 36 = 0   ⟹   c = 6

* Then AC = AE + EC = √13 + 6 and AD² = AC² + CD² = (√13+6)² + 81
  = **130 + 12√13** ≈ 173.27.

Cross-checked the other way round: AD² = AB² + BD² = 9 + (2 + 3√13)², the same
value — so the two right angles agree, which they must.

``solve`` runs that algebra. ``check`` builds the circle: it takes the diameter
as an unknown, places C on the circle so that AE is the printed length, finds B
as the second crossing of line DE, and bisects on the diameter until BE comes out
right — then measures AD² off the figure.
"""

from __future__ import annotations

import math

#: AE² (the stem prints AE as a surd), BE, and CD − CE.
PARAMS = {"ae_sq": 13, "be": 2, "gap": 3}
ANSWER = 130 + 12 * math.sqrt(13)
TOL = 1e-5
VARIANTS = [
    {"ae_sq": 25, "be": 3, "gap": 4},
    {"ae_sq": 13, "be": 2, "gap": 5},
    {"ae_sq": 20, "be": 4, "gap": 2},
    {"ae_sq": 36, "be": 5, "gap": 3},
    {"ae_sq": 4, "be": 3, "gap": 3},      # BE > AE: no right triangle ABE
    {"ae_sq": 50, "be": 5, "gap": 6},
]


def solve(ae_sq=13, be=2, gap=3):
    """Solve 5c² − 24c − 36 = 0 in general form, then AD² = AC² + CD²."""
    if ae_sq <= 0 or be <= 0 or gap <= 0:
        return None
    ae = math.sqrt(ae_sq)
    if be >= ae:
        return None                      # E must lie inside, with AB real
    # ED = ae·c/be from the power of the point; ED² = c² + (c+gap)²
    # ⟹ (ae²/be² − 2)c² − 2·gap·c − gap² = 0
    a = ae_sq / (be * be) - 2
    b, c0 = -2 * gap, -gap * gap
    if a == 0:
        return None
    disc = b * b - 4 * a * c0
    if disc < 0:
        return None
    roots = [(-b + math.sqrt(disc)) / (2 * a), (-b - math.sqrt(disc)) / (2 * a)]
    positive = [r for r in roots if r > 0]
    if len(positive) != 1:
        return None
    c = positive[0]
    ac = ae + c
    cd = c + gap
    return ac * ac + cd * cd


def _figure(diameter, ae_sq, gap):
    """A = (0,0), D = (diameter, 0); place C, then E, then B. Returns lengths."""
    if diameter <= 0:
        return None
    radius = diameter / 2
    centre = (radius, 0.0)
    ae = math.sqrt(ae_sq)
    # C on the circle with A–E–C collinear and AE the printed length: sweep the
    # direction of AC and take the one where CD − CE is the printed gap.
    def build(theta):
        ux, uy = math.cos(theta), math.sin(theta)
        # second crossing of the ray from A with the circle
        ac = 2 * (centre[0] * ux + centre[1] * uy)
        if ac <= ae:
            return None
        c = (ac * ux, ac * uy)
        e = (ae * ux, ae * uy)
        d = (diameter, 0.0)
        ce = ac - ae
        cd = math.hypot(c[0] - d[0], c[1] - d[1])
        return c, e, d, cd - ce

    previous = None
    steps = 3000
    found = None
    for i in range(1, steps):
        theta = math.pi / 2 * i / steps
        got = build(theta)
        if got is None:
            previous = None
            continue
        value = got[3] - gap
        if value == 0.0:
            found = theta
            break
        if previous is not None and previous[1] * value < 0:
            lo, hi = previous[0], theta
            for _ in range(200):
                mid = (lo + hi) / 2
                g_mid, g_lo = build(mid), build(lo)
                if g_mid is None or g_lo is None:
                    return None
                if (g_mid[3] - gap) * (g_lo[3] - gap) <= 0:
                    hi = mid
                else:
                    lo = mid
            found = (lo + hi) / 2
            break
        previous = (theta, value)
    if found is None:
        return None
    got = build(found)
    if got is None:
        return None
    c, e, d, _ = got

    # B: the second crossing of the line D→E with the circle
    dx, dy = e[0] - d[0], e[1] - d[1]
    step = math.hypot(dx, dy)
    if step < 1e-12:
        return None
    dx, dy = dx / step, dy / step
    fx, fy = d[0] - centre[0], d[1] - centre[1]
    beta = 2 * (fx * dx + fy * dy)
    gamma = fx * fx + fy * fy - radius * radius
    disc = beta * beta - 4 * gamma
    if disc < 0:
        return None
    t = max((-beta - math.sqrt(disc)) / 2, (-beta + math.sqrt(disc)) / 2)
    b = (d[0] + t * dx, d[1] + t * dy)
    del c
    return math.hypot(b[0] - e[0], b[1] - e[1])


def check(ae_sq=13, be=2, gap=3):
    """Independent: bisect the diameter until the built BE is the printed one.

    The circle is drawn first and the lengths measured off it — the right angles
    at B and C are consequences of the construction, never inputs, and the power
    of the point is never invoked. AD² comes back as the square of the diameter
    that made BE come out right.
    """
    if ae_sq <= 0 or be <= 0 or gap <= 0:
        return None
    ae = math.sqrt(ae_sq)
    if be >= ae:
        return None

    def residual(d):
        got = _figure(d, ae_sq, gap)
        return None if got is None else got - be

    previous = None
    steps = 2000
    lo = hi = None
    for i in range(1, steps):
        d = ae + 60.0 * ae * i / steps
        value = residual(d)
        if value is None:
            previous = None
            continue
        if value == 0.0:
            lo = hi = d
            break
        if previous is not None and previous[1] * value < 0:
            lo, hi = previous[0], d
            break
        previous = (d, value)
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
    diameter = (lo + hi) / 2
    return diameter * diameter
